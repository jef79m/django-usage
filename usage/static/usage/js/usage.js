(function($){

  function expandInfo(event) {
    var target = $("#"+this.dataset.target);
    if (target.hasClass("hide")) {
      target.removeClass('hide');
    } else {
      target.addClass('hide');
    }
  }

  $('.expandable_heading').click(expandInfo);


})(django.jQuery);
