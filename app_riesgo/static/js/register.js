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
	//Send the proper header information along with the request
	//http.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	
	//http.setRequestHeader("Content-length", params.length);
	//http.setRequestHeader("Connection", "close");
	
	//http.onreadystatechange = function() {//Call a function when the state changes.
	//if(http.readyState == 4 && http.status == 200) {
	//	alert(http.responseText);
	//}
	/*
	$(document).ready(function() {
	$('form').on('submit', function(event) {
		$.ajaxSetup({async:true});
		$.ajax({
			data: {
  				'nombre': name,  //  to the GET parameters
				'usuario': user,
				'contraseña': password
			},	
			type : 'POST',
			url : '/user_register/',
			async: true
		}).done(function(data) {
			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				console.log("llega");
				$('#successAlert').text(data.nombre).show();
				$('#errorAlert').hide();
				

			}
		});
			event.preventDefault();

		});

	});
	*/

}
