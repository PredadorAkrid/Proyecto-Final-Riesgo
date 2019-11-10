/**
Funcion auxuliar que nos permite saber si en la cadena que sele pasa
tiene numeros devuelve 0 si no hay numero, 1 si hay numeros
*/


function tiene_numeros(texto){
  numeros="0123456789"
 for(i=0; i<texto.length; i++){
    if (numeros.indexOf(texto.charAt(i),0)!=-1){
       return 1;
    }
 }
 return 0;
}

/**
Funcion auxuliar que nos permite saber si en la cadena que sele pasa
tiene caracteres especiales devuelve 0 si no hay numero, 1 si hay algun caracter
especial
*/
function tiene_caracteres_raros (texto){
  caracteres="!#$%&/()=@*+¿?¡"
  for(i=0; i<texto.length; i++){
    if (caracteres.indexOf(texto.charAt(i),0)!=-1){
       return 1;
    }
  }
  return 0;

}
/**
Fucion que nos devuelve true si tu nombre fue aceptado o false
en otro caso
*/
  function validar_nombre(event){
    var name = document.getElementById("save-name").value;
    num=tiene_numeros(name)
    car=tiene_caracteres_raros(name)
    if ((name.length!=0) && name.length<10 && (num==0) && (car==0) ) {
        alert("Nombre guardado")
        return true;
    }
      alert("Ese nombre no esta permitido")
      return false;
  }


/**
Funcion que nos permite saber si es valido el nombre de usuario que eligio
*/
function validar_usuario(event) {
  var name = document.getElementById("name-check").value;
  car=tiene_caracteres_raros(name)
  if ((name.length!=0) && name.length<10 && (car==0) ) {
      alert("Nombre guardado")
      return true;
  }
    alert("Ese nombre no esta permitido")
    return false;
}

/**
*Funcion que valida si la contraseña es valida 
*/
function validar_contrasena(event) {
  var con = document.getElementById("password-1").value;
  num=tiene_numeros(con)
  car=tiene_caracteres_raros(name)
  console.log(con);

  if ((con.length!=0) && con.length>5 && (num==1) ) {

      return true;
  }
  var con2= document.getElementById("password-2").value;
    alert("Ese nombre no esta permitido")
    return false;
}

/**
*/
function confirmaContrasena(event){
    var con = document.getElementById("password-1").value;
    if(con==con2 && validar_contrasena(event)){
      alert("Contraseña Guardada")
      return true;
    }
    alert("Porfavor verifique que las contraseñas coicidan :(");
    return false;

}
