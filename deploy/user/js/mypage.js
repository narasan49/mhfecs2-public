function DrawBarChart(id, label, data) {
  var ctx = document.getElementById(id).getContext('2d');
  ctx.canvas.height = 450;
  var myChart = new Chart(ctx, {
    type: 'horizontalBar',
    data: {
      labels: label,
      datasets: [{
        data: data,
        backgroundColor: "rgba(153,255,51,0.4)"
      }]
    },
    options: {
      maintainAspectRatio: false,
       legend: {
          display: false
       }
    }
  });
}

$(function() {
  data = $("#chart_data").val().replace("[","").replace("]","").split(",").map( str => parseInt(str, 10) );
  // console.log(data);
  labels_short = $("#chart_labels_short").val().replace(/ /g,"").replace(/'/g,"").replace("[","").replace("]","").split(",");
  labels = $("#chart_labels").val().replace(/ /g,"").replace(/'/g,"").replace("[","").replace("]","").split(",");
  // console.log(labels);
  DrawBarChart('chart', labels, data);
  DrawBarChart('chart_short', labels_short, data);
});

$(function() {
  $('#u_follow').click(function() {
    var a = $(this);
    $.ajax({
        'url': a.prop("href"),
        'type': "GET",
        'timeout': 10000,
        'dataType': "json",
    })
    .done(function(data) {
      $('#u_follow').text(data.text);
    })
    .fail(function() {
      alert("失敗しました");
    });
    return false;
  });
});
