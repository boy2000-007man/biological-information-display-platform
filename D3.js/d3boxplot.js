var d3boxplot = function(ahref, path, filename, extension) {
d3.dsv("	", "text/plain")(path+filename+extension, function(error, csv) {
    var ideal = {width: 800, height: 400};
    var margin = {top: 20, right: 20, bottom: 60, left: 20},
        width = ideal.width - margin.left - margin.right,
        height = ideal.height - margin.top - margin.bottom;
    
    var template = [];
    for (key in csv[0])
        template.push(key);
    template[0] = template[0].substr(1);
    var color = ["black", "blue", "red", "black", "black", "black", "black"];
    var data = [];
    csv.forEach(function(d) {
        tmp = [d["#"+template[0]]];
        for (var i = 1; i < template.length; i++)
            tmp.push(d[template[i]]);
        data.push(tmp);
    });
    
    var box = {margin: 2, width: width/data.length};
    var x_domain = [],
        x_range = [];
    for (var i = 0; i < data.length; i++) {
        x_domain.push(data[i][0]);
        x_range.push(i*box.width);
    }
    
    var x = d3.scale.ordinal()
        .domain(x_domain)
        .range(x_range);
    var y = d3.scale.linear()
        .domain([0, d3.max(data, function(d) { return +d[6]; })])
        .range([height, 0]);
    
    var graph = d3.select(ahref)
    .append("svg")
        .attr("viewBox", "0 0 "+ideal.width+" "+ideal.height)
        .style("font-family", "Helvetica Neue, Helvetica, Arial, sans-serif")
    .append("g")
        .attr("class", "graph")
        .attr("transform", "translate("+margin.left+","+margin.top+")");
    graph.append("g")
        .attr("class", "rects")
    .append("rect")
        .attr("x",0)
	    .attr("y",y(20))
	    .attr("width",width)
	    .attr("height",height-y(20))
	    .style("fill","pink")
	    .style("stroke-width",0);
	graph.select("g.rects")
	.append("rect")
        .attr("x",0)
	    .attr("y",y(28))
	    .attr("width",width)
	    .attr("height",y(20)-y(28))
	    .style("fill","orange")
	    .style("stroke-width",0);
	graph.select("g.rects")
	.append("rect")
        .attr("x",0)
	    .attr("y",0)
	    .attr("width",width)
	    .attr("height",y(28))
	    .style("fill","lightgreen")
	    .style("stroke-width",0);
	    
    var xAxis = d3.svg.axis()
        .scale(x)
        .tickSize(0)
        .orient('bottom');
    var yAxis = d3.svg.axis()
        .scale(y)
        .tickSize(0)
        .orient('left')
        .ticks(20);
    
    graph.append('g')
        .attr('class', 'x-axis')
        .attr('transform', 'translate(0,'+height+')')
        .call(xAxis)
    .select("path.domain")
        .attr("d", "M0,0H"+width)
        .style("stroke", "black");
    graph.select("g.x-axis").selectAll("g.tick")
        .each(function(d, i) {
            if (i % 2 == 1)
                d3.select(this)
                .append("rect")
                    .attr("x", 0)
                    .attr("y", -height)
                    .attr("width",box.width)
	                .attr("height",height)
	                .style("fill","white")
	                .style("fill-opacity","0.4")
	                .style("stroke-width",0);
        });
    graph.select("g.x-axis").selectAll("text")
        .style("text-anchor", "end")
        .attr("x", box.width/2)
        .attr("y", box.width/2)
        .attr("transform", "rotate(-45)");
    
    graph.append('g')
        .attr('class', 'y-axis')
        .attr('transform', 'translate(0,0)')
        .call(yAxis)
    .select("path.domain")
        .style("stroke", "black");
        
    graph.append("g")
        .attr("class", "boxes")
    .selectAll("g")
        .data(data)
        .enter()
    .append("g")
        .attr("transform", function(d) { return "translate("+x(d[0])+",0)"; })
        .each(function(d, i) {
            var g = d3.select(this);
	        
            g.selectAll("line.plumb")
                .data([[d[5], d[6]]])
                .enter()
            .append("line")
                .attr("class", "plumb")
                .attr("x1", box.width/2)
                .attr("y1", function(d) { return y(d[0]); })
                .attr("x2", box.width/2)
                .attr("y2", function(d) { return y(d[1]); })
                .style("stroke", color[5]);

            g.selectAll("rect.box")
                .data([[d[3], d[4]]])
                .enter()
            .append("rect")
                .attr("class", "box")
                .attr("x", box.margin)
                .attr("y", function(d) { return y(d[1]); })
                .attr("width", box.width-2*box.margin)
                .attr("height", function(d) { return y(d[0]) - y(d[1]); })
                .style("fill", "yellow")
                .style("stroke", color[3]);

            g.selectAll("line.level")
                .data([d[5], d[6]])
                .enter()
            .append("line")
                .attr("class", "level")
                .attr("x1", box.margin)
                .attr("y1", y)
                .attr("x2", box.width-box.margin)
                .attr("y2", y)
                .style("stroke", color[5]);

            g.selectAll("line.median")
                .data([d[2]])
                .enter()
            .append("line")
                .attr("class", "median")
                .attr("x1", box.margin)
                .attr("y1", y)
                .attr("x2", box.width-box.margin)
                .attr("y2", y)
                .style("stroke", color[2]);
        });
       
    var line = d3.svg.line()
        .x(function(d) { return x(d[0])+box.width/2; })
        .y(function(d) { return y(d[1]); })
        .interpolate('monotone');

    graph.append('path')
        .attr('class', 'line')
        .attr('d', line(data))
        .style("fill", "none")
        .style("stroke", color[1]);
        
    graph.append("g")
        .attr("class", "points")
    .selectAll('circle')
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
        .text("Quality scores across all bases (lllumina 1.5 encoding)")
        .style("font-size", "125%")
        .style("text-anchor", "middle");
    graph.append("g")
        .attr("class", "title")
        .attr("transform", "translate("+(ideal.width/2-margin.left)+","+(ideal.height-margin.top-5)+")")
    .append("text")
        .text("Position in read (bp)")
        .style("font-size", "125%")
        .style("text-anchor", "middle");
        
    var tip_margin = {left: 2, bottom: 2};
    var tip = graph.append('g')
        .attr('class', 'tip')
        .attr("transform", "translate("+tip_margin.left+","+(height-(template.length-1)*20-tip_margin.bottom)+")");
 
    tip.selectAll("text.tip")
        .data(template)
        .enter()
    .append("text")
        .attr('class', 'tip')
        .each(function(d, i) {
            d3.select(this)
                .attr('y', 20*i)
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
                if (distance(m[0], m[1], x(data[i][0])+box.width/2, y(data[i][1]))
                    < distance(m[0], m[1], x(data[index][0])+box.width/2, y(data[index][1])))
                    index = i;
            if (box.width/2 <= distance(m[0], m[1], x(data[index][0])+box.width/2, y(data[index][1])))
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
