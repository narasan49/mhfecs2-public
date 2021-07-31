$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

$(function() {
  $('.iine').click(function(event) {
    event.preventDefault();
    var a = $(this);
    $.ajax({
      url: a.prop("href"),
      type: "GET",
      timeout: 10000,
      dataType: "json",
    })
    .done(function(data) {
      // console.log('iine='+data.cookie_to_be_set+"; max-age="+data.max_age);
      $("#Niine"+data.id).text(data.res_good);
      document.cookie = 'iine='+data.cookie_to_be_set+"; path=/; max-age="+data.max_age;
    })
    .fail(function() {
      alert("失敗しました");
    });
  });
});

$(function() {
  $('.saveeq').submit(function(event) {
    event.preventDefault();
    var form = $(this);
    $.ajax({
        'url': form.prop("action"),
        'method': form.prop("method"),
        'data': form.serialize(),
        'timeout': 10000,
        'dataType': "json",
    })
    .done(function(data) {
        var alt_text=data.alt_text;
        var src_text=data.src_text;
        // console.log("a")
        $('#save_icon'+data.id).attr('src', src_text);
        $('#save_icon'+data.id).attr('alt', alt_text);
        $('#save_icon'+data.id).attr('title', alt_text);
      })
    .fail(function() {
      alert("保存に失敗しました");
    });
  });
});

$(function() {
  $('.save_clip').submit(function(event) {
    event.preventDefault();
    var form = $(this);
    $.ajax({
        'url': form.prop("action"),
        'method': form.prop("method"),
        'data': form.serialize(),
        'timeout': 10000,
        'dataType': "json",
    })
    .done(function(data) {
        var eq = document.getElementById("card"+data.id);
        var res_text=data.res_text;
        // console.log(res_text);
        var targ = document.createElement("textarea");
        $(targ).css({
          "left": "-9999px",
          "position": "absolute",
        });
        targ.textContent = res_text;
        $(eq).parent().append(targ);
        targ.select();
        document.execCommand("copy");
        $(targ).remove();
      })
    .fail(function() {
      alert("保存に失敗しました");
    });
  });
});
