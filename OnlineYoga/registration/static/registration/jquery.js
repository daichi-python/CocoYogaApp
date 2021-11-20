$(window).scroll(function() {
    var windowH = $(window).height(),
    scrollY = $(window).scrollTop(),
    elPosition = $('.fee-container').offset().top;
    if (scrollY > elPosition - windowH) {
      $('.fee-container').addClass("addSlideIn");
    }
});

$(window).scroll(function() {
    var windowH = $(window).height(),
    scrollY = $(window).scrollTop(),
    elPosition = $('.payment-container').offset().top;
    if (scrollY > elPosition - windowH) {
      $('.payment-container').addClass("addSlideInReverse");
    }
});

$(window).scroll(function() {
    var windowH = $(window).height(),
    scrollY = $(window).scrollTop(),
    elPosition = $('.detail-container').offset().top;
    if (scrollY > elPosition - windowH) {
      $('.detail-container').addClass("addSlideIn");
    }
});

$(window).scroll(function() {
  var windowH = $(window).height(),
  scrollY = $(window).scrollTop(),
  elPosition = $('.register').offset().top;
  if (scrollY > elPosition - windowH) {
    $('.register').addClass("addFadeSlideIn");
  }
});

$(window).scroll(function() {
  var windowH = $(window).height(),
  scrollY = $(window).scrollTop(),
  elPosition = $('.register-container').offset().top;
  if (scrollY > elPosition - windowH) {
    $('.register-container').addClass("addFadeSlideInReverse");
  }
});