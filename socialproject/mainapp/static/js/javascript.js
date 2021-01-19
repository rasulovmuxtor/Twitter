$(function () {
  $("textarea[maxlength]").bind('input propertychange', function () {
    var maxLength = $(this).attr('maxlength');
    if ($(this).val().length > maxLength) {
      $(this).val($(this).val().substring(0, maxLength));
    }
  })
});

function openForm() {
  document.getElementById("myForm").style.display = "block";
  document.getElementById("mobile-post").style.display = "none";
}

function closeForm() {
  document.getElementById("myForm").style.display = "none";
  document.getElementById("mobile-post").style.display = "block";
}