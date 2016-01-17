function loadUrlMetadata(url, url_id){
	var MAX_URL_LENGTH = 69;
	var formattedUrl = url.substr(0, MAX_URL_LENGTH) + (url.length > MAX_URL_LENGTH ? "..." : "");
	var container = $('<div></div>')
						.addClass('stack-item');

	var thumbnailSide = $('<div></div>')
						.addClass('float-left stack-item-img')
						.click(function() {
							window.open(url, '_blank');
						});
	var infoSide = $('<div></div>').addClass('float-left stack-item-info');
	infoSide.html("<p><a href="+url+" target='_blank'>"+formattedUrl+"</a></p><p style='color:#999'>Loading Information...</p>");
	
	var optionStateClicked = false;
	var options = $('<div>pop</div>')
					.click(function() {
						if (optionStateClicked) return;
						optionStateClicked = true;
						var that = this;
						$(this).html("popping...")
						$.ajax({
							url: 'http://'+location.host+'/pop',
							method: 'POST',
							data: {url_id:url_id},
						}).done(function(data) {
							$(that).html("pop");
							$(container).hide();
						});
					})
					.addClass('stack-item-options');

	container.append(thumbnailSide).append(infoSide).append(options);

	$('#stack').prepend(container);

	$.ajax({
		url: 'http://'+location.host+'/fetch/cors',
		method: 'GET',
		data: {url: url}
	}).done(function(data) {
		var response = $('<html/>').html(data);
		var titleValue = $(response).find('title').first().html() || $(response).find('meta[name="twitter:title"], meta[property="og:title"]').first().attr('content') || url;
		var thumbnailUrl = $(response).find('meta[property="og:image"]').first().attr('content');
		var iconUrl = $(response).find('link[rel~="icon"]').first().attr('href');
		var iconError = 0;

		var thumbnail = $('<img>')
					.load(function() {
						if (this.width > this.height) {
							$(this).css({'height':'100%',
										 'width':'auto'});
						}
					})
					.attr('src', thumbnailUrl);
		var icon = $('<img>')
					.addClass('stack-item-icon')
					.error(function() {
						iconError++;
						if (iconError > 1) {
							$(this).hide();
							return;
						}
						this.src = url + (iconUrl[0] != '/' ? '/' : '') +iconUrl;
					})
					.attr('src', iconUrl);
		var title = $('<div></div>')
						.addClass('info-title')
						.append($('<a></a>').attr({'href': url, 'target': '_blank'}).html(titleValue));
		var urlDiv = $('<div></div>')
						.addClass('url-info')
						.append($(icon).addClass('float-left'))
						.append($('<div></div>').addClass('float-left').append($('<a></a>').attr({'href': url, 'target': '_blank'}).html(formattedUrl)))
						.append($('<div></div>').addClass('clear-fix'));

		thumbnailSide.html("");
		infoSide.html("");

		thumbnailSide.append(thumbnail);
		infoSide.append(title)
				.append(urlDiv);

		var clearFix = $('<div></div>').addClass('clear-fix');

		$(container)
			.append(thumbnailSide)
			.append(infoSide)
			.append(clearFix);
	});
}

function showLoadingScreen(txt) {
	$('#load-box').html(txt);
	$('#load-box').show();
}

function closeLoadingScreen() {
	$('#load-box').hide();
}

function addUrl(){
	var url = $('#add-url').val().trim();
	if (url.length == 0) return;
	$.ajax({
		url:'http://'+location.host+'/add',
		data:{url:url},
		method:'POST',
		beforeSend:function() {
			showLoadingScreen('adding...');
		}
	}).done(function(data){
		if(data.success){
			loadUrlMetadata(url, data.url_id);
			$('#add-url').val('');
		}
	}).always(function(data) {
		closeLoadingScreen();
	});
}

function fetchUrls() {
	$.ajax({
		url:'http://'+location.host+'/fetch/urls',
		method:'GET',
		beforeSend:function(){
			showLoadingScreen('Loading..');
		}
	}).done(function(data) {
		data.reverse();
		for (var i = 0; i < data.length; ++i) {
			loadUrlMetadata(data[i].url, data[i].url_id)
		}
	}).always(function(data) {
		closeLoadingScreen();
	});
}

$(document).ready(function() {
	$('#add-url').keydown(function(e){
		if (e.which == 13) {
			addUrl();
			e.preventDefault();
			return false;
		}
	})
	$('#add-submit').click(function(){
		addUrl();
	});

	fetchUrls();
});