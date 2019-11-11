function myfunc(){
$(document).ready(function() {

	$('form-calif').on('submit', function(event) {
		$.ajaxSetup({async:true});
		$.ajax({
			//data : {
			//	calificacion : '1',
			//	lectura : '2'
			//},
			data: {
  				'calificacion': '07',  //  to the GET parameters
				'lectura': '05',
				'unidad': '01'
			},	
			type : 'POST',
			url : '/calif-lectura',
			async: true
		}).done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.calificacion).show();
				$('#errorAlert').hide();
				location.reload(true)
			}

		});

		event.preventDefault();

	});

});

}