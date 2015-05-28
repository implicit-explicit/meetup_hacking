var groups = {};
var venn_groups = [];

function k_combinations(set, k) {
    var i, j, combs, head, tailcombs;

    if (k > set.length || k <= 0) {
        return [];
    }

    if (k == set.length) {
        return [set];
    }

    if (k == 1) {
        combs = [];
        for (i = 0; i < set.length; i++) {
            combs.push([set[i]]);
        }
        return combs;
    }

    // Assert {1 < k < set.length}

    combs = [];
    for (i = 0; i < set.length - k + 1; i++) {
        head = set.slice(i, i+1);
        tailcombs = k_combinations(set.slice(i + 1), k - 1);
        for (j = 0; j < tailcombs.length; j++) {
            combs.push(head.concat(tailcombs[j]));
        }
    }
    return combs;
}

function combinations(set) {
    var k, i, combs, k_combs;
    combs = [];

    // Calculate all non-empty k-combinations
    for (k = 1; k <= set.length; k++) {
        k_combs = k_combinations(set, k);
        for (i = 0; i < k_combs.length; i++) {
            combs.push(k_combs[i]);
        }
    }
    return combs;
}

function load_single_group(json) {
  var members = [];
  $.each(json, function( key, val ) {
      members.push( {x: parseInt(key, 10), y: val }  );
  });
  return members
}

var graph = null;

function init_graph() {

    console.log("Initializing graph");

    var series = [];

    var graph = new Rickshaw.Graph( {
        element: document.querySelector("#chart"),
        width: 540,
        height: 240,
        renderer: 'line',
        series: series
    } );

    graph.palette = new Rickshaw.Color.Palette();

    var x_axis = new Rickshaw.Graph.Axis.Time( { graph: graph } );

    var y_axis = new Rickshaw.Graph.Axis.Y( {
        graph: graph,
        orientation: 'left',
        tickFormat: Rickshaw.Fixtures.Number.formatKMBT,
        element: document.getElementById('y_axis'),
    } );

    graph.legend = new Rickshaw.Graph.Legend( {
        element: document.querySelector('#legend'),
        graph: graph
    } );


    return graph;
}

function plot_meetups(err, name, data) {

    console.log("Plotting graph for " + name);

    if (graph == null) {
        graph = init_graph();
    }

    var group_series = {
        name: name,
        data: data,
        color: graph.palette.color()
    };

    graph.series.push(group_series);
    graph.legend.addLine(group_series);

    graph.render();
}

function common_members(group_names) {
    var ids = [];
    for (var i = 0; i < group_names.length; i++) {
        ids.push(groups[group_names[i]]['ids']);
    }

    var result = ids.shift().filter(function(v) {
        return ids.every(function(a) {
            return a.indexOf(v) !== -1;
        });
    });

    return result

}

function plot_venn(name, data) {

    var venn_sets = [];

    venn_groups.push(name);
    var combs = combinations(venn_groups);
    for (var i = 0; i < combs.length; i++){
        if (combs[i].length < 2) {
            var group_name = combs[i][0];
            venn_sets.push({sets: combs[i], label: group_name, size: groups[group_name]['ids'].length})
        } else {
            var intersection = common_members(combs[i]);
            venn_sets.push({sets: combs[i], size: intersection.length})
        }
    }

    console.log('Adding ' + name + ' to the venn diagram');

    var chart = venn.VennDiagram();
    d3.select("#venn_container").datum(venn_sets).call(chart);
}

$("#meetup_form").submit(function (e) {

    e.preventDefault();
    var form_data = $("#meetup_form").serialize();
    var values = {};
    $.each($('#meetup_form').serializeArray(), function(i, field) {
        values[field.name] = field.value;
    });
    var name = values['name'];

    console.log("Getting data for " + name);

    $.ajax({
        url: '/meetup',
        type: 'get',
        data:  form_data,
        success: function (data) {
            var group_data = JSON.parse(data);
            console.log("Received data for " + name);
            groups[name] = group_data;
            plot_meetups(null, values['name'], load_single_group(group_data['membership']));
            plot_venn(values['name'], group_data);
        }
    });
});