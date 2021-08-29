var i = 0;
var txt = 'Get a Quick Overview of a Dataset...';
var speed = 100;

$(document).ready(function typeWriter() {
    if (sessionStorage.getItem('anime-count') == null) {
        if (i < txt.length) {
            document.getElementById("content-explain").innerHTML += txt.charAt(i);
            i++;
            setTimeout(typeWriter, speed);
        }
        else {
            sessionStorage.setItem('anime-count', 1);      // set animation count to 1 so it wont repeat
        }
    }
    else{                                           // after refreshing to avoid "no text" 
        document.getElementById("content-explain").innerHTML = txt;
    }
});

let load_images = ['loading.gif', 'loading-1.gif']

function start_analysis(){
    document.getElementById('content').innerHTML='';    //remove all body

    let rand_num = Math.floor(Math.random()*2);         // pick loading gif randomly
    document.getElementById('loader').innerHTML = "<img src=../static/"+load_images[rand_num]+"/>";
    document.getElementById('loader').style.display = "block";
    //typing_2();
    
    window.location.href = "/Analysis";
    
}
