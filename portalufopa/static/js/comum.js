// $(".nano").nanoScroller();

// // Busca
// $("#topo").on('click', '.btn-search', function(event) {
//           event.preventDefault();
//           $("body").addClass('search-active');
//         });

// $(".search-popup-bg").on('click', function(event) {
//           $("body").removeClass('search-active');
//         });

// // alto-contraste
// $("body").on('click', '.ativa-contraste', function(event) {
//           event.preventDefault();
//           /* Act on the event */
//           $('body').toggleClass('contraste');
//       });

//  // aumentando a fonte
//  $(".inc-font").click(function () {
//           var size = $("body").css('font-size');
//           size = size.replace('px', '');
//           size = parseInt(size) + 1.4;
//           $("body").animate({'font-size' : size + 'px'});
//       });

//  //diminuindo a fonte
// $(".dec-font").click(function () {
//         var size = $("body").css('font-size');
//         size = size.replace('px', '');
//         size = parseInt(size) - 1.4;
//         $("body").animate({'font-size' : size + 'px'});
//       });

// // resetando a fonte
// $(".res-font").click(function () {
//         $("body").animate({'font-size' : '10px'});
//       });

$(document).ready(function () {
  // menu hover

  if(screen.width > 767){  
    $('ul.nav li.dropdown').hover(function() {
      $(this).find('.dropdown-menu1').stop(true, true).delay(0).fadeIn(50);
        }, function() {
        $(this).find('.dropdown-menu1').stop(true, true).delay(0).fadeOut(50);
      });

    // fix lateral comum  
  $('#lateral').affix({
    offset: {     
      top: 500,
      bottom:  $('.rodape').outerHeight(true)
    }
  });
  }

  // fim meunu hover
  
// alto-contraste
  $("body").on('click', '.ativa-contraste', function(event) {
    event.preventDefault();
    /* Act on the event */
  $('body').toggleClass('contraste');
  });
  
  // aumentando a fonte
  $(".inc-font").click(function () {
    var size = $("body").css('font-size');
    size = size.replace('px', '');
    size = parseInt(size) + 1.4;
    $("body").animate({'font-size' : size + 'px'});
  });

  //diminuindo a fonte
  $(".dec-font").click(function () {
    var size = $("body").css('font-size');
    size = size.replace('px', '');
    size = parseInt(size) - 1.4;
    $("body").animate({'font-size' : size + 'px'});
  });

  // resetando a fonte
  $(".res-font").click(function () {
    $("body").animate({'font-size' : '14px'});
  });
//nano 
  $(".nano").nanoScroller();
  $(".nanoAgenda").nanoScroller();
  

  $(document).ready(function() {
      var navpos = $('#menu').offset();
      console.log(navpos.top);
      $(window).bind('scroll', function() {
        if ($(window).scrollTop() > navpos.top) {
          $('#menu').addClass('navbar-fixed-top');
          $('#destaque').css('margin-top','90px');
          $('#menu').css('border-bottom','1px solid #ccc');
        }
        else {
          $('#menu').removeClass('navbar-fixed-top');
          $('#menu').css('border-bottom','0px');
          $('#destaque').css('margin-top','30px');

        }

        $("#linksmenu").on('click',function(e) {
          e.preventDefault();
          $("#wrapper").toggleClass("toggled");
        });
      });

  });


    // busca
    $("#topo").on('click', '.btn-search', function(event) {
      event.preventDefault();
      $("body").addClass('search-active');
    });
    $(".search-popup-bg").on('click', function(event) {
      $("body").removeClass('search-active');
    });

              // redes sociais
              // facebook
              (function(d, s, id) {
          var js, fjs = d.getElementsByTagName(s)[0];
          if (d.getElementById(id)) return;
          js = d.createElement(s); js.id = id;
          js.src = "//connect.facebook.net/pt_BR/sdk.js#xfbml=1&version=v2.5";
          fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
});