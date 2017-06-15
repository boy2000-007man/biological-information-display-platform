var d3piechart = function(ahref, path, filename, extension) {
d3.dsv("	", "text/plain")(path+filename+extension, function(error, csv) {
    var ideal = {width: 1080, height: 540};
    var template = [];
    for (key in csv[0])
        template.push(key);
    var content = [];
    var sum = 0.0;
    csv.forEach(function(d) {
        sum += +d[template[1]];
        content.push({
            "label": d[template[0]],
            "value": +d[template[1]],
            "color": "#"+('00000'+(Math.random()*0x1000000<<0).toString(16)).slice(-6)
        });
    });
    var pie = new d3pie(ahref, {
	    "header": {
	    	"title": {
	    	    "text": template[1],
	    		"fontSize": 24,
	    		"font": "open sans"
	    	},
	    	"subtitle": {
	    		"text": filename+extension,
	    		"color": "#999999",
	    		"fontSize": 12,
	    		"font": "open sans"
	    	},
	    	"titleSubtitlePadding": 9
	    },
	    "footer": {
	    	"color": "#999999",
	    	"fontSize": 10,
	    	"font": "open sans",
	    	"location": "bottom-left"
	    },
	    "size": {
	    	"canvasWidth": ideal.width,
	    	"canvasHeight": ideal.height
	    },
	    "data": {
		    "sortOrder": "value-desc",
	    	"content": content
	    },
	    "labels": {
	    	"outer": {
	    		"format": "label-percentage1",
	    		"pieDistance": 32
	    	},
	    	"inner": {
	    		"format": "none",
	    		"hideWhenLessThanPercentage": 3
	    	},
	    	"mainLabel": {
	    		"color": "#000000",
	    		"fontSize": 11
	    	},
	    	"percentage": {
	    		"color": "#333333",
	    		"decimalPlaces": 0
	    	},
	    	"value": {
	    		"color": "#333333",
	    		"fontSize": 11
	    	},
	    	"lines": {
	    		"enabled": true
	    	}
	    },
	    "effects": {
	    	"pullOutSegmentOnClick": {
	    		"effect": "linear",
	    		"speed": 400,
	    		"size": 8
	    	}
	    },
	    "misc": {
	    	"gradient": {
	    		"enabled": true,
	    		"percentage": 100
	    	}
	    },
	    "callbacks": {
		    "onload": function() {
                var html = d3.select(ahref).select("svg")
                    .attr("title", filename+".svg")
                    .attr("version", 1.1)
                    .attr("xmlns", "http://www.w3.org/2000/svg")
                    .node().parentNode.innerHTML;

                d3.select(ahref)
                    .attr("href", "data:image/svg+xml;base64,"+btoa(html))
                    .attr("download", filename+".svg");
                    
                var tip = d3.select(ahref).select("svg").append('g')
                    .attr('class', 'tip')
                    .attr("transform", "translate(0,75)")
                    .style("font-weight", "bold")
                    .style("font-size", "100%");
    
                tip.append("text")
                    .attr("class", "lab")
                    .attr("y", 0);
                tip.append("text")
                    .attr("class", "val")
                    .attr("y", 20);
                tip.append("text")
                    .attr("class", "per")
                    .attr("y", 40)
                    .style("fill", "#999999");
            },
            "onMouseoverSegment": function(info) {
                var tip = d3.select(ahref).select("svg").select("g.tip");
                if (tip) {
                    tip.select("text.lab")
                        .text(template[0]+": "+info.data.label);
                    tip.select("text.val")
                        .text(template[1]+": "+info.data.value)
                        .style("fill", info.data.color);
                    tip.select("text.per")
                        .text("percentage: "+(info.data.value/sum*100).toFixed(2)+"%");
                }
            },
            "onMouseoutSegment": function(info) {
                var tip = d3.select(ahref).select("svg").select("g.tip");
                if (tip)
                    tip.selectAll("text")
                        .text("");
            }
        }
    });
    
    d3.select(ahref)
        .on("click", function() {
            if (!d3.event.defaultPrevented)
                d3.event.preventDefault();
        });
});
}
