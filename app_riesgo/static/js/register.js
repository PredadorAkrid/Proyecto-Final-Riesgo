function myFuncRegister(){
	name = document.getElementById('nombre').value;
	user = document.getElementById('usuario').value;
	password = document.getElementById('contraseña').value;
	confPassword = document.getElementById('contraseña_conf').value;
	grupo = document.getElementById('grupo').value;

	var regexName = /^[a-zA-Z ]{2,64}$/;
	var regexPwd = /^[a-zA-Z0-9$^+=!*()@%&]{8,16}$/;
	var regexUsr = /^[a-zA-Z0-9%$@]{5,64}$/;
	if(regexName.test(name)){
		if(regexPwd.test(password)){
			if(regexUsr.test(user)){
				if(password  == confPassword){
				var http = new XMLHttpRequest();
				var url = "/user_register";
				var params = (name + "," + user + ","+ password + "," + grupo);
				http.open("POST", url, false);
				http.send(params);
				window.location.href = "/"
	
				}else{
					alert("Las contraseñas no coinciden")
				}
			}else{
				alert("El usuario solo puede contener letras mayúsculas, minúsculas, números y los caracteres %$@\nLa longitud máxima es de 64 y la mínima de 5")
			}
			
		}else{
			alert("La contraseña debe tener mayúscula, minúscula, numero o caracter especial  $^+=!*()@%&\nLa longitud máxima es de 16 y la mínima de 8")
		}
	}else{
		alert("Error en el nombre, solo se permiten letras mayúsculas minúsculas y espacios\nLa longitud máxima es 64 y la mínima de 2")
	}
	
	

}

