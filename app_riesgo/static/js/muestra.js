const cartas = document.querySelectorAll(".card")
const  fondo=document.getElementsByClassName('.contenedor')
let parActual = ""
let parActualId = ""
let guardaPares=[]
let parAnterior



cartas.forEach((element)=>{
    element.addEventListener("click", revisarPares)
})

function EnviarResultado() {
    var numeroPares=guardaPares.length
    var stringPares;
    if(numeroPares == 10){
      stringPares = "10"
    }
    else{
      stringPares = "0"+numeroPares
    }

    var http = new XMLHttpRequest();
    var url = "/calif-lectura";
    window.alert(stringPares)
    var params = ("calificacion="+stringPares + "&lectura=" + "02" + "&unidad="+ "01");
    http.open("POST", url, false);
    http.send(params);
    //alert("Obtuviste  " + numeroPares + " de " + "10 pares posibles.");
    window.location.href = "/home/obligatorias"
    
}

function EnviarResultado2() {
    var numeroPares=guardaPares.length
    var numParesAux = numeroPares*2
    var stringPares;
    if(numParesAux == 10){
      stringPares = "10"
    }
    else{
      stringPares = "0"+numParesAux
    }
    window.alert(stringPares)
    var http = new XMLHttpRequest();
    var url = "/calif-lectura";
    window.alert(stringPares)
    var params = ("calificacion="+stringPares + "&lectura=" + "05" + "&unidad="+ "02");
    http.open("POST", url, false);
    http.send(params);
    //alert("Obtuviste  " + numeroPares + " de " + "10 pares posibles.");
    window.location.href = "/home/obligatorias"
}
function daVueltas(gira,gira2){
  gira.classList.toggle("card-back-flip")
  gira2.classList.toggle("card-front-flip")
}


function revisarPares(evento){
    const clase = this.classList[this.classList.length -1 ]
    imagenes=this.querySelectorAll((".card-back"))
    imagenes2=this.querySelectorAll((".card-front"))
    if (guardaPares.indexOf(clase) !== -1){
      return
    }

    if(parActual === ""){ //

        parActual = clase
        daVueltas(imagenes[0],imagenes2[0])
        parActualId = this.id
        parAnterior=this
        return
    }
    if(this.id!==parActualId && parActual===clase){
        imagenes2=this.querySelectorAll((".card-front"))
        daVueltas(imagenes[0],imagenes2[0])
        var audio2= new Audio("../../../static/audio/bien.wav")
        audio2.play()
        guardaPares.push(parActual)
    }else{
      var audio= new Audio("../../../static/audio/mal.wav")
      imgAnt=parAnterior.querySelectorAll((".card-back"))
      imgAnt2=parAnterior.querySelectorAll((".card-front"))
      daVueltas(imagenes[0],imagenes2[0])
      setTimeout(function() {daVueltas(imagenes[0],imagenes2[0])},425)
      setTimeout(function() {daVueltas(imgAnt[0],imgAnt2[0])},425)
      audio.play()
    }
    parActual = ""
    parActualId = ""
}
