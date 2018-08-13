(function($){
	$.fn.jTruncSubstr = function(options) {
	   
		var defaults = {
			length: 300,
			minTrail: 20,
			moreText: "more",
			lessText: "less",
			ellipsisText: "...",
			moreAni: 500,
			lessAni: 500,
			delimiters: ""
		};
		
		var options = $.extend(defaults, options);
	   
		return this.each(function() {
			obj = $(this);
			var body = obj.html();
			
			if(body.length > options.length + options.minTrail) {
				var splitLocation;
				if(options.delimiters == ""){
					splitLocation = options.length;
				}else{
					splitLocation = body.length;
					$.each(options.delimiters, function(){
						var pos = body.indexOf(this, options.length);
						if(pos > -1)
							splitLocation = Math.min(splitLocation, pos);
					});
				}
				if(splitLocation != -1) {
					// truncate tip
					var str1 = body.substring(0, splitLocation+1);
					var str2 = body.substring(splitLocation+1, body.length - 1);
					obj.html(str1 + '<span class="truncate_ellipsis">' + options.ellipsisText + 
						'</span>' + '<span class="truncate_more">' + str2 + '</span>');
					obj.find('.truncate_more').css("display", "none");
					
					// insert more link
					obj.append(
						'<div class="clearboth">' +
							'<a href="#" class="truncate_more_link">' + options.moreText + '</a>' +
						'</div>'
					);

					// set onclick event for more/less link
					var moreLink = $('.truncate_more_link', obj);
					var moreContent = $('.truncate_more', obj);
					var ellipsis = $('.truncate_ellipsis', obj);
					moreLink.click(function() {
						if(moreLink.text() == options.moreText) {
							if(options.moreAni){
								moreContent.slideDown(options.moreAni);
							}else{
								moreContent.show();
							}
							moreLink.text(options.lessText);
							ellipsis.css("display", "none");
						} else {
							if(options.lessAni){
								moreContent.slideUp(options.lessAni);
							}else{
								moreContent.hide();
							}
							moreLink.text(options.moreText);
							ellipsis.css("display", "inline");
						}
						return false;
				  	});
				}
			} // end if
			
		});
	};
})(jQuery);
