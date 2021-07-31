$(function () {
  $("#logout").click(function() {
    document.cookie = "gerogero=; path=/; max-age=0";
    document.cookie = "uso=; path=/; max-age=0";
  });
});
