function NarrowDownChange(partID, partSlideID, partSlideValID) {
  var current_num = $(partSlideID).val();
  $(partSlideValID).text(current_num)[0];
  $(partID).find("div").each(function() {
    if (String($(this).find("input").data("num")) === current_num) {
      $(this).css('display', 'flex');
    } else {
      $(this).css('display', 'none');
    }
  });
}
function NarrowDown(partID, partSlideID, partSlideValID) {
  $(partSlideID).on('change', function() {
    NarrowDownChange(partID, partSlideID, partSlideValID);
  });
}
$(function() {
  NarrowDown("#wep_queried"  , "#wepSlide"  , "#wepSlideVal");
  NarrowDown("#head_queried" , "#headSlide" , "#headSlideVal");
  NarrowDown("#body_queried" , "#bodySlide" , "#bodySlideVal");
  NarrowDown("#arm_queried"  , "#armSlide"  , "#armSlideVal");
  NarrowDown("#wst_queried"  , "#wstSlide"  , "#wstSlideVal");
  NarrowDown("#leg_queried"  , "#legSlide"  , "#legSlideVal");
  NarrowDown("#cuff_queried" , "#cuffSlide" , "#cuffSlideVal");
  NarrowDown("#jewel_queried", "#jewelSlide", "#jewelSlideVal");
});



// 装備検索のajax
$(function() {
  $('#skill_query').on('submit', function(event) {
    event.preventDefault(); // 本来のPOSTを打ち消すおまじない
    $("#send_query").prop("disabled", true);
    var form = $(this);
    $.ajax({
      url: form.attr('action'),
      type: form.attr('method'),
      data: form.serialize(),
      timeout: 10000,
      dataType: "json",
    })
    .done(function(data) {
      if ("data" in data) {
        var wep_kind = document.createElement("input");
        var uname = document.createElement("input");
        var form_second = document.getElementById("post_eq");
        // $(wep_kind).prop(, true);
        wep_kind.type="hidden";
        wep_kind.name="wep_kind";
        wep_kind.value=data.wep_kind;
        uname.type="hidden";
        uname.name="name";
        uname.value=data.name;
        // console.log(wep_kind);
        // console.log(form_second);

        form_second.prepend(wep_kind);
        $("#head_queried").empty();
        $("#body_queried").empty();
        $("#arm_queried").empty();
        $("#wst_queried").empty();
        $("#leg_queried").empty();
        $("#cuff_queried").empty();
        $("#jewel_queried").empty();
        for(var i=0;i<data.data.length;i++){
          var opt = document.createElement("input");
          var lbl = document.createElement("label");
          var div_rad = document.createElement("div");
          if (data.data[i][3] === "jewel" || data.data[i][3] === "cuff") {
            opt.type = "checkbox"
          } else {
            opt.type = "radio"
          }

          opt.value = data.data[i][1];  //防具名
          opt.id = data.data[i][3]+data.data[i][0];   //防具id
          opt.name = data.data[i][3]; //部位値
          opt.classList.add("form-check-input");
          opt.classList.add(data.data[i][3]);
          opt.classList.add("candidate_eqs");
          $(opt).attr('data-class', data.data[i][2]);
          $(opt).attr('data-num', data.data[i][4]);

          lbl.for = data.data[i][0];
          lbl.textContent = data.data[i][1];
          lbl.classList.add("form-check-label");

          div_rad.classList.add("form-check");
          document.getElementById(opt.name+"_queried").appendChild(div_rad);
          div_rad.appendChild(lbl);
          lbl.prepend(opt);
        }
        NarrowDownChange("#wep_queried", "#wepSlide", "#wepSlideVal");
        NarrowDownChange("#head_queried", "#headSlide", "#headSlideVal");
        NarrowDownChange("#body_queried", "#bodySlide", "#bodySlideVal");
        NarrowDownChange("#arm_queried", "#armSlide", "#armSlideVal");
        NarrowDownChange("#wst_queried", "#wstSlide", "#wstSlideVal");
        NarrowDownChange("#leg_queried", "#legSlide", "#legSlideVal");
        NarrowDownChange("#cuff_queried", "#cuffSlide", "#cuffSlideVal");
        NarrowDownChange("#jewel_queried", "#jewelSlide", "#jewelSlideVal");
        // console.log(data.time);
      } else {
        alert(data.mssg);
      }
    })
    .fail(function() {
      alert('データの取得に失敗しました');
    });
    $("#send_query").prop("disabled", false);
  });
});
// チェックした装備を表示する処理
// 処理が重いのでとりあえず保留
// function CheckedEQ(part) {
//   $(document).on("change", "#"+part+"_queried", function() {
//     $(this).find("input").each(function() {
//       if ($(this).prop("checked")) {
//         console.log($(this).prop("checked"));
//         var res = document.getElementById("list_selected_"+part);
//         var eq_name = $(this).val();
//         res.textContent =eq_name;
//       }
//     })
//   });
// }
// $(function() {
//   CheckedEQ("wep");
//   CheckedEQ("head");
// });

// 装飾品の増減指定
function ChangeJewelNum(num, id) {
  var input_num = document.getElementById(id);
  $(input_num).val(Number($(input_num).val())+num);
}
// xボタンの動作
function DelButton(part) {
  $(document).on("click", "."+part+"_close", function() {
    // ボタングループの削除
    $(this).parent().parent().parent().remove();
    // アイテムのチェックを外す
    var selected_id = $(this).data("num_id");
    var item_id = selected_id.slice("selected_".length);
    // console.log(item_id);
    $("#"+item_id).prop("checked", false);
  });
}
// ＋－ボタンのdisableを制御
function ButtonAvailabilityInc(maxval, part) {
  var val_sum = 0;
  $("#selected_"+part).find('input.form-control').each(function() {
    val_sum += Number($(this).val());
  });
  // console.log(val_sum);
  if (val_sum >= maxval) {
    $("#selected_"+part).find('input.'+part+'_inc').each(function() {
      $(this).prop("disabled", true);
      // 未選択の選択肢も無効化
      $("#"+part+"_queried").find('input.'+part).each(function() {
        if (! $(this).prop("checked")) {
          $(this).prop("disabled", true);
        }
      });
    });
  } else {
    $("#selected_"+part).find('input.'+part+'_inc').each(function() {
      $(this).prop("disabled", false);
      // 未選択の選択肢も有効化
      $("#"+part+"_queried").find('input.'+part).each(function() {
        $(this).prop("disabled", false);
      });
    });
  }
}
function ButtonAvailabilityDec(minval, part) {
  $("#selected_"+part).find('input.form-control').each(function() {
    if ($(this).val() <= 1) {

      $(this).parent().parent().find('input.'+part+'_dec').each(function() {
        $(this).prop("disabled", true);
      });
    } else {
      $(this).parent().parent().find('input.'+part+'_dec').each(function() {
        $(this).prop("disabled", false);
      });
    }
  });
}

// 装飾品やカフが上限値、下限値になるとボタンを無効化
// 未選択の選択肢も無効化
function ButtonControl(maxval, minval, part) {
  $(document).on("click", "."+part+"_inc", function() {
    ChangeJewelNum(1, $(this).data('num_id'));
    ButtonAvailabilityInc(maxval, part);
    ButtonAvailabilityDec(minval, part);
  });
  $(document).on("click", "."+part+"_dec", function() {
    ChangeJewelNum(-1, $(this).data('num_id'));
    ButtonAvailabilityInc(maxval, part);
    ButtonAvailabilityDec(minval, part);
  });
  $(document).on("click", "."+part+"_close", function() {
    ChangeJewelNum(-1, $(this).data('num_id'));
    ButtonAvailabilityInc(maxval, part);
    ButtonAvailabilityDec(minval, part);
  });
}
$(function() {
  ButtonControl(2, 1, "cuff");
  ButtonControl(18, 1, "jewel");
  $(document).on("change", "input.form-check-input", function() {
    ButtonAvailabilityInc(2, "cuff");
    ButtonAvailabilityDec(1, "cuff");
    ButtonAvailabilityInc(18, "jewel");
    ButtonAvailabilityDec(1, "jewel");
  });
  DelButton("cuff");
  DelButton("jewel");
});

function SelectedList(id, part) {
  // 選択した装飾品をリスト表示
  $("#"+id).on("change", function() {
    $(this).find("input").each(function() {
      selectedJ = document.getElementById("selected_"+$(this).prop("id"));
      if ($(this).prop("checked") && selectedJ == null) {
        var lst = document.createElement("li");
        lst.classList.add("list-group-item");
        lst.classList.add("p-0");
        var num = document.createElement("input");
        num.type = "number";
        num.value = 1;
        num.name = "num_"+$(this).val();
        num.id = "selected_"+$(this).prop("id");
        num.min = 1;
        num.classList.add("form-control");
        num.classList.add("px-0");
        $(num).prop("readonly", true);
        $(num).css("width", "2.5rem");
        // num.classList.add("col-sm-2");

        // インプットグループ
        // https://cccabinet.jpn.org/bootstrap4/components/button-group
        var input_group = document.createElement("div");
        var input_group_pre = document.createElement("div");
        var input_group_txt = document.createElement("div");
        input_group.classList.add("input-group");
        input_group_pre.classList.add("input-group-prepend");
        input_group_txt.classList.add("input-group-text");
        $(input_group_txt).text($(this).val());
        input_group_pre.append(input_group_txt);
        input_group.append(input_group_pre);
        input_group.append(num);

        // +-ボタン
        var btn_inc = document.createElement("input");
        var btn_dec = document.createElement("input");
        btn_inc.type="button";
        btn_inc.value="+";
        btn_inc.classList.add(part+"_inc");
        btn_inc.classList.add("btn");
        btn_inc.classList.add("btn-secondary");
        $(btn_inc).attr('data-num_id', num.id);
        btn_dec.type="button";
        btn_dec.value="-";
        btn_dec.classList.add(part+"_dec");
        btn_dec.classList.add("btn");
        btn_dec.classList.add("btn-secondary");
        $(btn_dec).attr('data-num_id', num.id);

        // xボタン
        var btn_close = document.createElement("input");
        var btn_groupx = document.createElement("div");
        btn_close.type = "button";
        btn_close.value = "×";
        btn_close.classList.add(part+"_close");
        btn_close.classList.add("btn");
        btn_close.classList.add("btn-danger");
        btn_close.classList.add("ml-2");
        $(btn_close).attr('data-num_id', num.id);

        // ボタングループにする
        var btn_toolbar = document.createElement("div");
        var btn_group1 = document.createElement("div");
        var btn_group2 = document.createElement("div");
        btn_toolbar.classList.add("btn-toolbar");
        btn_toolbar.role="toolbar"
        btn_group1.classList.add("btn-group");
        btn_group1.role="group"
        btn_group1.append(btn_inc);
        btn_group1.append(btn_dec);
        btn_group1.append(btn_close);
        btn_toolbar.append(btn_group1);

        document.getElementById("selected_"+part).appendChild(lst);
        btn_toolbar.prepend(input_group);
        lst.append(btn_toolbar);
      } else if ($(this).prop("checked") === false && selectedJ != null) {
        // 選択されていなければリストから削除
        $(selectedJ).parent().parent().parent().remove();
        // console.log("消去");
      }
    })
  });
}

$(function() {
  SelectedList("jewel_queried", "jewel");
  SelectedList("cuff_queried", "cuff");
});

$(function() {
  $('#post_eq').on('submit', function(event) {
    event.preventDefault(); // 本来のPOSTを打ち消すおまじない
    var form = $(this);
    var a = $.ajax({
      url: form.attr('action'),
      type: form.attr('method'),
      data: form.serialize(),
      timeout: 10000,
      dataType: "json",
    })
    .done(function(data) {
      alert(data.mssg);
    })
    .fail(function(data) {
      form2 = document.getElementById("post_eq");
      form2.id = "tmp_post_eq";
      form2.submit();
    });
  });
});
