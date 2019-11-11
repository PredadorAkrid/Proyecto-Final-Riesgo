var caracteresEspeciales= /[ !@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/
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
  caracteres="!#$%&/()=@*+¿?¡-\"@ł€¶ŧ←↓→øþæßðđŋħł~«»¢“”nµ─·─_ "
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
    confirma=/[a-z]/.test(name)
    confirma2=/[A-Z]/.test(name)
    confirma3= caracteresEspeciales.test(name)
    confirma4= /[0-9]/.test(name)
    console.log(confirma || confirma2);
    console.log("Este es confirma 3 " + !confirma3)
    if ((name.length!=0) && name.length<10 && (confirma || confirma2) && !confirma3 && !(confirma4)) {
      //alert("Nombre Guardado")
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
  confirma=/[a-z]/.test(name)
  confirma2=/[A-Z]/.test(name)
  confirma3= caracteresEspeciales.test(name)
  confirma4= /[0-9]/.test(name)

  if ((name.length!=0) && (confirma || confirma2 || confirma4) && !confirma3   ) {
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
  const guiones=/[\-_]/
  confirma=/[a-z]/.test(con)
  confirma2=/[A-Z]/.test(con)
  confirma3= guiones.test(con)
  confirma4= /[0-9]/.test(con)


  if ((con.length!=0) && con.length>5 && (confirma || confirma2 ) && confirma4 && !confirma3) {

      return true;
  }

    alert("Esa contraseña no esta permitida ya que tiene - o _ y Porfavor verifique que las contraseñas coicidan :(" )
    return false;
}

/**

*/
function confirmaContrasena(event){
    var con = document.getElementById("password-1").value;
    var con2=document.getElementById("password-2").value;
    if(con==con2 && validar_contrasena(event)){
      alert("Contraseña Guardada")
      return true;
    }

    return false;

}
