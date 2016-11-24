var width = 960;
var height = 960;

var projection = d3.geo.orthographic()
    .scale(width / 2 - 20)
    .translate([width / 2, height / 2])
    .clipAngle(90);

var graticule = d3.geo.graticule();

var path = d3.geo.path()
    .projection(projection);

var svg = d3.select('body').append('svg')
    .datum(graticule.outline)
    .attr('width', width)
    .attr('height', height);

svg.append("svg:circle")
    .attr('cx', width / 2)
    .attr('cy', height / 2)
    .attr('r', projection.scale())
    .attr('class', 'sea');

var tooltip = d3.select('body').append('div')
    .attr('class', 'hidden tooltip');

queue()
    .defer(d3.json, 'world.json')
    .defer(d3.tsv, 'world-country-names.tsv')
    .defer(d3.json, 'out.json')
    .await(ready);

function ready(error, world, names, data) {
    if (error) {
        throw error;
    };

    var countries = topojson.feature(world, world.objects.countries).features;

    // name the countries
    countries = countries.filter(function(d) {
        return names.some(function(n) {
            if (d.id == n.id) return d.name = n.name;
        });
    });

    // add exchange data to countries
    for (var i in countries) {
        var country = countries[i];
        if (country.id in data) {
            country.data = data[country.id];
        };
    }

    svg.selectAll('.country')
        .data(countries)
        .enter()
        .append('path')
        .attr('class', function(d) {
            if (d.data != null) {
                if (d.data.number <= 100) {
                    return 'country level1';
                } else if (d.data.number <= 500) {
                    return 'country level2';
                } else if (d.data.number <= 1000) {
                    return 'country level3';
                } else {
                    return 'country level4';
                }
            } else {
                return 'country';
            }
        })
        .attr('d', path)
        .on('mouseover', function(d) {
            d3.select(this).classed('hover', true);

            // tooltip content
            var studentNumber = 0;
            if (d.data != null)
                studentNumber = d.data.number;

            var message = d.name + '<br>Total exchange numbers: ' + studentNumber + '<br>';
            if (d.data != null) {
                var school = d.data.school;
                for (var i = 0; i < 3; i++) {
                    if (school.length > i) {
                        message += school[i][0] + ': ' + school[i][1] + '<br>';
                    } else {
                        break;
                    }
                }
            }

            // get the mouse location
            var mouse = d3.mouse(svg.node()).map(function(d) {
                return parseInt(d);
            });

            tooltip.classed('hidden', false)
            .attr('style', 'left:' + (mouse[0] + 15) +
                    'px; top:' + (mouse[1] - 35) + 'px')
            .html(message);
        })
        .on('mouseout', function() {
            d3.select(this).classed('hover', false);
            tooltip.classed('hidden', true);
        });

    svg.call(
        d3.behavior.drag().origin(function() {
            r = projection.rotate();
            return {x: r[0], y: -r[1]};
        })
        .on('drag', function() {
            rotate = projection.rotate();
            projection.rotate([d3.event.x, -d3.event.y, rotate[2]]);
            svg.selectAll('path').attr('d', path);
        })
    );
}

