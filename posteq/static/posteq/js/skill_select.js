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
function DelSkill(id) {
  if (document.getElementById("checked_skill_"+id) != null) {
    //スキルのチェック外す
    var targ = document.getElementById("checked_skill_"+id);
    // $(targ).css('display', 'none');
    $(targ).remove();
    //スキル系列のチェックを外す
    var ktarg = document.getElementById(id);
    $(ktarg).prop('checked', false);
    NumCheckedSkill();
  }
}

function DelActiveSkillSelect(id) {
  if (document.getElementById("select_active_skill") != null) {
    //スキルのチェック外す
    var targ = document.getElementById("select_active_skill_"+id);
    $(targ).find("input").each(function() {
      $(this).prop("checked", false);
    });
    $(targ).css('display', 'none');

    // $(targ).remove();
    //スキル系列のチェックを外す
    var ktarg = document.getElementById(id);
    $(ktarg).prop('checked', false);
    NumCheckedSkill();
  }
}
// 選択されたスキルを表示
function CreateElementSelectedSkill(id) {
  if (document.getElementById("checked_skill_"+id) == null) {
    var selected_skill = document.createElement("li");
    var label = document.createElement("label");
    var b = document.createElement("b");
    var button = document.createElement("button");
    var span = document.createElement("span");
    selected_skill.classList.add("breadcrumb-item");
    selected_skill.id = "checked_skill_"+id;
    b.textContent = id;
    button.type = "button";
    button.classList.add("close");
    button.onclick = function(){DelSkill(id);};
    $(button).attr("aria-label", "取り消し");
    $(span).attr("aria-hidden", true);
    span.textContent = "×";
    button.appendChild(span);
    label.appendChild(b);
    label.appendChild(button);
    selected_skill.appendChild(label);
    document.getElementById("selected_skills").appendChild(selected_skill);
  }
}

// スキル系列から発動スキルの選択欄も含めて追加
function CreateElementActiveSkillSelect(id) {
  $("#select_active_skill_"+id).css('display', 'flex');
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
      // $("#checked_skill_"+id).css('display', 'flex');
      if (document.getElementById("select_active_skill") != null) {
        CreateElementActiveSkillSelect(id);
      } else {
        CreateElementSelectedSkill(id);
      }
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
          if (document.getElementById("select_active_skill") != null ) {
            CreateElementActiveSkillSelect(id);
          } else {
            CreateElementSelectedSkill(id);
          }
          // $("#checked_skill_"+id).css('display', 'flex');
        } else {
          //非表示、選択も解除
          // var targ = document.getElementById("#checked_skill_"+id);
          DelSkill(id);
          DelActiveSkillSelect(id);
          // $("#checked_skill_"+id).css('display', 'none');
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
