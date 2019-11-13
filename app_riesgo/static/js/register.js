function myFuncRegister(){
	name = document.getElementById('nombre').value;
	user = document.getElementById('usuario').value;
	password = document.getElementById('contraseña').value;
	confPassword = document.getElementById('contraseña_conf').value;
	grupo = document.getElementById('grupo').value;
	window.alert(name + user + password + confPassword + grupo);
	var http = new XMLHttpRequest();
	var url = "/user_register";
	var params = (name + "," + user + ","+ password + "," + grupo);
	http.open("POST", url, false);
	http.send(params);
	window.location.href = "/"
	

}

