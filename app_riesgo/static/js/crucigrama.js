var palabras1 = ["handheld", "graphics", "console", "release", "joystick"];
var palabras2 = ["ancestor", "skeleton", "tombstone", "custom", "soul"];

function revisar1(){
    var calif =  revisar(palabras1);
    var stringPares;
    if(calif == 10){
      stringPares = "10"
    }
    else{
      stringPares = "0"+calif
    }
    
    var http = new XMLHttpRequest();
    var url = "/calif-lectura";
    window.alert(stringPares)
    var params = ("calificacion="+stringPares + "&lectura=" + "03" + "&unidad="+ "01");
    http.open("POST", url, false);
    http.send(params);
    
    window.location.href = "/home/obligatorias"

}

function revisar2() {
    var calif =  revisar(palabras2);
    var stringPares;
    if(calif == 10){
      stringPares = "10"
    }
    else{
      stringPares = "0"+calif
    }
    var http = new XMLHttpRequest();
    var url = "/calif-lectura";
    window.alert(stringPares)
    var params = ("calificacion="+stringPares + "&lectura=" + "06" + "&unidad="+ "02");
    http.open("POST", url, false);
    http.send(params);
    window.location.href = "/home/obligatorias"
}

function revisar(palabras){
  var respuestas = []
  var temp = [];
  var c = "";
  var v = [];
  for (var i = 0; i < palabras.length; i++) {
    for (var j = 0; j < palabras[i].length; j++) {
      c = (i+1) + "-" + (j+1);
      v = document.getElementsByClassName(c);
      temp.push(v[0].value);
    }
    respuestas.push(temp.join(""));
    temp = [];
  }
      console.log(respuestas);

  var bien = 0;

  for (var i = 0; i < palabras.length; i++) {
    if( palabras[i] === respuestas[i] )
      bien = bien + 1;
  }

  alert("Tuviste bien "+ bien + " palabras de " + palabras.length+".");
  return bien*2;
}