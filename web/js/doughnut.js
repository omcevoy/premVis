var myDuration = 600;
var firstTime = true;

var width = 960,
height = 500,
radius = Math.min(width, height) / 2;

var color = d3.scaleOrdinal(d3.schemeCategory20);

var pie = d3.pie().value(function(d) { return d.Value; }).sort(null);
var arc = d3.arc().innerRadius(radius-40).outerRadius(radius-20);
var svg = d3.select('#donut_chart')
  .append('svg')
  .attr('width', width)
  .attr('height', height)
  .append('g')
  .attr('transform', 'translate(' + (width / 2) + ',' + (height / 2) + ')');


d3.json("../payData.json",  function(error, data) {
   var paymentsByClub = Object.keys(data);
   var dropDown = d3.select("form").append("select").attr("name", "club-list").attr("id", "club-list");
   dropDown.on("change", change);

   var options = dropDown.selectAll("option")
                         .data(paymentsByClub)
                         .enter()
                         .append("option")
    options.text(function(d) {return d})
           .attr("value", function(d){return d})

    function formatData(data) {
        var newData = []
        var positions = ["goalkeepers", "defenders", "midfielders", "forwards"];
        positions.forEach((pos, index) => {
            var thisData = {
                "Name": pos,
                "Value": data[pos]
            }
            newData.push(thisData);
        })
        return newData;
    }

    function change() {
            var path = svg.select("path");
            var selectedClub = d3.select("#club-list").property("value")
            var selectedData = data[selectedClub];
            var cleanData = formatData(selectedData);

            var originalPath = path.data();
            
            var newPath = pie(cleanData);       
           if (originalPath.length == 0) {
                originalPath = newPath
            }

            if (!firstTime){ 
                path = path.data(newPath);
                path.transition()
                .duration(myDuration)
                .attrTween("d", arcTween)

                path.enter()
                    .append("path")
                    .each(function(d, i) {
                        var narc = findNeighborArc(i, originalPath, newPath, key);
                        if(narc) {          
                        this._current = narc;
                        this._previous = narc;
                        } else {          
                        this._current = newPath;
                        }
                    }) 
                    .attr("fill", function(d,i) { 
                        return color(d.data.Name)
                    })
                    .transition()
                    .duration(myDuration)
                    .attrTween("d", arcTween)
            
            
                path.exit()
                    .transition()
                    .duration(myDuration)
                    .attrTween("d", function(d, index) {
                        var currentIndex = this._previous.data.region;
                        var i = d3.interpolateObject(d,this._previous);
                        return function(t) {
                            return arc(i(t))
                        }
                
                    })
                    .remove()    
                }
                else {
                    path = path.data(newPath)
                               .enter()
                               .append('path')
                               .attr('d', arc)
                               .attr("fill", function(d,i) { 
                                return color(d.data.Name)
                            })
                            .remove();
                }
                
            firstTime = false;
         }
});
function key(d) {
    return d.data.Name;
 }

 function findNeighborArc(i, data0, data1, key) {
   var d;
   if(d = findPreceding(i, data0, data1, key)) {
     var obj = cloneObj(d)
     obj.startAngle = d.endAngle;
     return obj;

   } else if(d = findFollowing(i, data0, data1, key)) {

     var obj = cloneObj(d)
     obj.endAngle = d.startAngle;
     return obj;

   }
   return null


 }

// Find the element in data0 that joins the highest preceding element in data1.
function findPreceding(i, data0, data1, key) {
    console.log('Data 0: ', data0);
    console.log('Data 1: ', data1);
 var m = data0.length;
 while (--i >= 0) {
   var k = key(data1[i]);
   console.log('K ', k);
   for (var j = 0; j < m; ++j) {
     console.log(data0[j]);
     if (key(data0[j]) === k) return data0[j];
   }
 }
}

// Find the element in data0 that joins the lowest following element in data1.
function findFollowing(i, data0, data1, key) {
 var n = data1.length, m = data0.length;
 while (++i < n) {
   var k = key(data1[i]);
   for (var j = 0; j < m; ++j) {
     console.log(data0[j])
     if (key(data0[j]) === k) return data0[j];
   }
 }
}

function arcTween(d) {
   var i = d3.interpolate(this._current, d);

 this._current = i(0);

 return function(t) {
   return arc(i(t))
 }

}


function cloneObj(obj) {
 var o = {};
 for(var i in obj) {
   o[i] = obj[i];
 }
 console.log(o);
 return o;
}