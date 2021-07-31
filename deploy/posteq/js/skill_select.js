// 選択されたスキルの数
function NumCheckedSkill() {
  var num = 0
  $("#children").find("input").each(function() {
    if ($(this).prop('checked')) {
      num = num + 1
    }
  });
  $("#num_selected_skill").text(num);
}
// スキル選択の解除
function DelSkill(id, kid) {
  //スキルのチェック外す
  var targ = document.getElementById(id);
  $(targ).css('display', 'none');
  //スキル系列のチェックを外す
  var ktarg = document.getElementById(kid);
  $(ktarg).prop('checked', false);
  NumCheckedSkill();
}
$(function () {
  // 読み込み時処理
  // 選択されたスキル系列の表示
  $(".skill_type_select").each(function() {
    // console.log($(this).prop("checked"));
    if ($(this).prop("checked")) {
      var skill_type = $(this).val();
      $("#children").find('ol').each(function() {
        var val = $(this).data('val');
        if (skill_type != val) {
          $(this).css('display', 'none');
        } else {
          $(this).css('display', 'flex');
        }
      });
    }
  });
  // 選択されたスキルの表示
  $("#children").find('input').each(function() {
    var val = $(this).prop('checked'); //スキル種別
    var id = $(this).attr("id");
    if (val) { //スキル種別にチェックが入っているかどうか
      $("#checked_skill_"+id).css('display', 'flex');
    }
  });
  NumCheckedSkill();
});
$(function() {
  // 変更時処理
  // 選択されたスキル系列の表示
  $(".skill_type_select").change(function() {
    var skill_type = $(this).val();
    $("#children").find('ol').each(function() {
      var val = $(this).data('val');
      if (skill_type != val) {
        $(this).css('display', 'none');
      } else {
        $(this).css('display', 'flex');
      }
    });
  });

    $('input').change(function() {
      $("#children").find('input').each(function() {
        var val = $(this).prop('checked'); //スキル種別
        var id = $(this).attr("id");
        if (val) { //スキル種別にチェックが入っているかどうか
          $("#checked_skill_"+id).css('display', 'flex');
        } else {
          //非表示、選択も解除
          var targ = document.getElementById("#checked_skill_"+id);
          $("#checked_skill_"+id).css('display', 'none');
        }
      });
      NumCheckedSkill();
    })
  });

  // 検索条件追加
  $(function() {
    var i=1;
    $("#add_btn").click(function() {
      var info_element = document.getElementById("info");
      i++;
      var clone = info_element.cloneNode(true);
      clone.id = "info"
      $("#additional_info").append(clone);
    });
  });
