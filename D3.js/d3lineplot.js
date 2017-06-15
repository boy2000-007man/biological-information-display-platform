var d3lineplot = function(ahref, path, filename, extension) {
d3.dsv("	", "text/plain")(path+filename+extension, function(error, csv) {
    var ideal = {width: 800, height: 400};
    var margin = {top: 20, right: 20, bottom: 50, left: 80},
    width = ideal.width - margin.left - margin.right,
    height = ideal.height - margin.top - margin.bottom;
    
    var template = [];
    for (key in csv[0])
        template.push(key);
    template[0] = template[0].substr(1);
    var color = ["black", "red"];
    var data = [];
    csv.forEach(function(d) {
        tmp = [d["#"+template[0]]];
        for (var i = 1; i < template.length; i++)
            tmp.push(d[template[i]]);
        data.push(tmp);
    });
    
    var graph = d3.select(ahref)
    .append("svg")
        .attr("viewBox", "0 0 "+ideal.width+" "+ideal.height)
        .style("font-family", "Helvetica Neue, Helvetica, Arial, sans-serif")
    .append("g")
        .attr("class", "graph")
        .attr("transform", "translate("+margin.left+","+margin.top+")");
    
    var x_length = Math.ceil(d3.max(data, function(d) { return +d[0]; })-d3.min(data, function(d) { return +d[0]; }));
    var x_distance = width/x_length;
    var x = d3.scale.linear()
        .domain([d3.min(data, function(d) { return +d[0]; }), d3.max(data, function(d) { return +d[0]; })])
        .range([0, width-x_distance]);
    var y = d3.scale.linear()
        .domain([0, d3.max(data, function(d) { return +d[1]; })])
        .range([height, 0]);
        
    var xAxis = d3.svg.axis()
        .scale(x)
        .orient('bottom')
        .tickSize(0)
        .ticks(x_length);
    var yAxis = d3.svg.axis()
        .scale(y)
        .orient('left')
        .tickSize(0);
    
    graph.append("rect")
        .attr("class", "background")
        .attr("x", 0)
        .attr("y", 0)
        .attr("width", width)
        .attr("height", height)
	    .style("fill-opacity","0")
	    .style("stroke-width",0);
	    
    graph.append('g')
        .attr('class', 'x-axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis)
    .select("path.domain")
        .attr("d", "M0,0H"+width)
        .style("stroke", "black");
        
    graph.select("g.x-axis").selectAll("text")
        .style("text-anchor", "end")
        .attr("x", x_distance/2)
        .attr("y", x_distance/2)
        .attr("transform", "rotate(-45)");
    
    graph.select("g.x-axis").selectAll("g.tick")
        .each(function(d, i) {
            if (i % 2 == 1)
                d3.select(this)
                .append("rect")
                    .attr("x", 0)
                    .attr("y", -height)
                    .attr("width", x_distance)
                    .attr("height", height)
                    .style("fill","grey")
	                .style("fill-opacity","0.3")
	                .style("stroke-width",0);
        });
        
    graph.append('g')
        .attr('class', 'y-axis')
        .attr('transform', 'translate(0,0)')
        .call(yAxis)
    .select("path.domain")
        .style("stroke", "black");
    graph.select("g.y-axis").selectAll("g.tick")
        .each(function(d, i) {
            if (i != 0)
                d3.select(this)
                .append("line")
                    .attr("class", "level")
                    .attr("x1", 0)
                    .attr("y1", 0)
                    .attr("x2", width)
                    .attr("y2", 0)
                    .attr("stroke", "grey")
                    .attr("stroke-opacity", "0.3")
                    .attr("stroke-width", 1);
        });

    var label_width = 160, label_right = 2, label_top = 4;
	var label = graph.append("g")
	    .attr("class", "labels");
	label.append("rect")
	    .attr("class", "labels")
	    .attr("x", width-label_width)
        .attr("y", 0)
        .attr("width", label_width)
        .attr("height", 20)
        .style("fill","white")
        .style("stroke","grey")
	    .style("stroke-width",1);
	label.append("text")
	    .attr("class", "labels")
	    .style("text-anchor", "end")
        .attr("x", width-label_right)
        .attr("y", 20-label_top)
        .style("fill", "red")
        .text("Average Quality per read");
        
    var line = d3.svg.line()
        .x(function(d) { return x(d[0])+x_distance/2; })
        .y(function(d) { return y(d[1]); })
        .interpolate('monotone');
        
    graph.append('path')
        .attr('class', 'line')
        .attr('d', line(data))
        .style("fill", "none")
        .style("stroke", color[1]);
  
    graph.selectAll('circle')
        .data(data)
        .enter()
    .append('circle')
        .attr('class', 'line')
        .attr('cx', line.x())
        .attr('cy', line.y())
        .attr('r', 1.5)
        .style("fill", color[1])
        .style("stroke-width", 0);
        
    graph.append("g")
        .attr("class", "title")
        .attr("transform", "translate("+(ideal.width/2-margin.left)+",-5)")
    .append("text")
        .text("Quality score distribution over all sequences")
        .style("font-size", "125%")
        .style("text-anchor", "middle");
    graph.append("g")
        .attr("class", "title")
        .attr("transform", "translate("+(ideal.width/2-margin.left)+","+(ideal.height-margin.top-5)+")")
    .append("text")
        .text("Mean Sequence Quality (Phred Score)")
        .style("font-size", "125%")
        .style("text-anchor", "middle");
        
    var tip_margin = {left: 2, top: 2};
    var tip = graph.append('g')
        .attr('class', 'tip')
        .attr("transform", "translate("+tip_margin.left+","+(tip_margin.top+12)+")");
    
    tip.selectAll("text.tip")
        .data(template)
        .enter()
    .append("text")
        .attr("class", "tip")
        .each(function(d, i) {
            d3.select(this)
                .attr("y", 20*i)
                .style("fill", color[i]);
        });
        
    graph
        .on('mousemove', function() {
            var m = d3.mouse(this);

            var distance = function(x1, y1, x2, y2) {
                return Math.sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2));
            }
            var index = 0;
            for (var i = 1; i < data.length; i++)
                if (distance(m[0], m[1], x(data[i][0])+x_distance/2, y(data[i][1]))
                    < distance(m[0], m[1], x(data[index][0])+x_distance/2, y(data[index][1])))
                    index = i;
            if (x_distance/2 <= distance(m[0], m[1], x(data[index][0])+x_distance/2, y(data[index][1])))
                tip.selectAll("text.tip")
                    .text("");
            else
                tip.selectAll("text.tip")
                    .text(function(d, i) { return d+": "+data[index][i]; });
        })
        .on('mouseout', function() {
            tip.selectAll("text.tip")
                .text("");
        });

    var html = d3.select(ahref).select("svg")
        .attr("title", filename+".svg")
        .attr("version", 1.1)
        .attr("xmlns", "http://www.w3.org/2000/svg")
        .node().parentNode.innerHTML;

    d3.select(ahref)
        .attr("href", "data:image/svg+xml;base64,"+btoa(html))
        .attr("download", filename+".svg");
});
}
