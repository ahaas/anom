d3.json("/api/data", function(err, data) {
  nv.addGraph(function() {
    var chart = nv.models.lineWithFocusChart();
    chart.xAxis.tickFormat(d3.format(',f'));
    chart.x2Axis.tickFormat(d3.format(',f'));
    chart.yAxis.tickFormat(d3.format(',.2f'));
    chart.y2Axis.tickFormat(d3.format(',.2f'));
    d3.select('#chart svg')
      .datum(testData())
      .call(chart);
    nv.utils.windowResize(chart.update);
    return chart;
  });
  function testData() {
    // list of objects with strKey, area?, and values
    out = []
    _.each(data, function(val) {
      out.push(val);
    })
    OUT = out
    return out
    return [{key: 'stream1', values: [{x:30,y:1}, {x:31,y:2}, {x:32, y:5}]}]

    return stream_layers(3,128,.1).map(function(data, i) {
      return {
        key: 'Stream' + i,
        area: i === 1,
        values: data
      };
    });
  }
})
