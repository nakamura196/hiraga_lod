var arg  = new Object;
url = location.search.substring(1).split('&');

for(i=0; url[i]; i++) {
	var k = url[i].split('=');
	arg[k[0]] = decodeURIComponent(k[1]);
}

if(arg["lang"]){
	sessionStorage.lang = arg["lang"]
}

var en_flg = false;

jQuery(document).ready(function() {
	if(sessionStorage.getItem('lang') == "en"){
		en_flg = true;
		$("#lang").attr("href", "?lang=ja")
		$("#lang").append("Japanese")
	} else {
		$("#lang").attr("href", "?lang=en")
		$("#lang").append("English")
	}
});
