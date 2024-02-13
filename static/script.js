window.addEventListener("DOMContentLoaded", () => {
    document.getElementById('form').addEventListener('submit', function(event){
        event.preventDefault();
        askQuestion()
    });
});
function askQuestion() {
    initialize()
    var question = document.getElementById('question').value;
    fetch('./search?question=' + encodeURIComponent(question))
        .then(response => response.text())
        .then(data =>{
            console.log("TEST 2")
            data=JSON.parse(data)
            console.log(data)
            aText1=new Array(data['answer'])
            iArrLength1=aText1[0].length
            document.getElementsByClassName('spinner')[0].style.display='none'
            aText2=new Array("URL:"+data['url'])
            iArrLength2=aText2[0].length
            timer=(iSpeed+27)*iArrLength2
            typewriter2()
            setTimeout(typewriter1, timer)
            document.getElementById('url').setAttribute('href',data['url'])  
        })
        .catch(error => {
            console.error('Error:', error);
    });
}
var iSpeed = 50; // time delay of print out
var iIndex1// start printing array at this posision
var iIndex2 
var iArrLength1// the length of the text array   
var iArrLength2
var iScrollAt = 20; // start scrolling up at this many lines
var iTextPos1 // initialise text position
var iTextPos2
var sContents1 // initialise contents variable
var sContents2
var iRow1 // initialise current row
var iRow2

function initialize(){
    document.getElementById('url').innerHTML=''
    document.getElementById('answer').innerHTML=''
    document.getElementsByClassName('spinner')[0].style.display='block'
    iIndex1 = 0;
    iTextPos1 = 0;
    sContents1 = ''
    iRow1=0
    iIndex2 = 0;
    iTextPos2 = 0;
    sContents2 = ''
    iRow2=0
}
function typewriter1(){
    sContents1 =  ' ';
    var destination1 = document.getElementById("answer");
    destination1.innerHTML = sContents1 + aText1[iIndex1].substring(0, iTextPos1) + "|";
    if ( iTextPos1++ == iArrLength1 ) {
        iTextPos1 = 0;
        iIndex1++;
        if ( iIndex1 != aText1.length ) {
            iArrLength1 = aText1[iIndex1].length;
            setTimeout("typewriter1()", 500);
        }
    } else {
        setTimeout("typewriter1()", iSpeed);
    }
}

function typewriter2(){
    sContents2 =  ' ';
    var destination2 = document.getElementById("url");
    destination2.innerHTML = sContents2 + aText2[iIndex2].substring(0, iTextPos2) + "|";
    if ( iTextPos2++ == iArrLength2 ) {
        iTextPos2 = 0;
        iIndex2++;
        if ( iIndex2 != aText2.length ) {
            iArrLength2 = aText2[iIndex2].length;
            setTimeout("typewriter2()", 500);
        }
    } else {
        setTimeout("typewriter2()", iSpeed);
    }
}