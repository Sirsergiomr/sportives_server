$(function() {

	window.mobilecheck = function() {
	var check = false;
	(function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4)))check = true})(navigator.userAgent||navigator.vendor||window.opera);
	return check; }

	if(!window.mobilecheck()){
		$.stellar({
			responsive: true,
			horizontalScrolling: false
		});
	}
	
	$('.homepage .navbar').affix({
		offset: {
			top: 100
		, bottom: function () {
			return (this.bottom = $('.bs-footer').outerHeight(true))
			}
		}
	});
	
	if ($("#carousel").length > 0){
		$('#carousel').carouFredSel({
			responsive: false,
			scroll: 1,
			pagination: "#pager",
			items: {
				width: 374,
				visible: {
					min: 4,
					max: 20
				}
			}
		});
	}
	
	if ($("#tabs").length > 0){
		$("#tabs").tabs();
	}
	
	if ($("#accordion").length > 0){
		$("#accordion").accordion();
	}
	
	if ($("#map").length > 0){
		$('#map').gmap3({
			map: {
			    options:{
			        zoom:16,
			        center: [51.576084, 0.488736],
			        mapTypeId: google.maps.MapTypeId.MAP,
			        mapTypeControl: false,
			        mapTypeControlOptions: {
			          style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
			        },
			        navigationControl: false,
			        scrollwheel: false,
			        streetViewControl: false
			    }
			},
			marker:{
			    latLng: [51.576084, 0.488736],
			    options: {
				    icon: new google.maps.MarkerImage(
				        "images/map-pin.png", new google.maps.Size(223, 167, "px", "px")
				    )
			    }
			 }
			}
	
		);
	}
	
	// delegate calls to data-toggle="lightbox"
	$(document).delegate('*[data-toggle="lightbox"], .lightbox', 'click', function(event) {
		event.preventDefault();
		return $(this).ekkoLightbox({
			onShown: function() {
				if (window.console) {
					return console.log('Checking our the events huh?');
				}
			}
		});
	});
	
});


/* Waucan javascript */
$(function(){
	// vars for clients list carousel
	// http://stackoverflow.com/questions/6759494/jquery-function-definition-in-a-carousel-script
	var $clientcarousel = $('#clients-list');
	var clients = $clientcarousel.children().length;
	var clientwidth = (clients * 220); // 140px width for each client item
	$clientcarousel.css('width',clientwidth);

	var rotating = true;
	var clientspeed = 0;
	var seeclients = setInterval(rotateClients, clientspeed);

	$(document).on({
	mouseenter: function(){
	  rotating = false; // turn off rotation when hovering
	},
	mouseleave: function(){
	  rotating = true;
	}
	}, '#clients');

	function rotateClients() {
		if(rotating != false) {
		  var $first = $('#clients-list li:first');
		  $first.animate({ 'margin-left': '-220px' }, 5000, "linear", function() {
			$first.remove().css({ 'margin-left': '0px' });
			$('#clients-list li:last').after($first);
		  });
		}
	}

	$('.counter').each(function () {
		$(this).prop('Counter',0).animate({
			Counter: $(this).text()
		}, {
			duration: 2800,
			easing: 'swing',
			step: function (now) {
				$(this).text(Math.ceil(now));
			}
		});
	});


	/* Menu JS */
	$('.navbar-nav a').on('click', function(e){
		if($(this).attr('href') != "/") {
			var anchor = $(this).attr('href').split("/");
			$('html, body').stop().animate({
				scrollTop: $(anchor[anchor.length - 1]).offset().top - 50
			}, 1500);
			e.preventDefault();
		}
	});

	/* Go To Top */
	$(function(){
		//Scroll event
		$(window).on('scroll', function(){
			var scrolled = $(window).scrollTop();
			if (scrolled > 300) $('.go-top').fadeIn('slow');
			if (scrolled < 300) $('.go-top').fadeOut('slow');
		});
		//Click event
		$('.go-top').on('click', function() {
			$("html, body").animate({ scrollTop: "0" },  1000);
		});
	});
});
