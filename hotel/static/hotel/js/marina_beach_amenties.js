// add padding top to show content behind navbar
$("body").css("padding-top", $(".navbar").outerHeight() + "px");
$(document).ready(function () {
  $("#book-a-stay").removeClass("scrolled-down").addClass("scrolled-up");
  $("#left-arrow").removeClass("fade-in").addClass("fade-out");
});

function changeButtons() {
  scroll_top = $(this).scrollTop();
  if (scroll_top < last_scroll_top) {
    $("#book-a-stay").removeClass("scrolled-down").addClass("scrolled-up");
    $("#left-arrow").removeClass("fade-in").addClass("fade-out");
  } else {
    $("#book-a-stay").removeClass("scrolled-up").addClass("scrolled-down");
    $("#left-arrow").removeClass("fade-out").addClass("fade-in");
  }
  last_scroll_top = scroll_top;
}

// detect scroll top or down
if ($(".smart-scroll").length > 0) {
  // check if element exists
  var last_scroll_top = 0;
  $(window).on("scroll", changeButtons);
}

$("#left-arrow").click(() => {
  $("#book-a-stay").removeClass("scrolled-down").addClass("scrolled-up");
  $("#left-arrow").removeClass("fade-in").addClass("fade-out");
});
