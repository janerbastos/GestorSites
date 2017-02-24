$(".nano").nanoScroller();

// Busca
$("#topo").on('click', '.btn-search', function(event) {
          event.preventDefault();
          $("body").addClass('search-active');
        });

$(".search-popup-bg").on('click', function(event) {
          $("body").removeClass('search-active');
        });

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
        $("body").animate({'font-size' : '10px'});
      });
