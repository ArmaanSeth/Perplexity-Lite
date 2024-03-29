from langchain import hub
from langchain.agents import create_structured_chat_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.runnables import RunnablePassthrough
from langchain_core.agents import AgentFinish
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from langgraph.graph import END, Graph
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from flask import Flask, render_template, request
from dotenv import load_dotenv
import re

def augment_text(text):
    text=text.replace('\n','<br>')
    pattern = r'\*\*(.*?)\*\*'
    return re.sub(pattern, r'<b>\1</b>', text)

load_dotenv()
llm=ChatGoogleGenerativeAI(model='gemini-pro',convert_system_message_to_human=True, temperature=0.2)
prompt=hub.pull("hwchase17/structured-chat-agent")
tools=[TavilySearchResults(max_results=1)]
agent_runnable=create_structured_chat_agent(llm, tools, prompt)
agent=RunnablePassthrough.assign(agent_outcome=agent_runnable)

def execute_tools(data):
  agent_action=data.pop('agent_outcome')
  tools_to_use={t.name: t for t in tools}[agent_action.tool]
  observation=tools_to_use.invoke(agent_action.tool_input)
  data['intermediate_steps'].append((agent_action, observation))
  return data

def should_continue(data):
  if isinstance(data['agent_outcome'],AgentFinish):
    return 'exit'
  else:
    return 'continue'
  
workflow=Graph()
workflow.add_node('agent', agent)
workflow.add_node('tools', execute_tools)
workflow.set_entry_point("agent")
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        'continue':"tools",
        'exit':END
    }
)
workflow.add_edge('tools','agent')
chain=workflow.compile()

template="""
Given a question and its answer. Rewrite the answer properly to address the question without straight jumping into the answer
Question:{question}
Answer:{answer}
"""
prompt=PromptTemplate(template=template, input_variables=['question','answer'])
chain2=LLMChain(llm=llm, prompt=prompt)


app=Flask(__name__)

@app.route('/')
def index():
  return render_template('./index.html')

@app.route('/search')
def search():
    try:
      ques=request.args.get('question')
      if ques!='':
          res=chain.invoke({"input":ques, 'intermediate_steps':[]})
          ans=res['agent_outcome'].return_values['output']
          url=res['intermediate_steps'][0][1][0]['url']
          ans_=chain2.invoke({'question':ques, "answer":ans})
          res=ans_['text']
          res=augment_text(res)
          return {"answer":res, "url":url}
      else:
        return {"answer":"","url":""} 
    except Exception as e:
      return {"answer":f"ERROR: Unable to find due to exception: {e}", "url":""}

if __name__=="__main__":
  app.run(debug=True, host='0.0.0.0', port=5000)