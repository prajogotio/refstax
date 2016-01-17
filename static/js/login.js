$(document).ready(function() {
	$('#submit').click(function() {
		var data = {
			username : $('#username').val().trim(),
			password : $('#password').val().trim(),
		};
		if (username.length == 0 || password.length == 0) return;
		$.ajax({
			url: 'http://' + location.host + '/login/submit',
			method: 'POST',
			data: data,
			beforeSend: function() {
				$('#info').html("Logging in...");
			}
		}).done(function(data) {
			if (data.success) {
				location.href = '/';
			}
		}).always(function(data) {
			if (!data.success) {
				$('#info').html("Login failed.");
			} else {
				$('#info').html("Successful. Starting app..")
			}
		})
	});
});