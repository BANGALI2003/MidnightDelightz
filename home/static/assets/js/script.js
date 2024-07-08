(function($){
	'use script';


	var $loader = $('#preloader');
    if($loader.length > 0){
		$(window).on('load', function(event) {
	        $('#preloader').delay(500).fadeOut(500);
		});
	}



	// Scroll Area
	var $scroll = $('.scroll-area');
	if($scroll.length > 0){
		$(document).ready(function(){
		    $('.scroll-area').click(function(){
		      	$('html').animate({
		        	'scrollTop' : 0,
		      	},700);
		      	return false;
		    });
		    $(window).on('scroll',function(){
		      	var a = $(window).scrollTop();
		      	if(a>400){
		            $('.scroll-area').slideDown(300);
		        }else{
		            $('.scroll-area').slideUp(200);
		        }
		    });
		});
	}

	//video
		var $video = $('.technology-video a');
	    if($video.length > 0){
			$('.technology-video a').magnificPopup({
			  	type: 'iframe',
			});	
	 }
		


	///add minicart login serach
	  let searchForm = document.querySelector('.search-form');

        document.querySelector('#search-btn').onclick = () =>{
         searchForm.classList.toggle('active');
         shoppingCart.classList.remove('active');
         loginForm.classList.remove('active');
        }

        let shoppingCart = document.querySelector('.mini-cart-side');

        document.querySelector('#cart-btn').onclick = () =>{
             shoppingCart.classList.toggle('active');
             searchForm.classList.remove('active');
             loginForm.classList.remove('active');
        }

        let loginForm = document.querySelector('.login-form');

        // document.querySelector('#login-btn').onclick = () =>{
        //     loginForm.classList.toggle('active');
        //     searchForm.classList.remove('active');
        //     shoppingCart.classList.remove('active');
            
        // }

    //     window.onscroll = () =>{
    //     searchForm.classList.remove('active');
    //     shoppingCart.classList.remove('active');
    //     loginForm.classList.remove('active');
        
    // }


    // close
    document.querySelector('#close-btn').onclick = () =>{
       shoppingCart.classList.remove('active');
    }
     document.querySelector('#close-login').onclick = () =>{
       loginForm.classList.remove('active');
    }



   		///banner
   		var $full = $('.slider-area-full');
		    if($full.length > 0){
		    $(document).ready(function(){
			  	$(".slider-area-full").owlCarousel({
			  		loop:true,
			  		center:true,
			  		items:1,
			  		autoplay: true,
			  		nav: true,
		  			navText: ["<i class='fas fa-long-arrow-alt-left'></i>","<i class='fas fa-long-arrow-alt-right'></i>"],
			  	});
			});
			}

			//product
	    	var $product = $('.product-slider');
		    if($product.length > 0){
		      $(document).ready(function(){
			  	$(".product-slider").owlCarousel({
			  		loop:false,
			  		center:false,
			  		margin:10,
			  		items:4,
			  		autoplay: true,
			  		nav: true,
		  			navText: ["<i class='fas fa-long-arrow-alt-left'></i>","<i class='fas fa-long-arrow-alt-right'></i>"],
		  			responsive:{
		  				0:{
		  					items:1,
		  				},
		  				430:{
		  					items:2,
		  				},
		  				767:{
		  					items:3,
		  				},
		  				991:{
		  					items:4,
		  				},
		  			}
			  	});
			});
	  	}

	  	///category
	      var $category_slider= $('.category-slider');
	 		if($category_slider.length > 0){
		       $(document).ready(function(){
			  	$(".category-slider").owlCarousel({
			  		loop:true,
			  		center:false,
			  		margin:10,
			  		items:4,
			  		autoplay: false,
			  		nav: true,
		  			navText: ["<i class='fas fa-long-arrow-alt-left'></i>","<i class='fas fa-long-arrow-alt-right'></i>"],
		  			responsive:{
		  				0:{
		  					items:1,
		  				},
		  				430:{
		  					items:2,
		  				},
		  				767:{
		  					items:3,
		  				},
		  				991:{
		  					items:4,
		  				},
		  			}
			  	});
			});
	      } 

	      ///client
	    var $clint = $('.client-slider');
	    if($clint.length > 0){
		 $(document).ready(function(){
		    $(".client-slider").owlCarousel({ 
	            loop: true,
	            autoplay: true,
	            autoplayTimeout: 9000,
	            items: 2,
	            nav: true,
  			    navText: ["<i class='fas fa-long-arrow-alt-left'></i>","<i class='fas fa-long-arrow-alt-right'></i>"],
	            responsive : {
				    // breakpoint from 0 up
				    0 : {
				        items:1,
				    },
				    // breakpoint from 480 up
				    480 : {
				        items:1,
				    },
				    // breakpoint from 768 up
				    768 : {
				       items:1,
				    },
				      929 : {
				       items:2,
				    }
				}
		    });
		});
	}


	//blog
	var $news = $('#news-slider');
	 if($news.length > 0){
	$(document).ready(function() {
	    $("#news-slider").owlCarousel({
	        items : 2,
	        itemsDesktop:[1199,2],
	        itemsDesktopSmall:[980,2],
	        itemsTablet:[650,1],
	        pagination:false,
	        navigation:true,
	        nav: true,
		    navText: ["<i class='fas fa-long-arrow-alt-left'></i>","<i class='fas fa-long-arrow-alt-right'></i>"],
		    responsive : {
				    // breakpoint from 0 up
				    0 : {
				        items:1,
				    },
				    590 : {
				        items:2,
				    },
				}
		    });
		});
	}	
	// slick
	var $slick = $('.slider-for');
	 if($slick.length > 0){
	 $('.slider-for').slick({
			  slidesToShow: 1,
			  slidesToScroll: 1,
			  arrows: true,
			  fade: true,
			  prevArrow:'<span class="prev-arrow"><i class="fas fa-chevron-right"></i></span>',
			  nextArrow:'<span class="next-arrow"><i class="fas fa-chevron-left"></i></span>',
			});
			$('.slider-nav').slick({
			  slidesToShow: 3,
			  slidesToScroll: 1,
			  asNavFor: '.slider-for',
			  dots:false,
			  centerMode: false,
			  focusOnSelect: true
			});
			$('.responsive').slick({
			  dots: true,
			  infinite: false,
			  speed: 300,
			  slidesToShow: 4,
			  slidesToScroll: 4,
			  responsive: [
			    {
			      breakpoint: 1024,
			      settings: {
			        slidesToShow: 4,
			        slidesToScroll: 1,
			        infinite:false,
			        dots:false
			      }
			    },
			    {
			      breakpoint: 600,
			      settings: {
			        slidesToShow: 4,
			        slidesToScroll: 1,
			        infinite:false,
			      }
			    },
			    {
			      breakpoint: 480,
			      settings: {
			        slidesToShow: 4,
			        slidesToScroll: 1,
			        infinite:false,
			      }
			    }
			  ]
			});
		}
			var $nav = $('.slider-nav2');
	 		if($nav.length > 0){
			$('.slider-nav2').slick({
			  slidesToShow: 2,
			  slidesToScroll: 1,
			  asNavFor: '.slider-for',
			  dots:false,
			  centerMode: false,
			  focusOnSelect: true
			});
			}


		
	
	//ui
	var $tab = $('#tabs');
	if($tab.length > 0){
	$( function() {
	    $( "#tabs" ).tabs();
	  } );
	}


		//===== Mobile Menu
    $('.mobile-menu-open').on('click', function(){
        $('.mobile-off-canvas-menu').addClass('open')
        $('.overlay').addClass('open')
    });
    

    $('.close-mobile-menu').on('click', function(){
        $('.mobile-off-canvas-menu').removeClass('open')
        $('.overlay').removeClass('open')
    });
    
    $('.overlay').on('click', function(){
        $('.mobile-off-canvas-menu').removeClass('open')
        $('.overlay').removeClass('open')
    });
    
    
   
    
    /*Variables*/
    var $offCanvasNav = $('.mobile-main-menu'),
        $offCanvasNavSubMenu = $offCanvasNav.find('.mega-sub-menu, .sub-menu, .submenu-item ');

    /*Add Toggle Button With Off Canvas Sub Menu*/
    $offCanvasNavSubMenu.parent().prepend('<span class="mobile-menu-expand"></span>');

    /*Close Off Canvas Sub Menu*/
    $offCanvasNavSubMenu.slideUp();

    /*Category Sub Menu Toggle*/
    $offCanvasNav.on('click', 'li a, li .mobile-menu-expand, li .menu-title', function(e) {
        var $this = $(this);
        if (($this.parent().attr('class').match(/\b(menu-item-has-children|has-children|has-sub-menu)\b/)) && ($this.attr('href') === '#' || $this.hasClass('mobile-menu-expand'))) {
            e.preventDefault();
            if ($this.siblings('ul:visible').length) {
                $this.parent('li').removeClass('active-expand');
                $this.siblings('ul').slideUp();
            } else {
                $this.parent('li').addClass('active-expand');
                $this.closest('li').siblings('li').find('ul:visible').slideUp();
                $this.closest('li').siblings('li').removeClass('active-expand');
                $this.siblings('ul').slideDown();
            }
        }
    });
	
	
	
class Slider {
  constructor (rangeElement, valueElement, options) {
    this.rangeElement = rangeElement
    this.valueElement = valueElement
    this.options = options

    // Attach a listener to "change" event
    this.rangeElement.addEventListener('input', this.updateSlider.bind(this))
  }

  // Initialize the slider
  init() {
    this.rangeElement.setAttribute('min', options.min)
    this.rangeElement.setAttribute('max', options.max)
    this.rangeElement.value = options.cur

    this.updateSlider()
  }

  // Format the money
  asMoney(value) {
    return '$' + parseFloat(value)
      .toLocaleString('en-US', { maximumFractionDigits: 2 })
  }

  generateBackground(rangeElement) {   
    if (this.rangeElement.value === this.options.min) {
      return
    }

    let percentage =  (this.rangeElement.value - this.options.min) / (this.options.max - this.options.min) * 100
    return 'background: linear-gradient(to right, #FF593A, #DA4D54 ' + percentage + '%, #FC3C46 ' + percentage + '%, white 100%)'
  }

  updateSlider (newValue) {
    this.valueElement.innerHTML = this.asMoney(this.rangeElement.value)
    this.rangeElement.style = this.generateBackground(this.rangeElement.value)
  }
}

let rangeElement = document.querySelector('.range [type="range"]')
let valueElement = document.querySelector('.range .range__value span') 

let options = {
  min: 20,
  max: 200,
  cur: 375
}

if (rangeElement) {
  let slider = new Slider(rangeElement, valueElement, options)

  slider.init()
}

}(jQuery));
