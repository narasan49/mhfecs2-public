$(function() {
  $('.follow').click(function() {
    var a = $(this);
    $.ajax({
        'url': a.prop("href"),
        'type': "GET",
        'timeout': 10000,
        'dataType': "json",
    })
    .done(function(data) {
      $('#follow'+data.id).text(data.text);
    })
    .fail(function() {
      alert("失敗しました");
    });
    return false;
  });
});
