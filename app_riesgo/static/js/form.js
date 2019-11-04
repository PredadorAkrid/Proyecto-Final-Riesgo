function myfunc(){
$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			//data : {
			//	calificacion : '1',
			//	lectura : '2'
			//},
			data: {
  				'calificacion': '01',  //  to the GET parameters
				'lectura': '01',
				'unidad': '01'
			},	
			type : 'POST',
			url : '/calif-lectura'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.calificacion).show();
				$('#errorAlert').hide();
			}

		});

		event.preventDefault();

	});

}); 
}