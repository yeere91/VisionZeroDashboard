console.log("main.js Loaded");

var dataURL = "http://localhost:5000/data"

var type = (function(global) {
    var cache = {};
    return function(obj) {
        var key;
        return obj === null ? 'null' // null
            : obj === global ? 'global' // window in browser or global in nodejs
            : (key = typeof obj) !== 'object' ? key // basic: string, boolean, number, undefined, function
            : obj.nodeType ? 'object' // DOM element
            : cache[key = ({}).toString.call(obj)] // cached. date, regexp, error, object, array, math
            || (cache[key] = key.slice(8, -1).toLowerCase()); // get XXXX from [object XXXX], and cache it
    };
}(this));

// set the dimensions and margins of the graph
var margin = {top: 20, right: 80, bottom: 20, left: 80},
    width = 1400 - margin.left - margin.right,
    height = 300 - margin.top - margin.bottom;

// Parse the date / time
var parseTime = d3.timeParse("%Y-%m-%d %H:%M:%S");

// Calculate the closest date for the tooltip functionality
var bisectDate = d3.bisector(function(d) { return d.date; }).right;

// Format of the date for the tooltip
formatDate = d3.timeFormat("%b-%d-%y");

// set the ranges
var xScale = d3.scaleTime().range([0, width]);
var yScale = d3.scaleLinear().range([height, 0]);

// append the svg obgect to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

// Define the line
var valueline = d3.line()
    .x(function(d) { return xScale(d.date); })
    .y(function(d) { return yScale(d.count); });

// Define the tooltip
var lineSvg = svg.append("g"); 

var focus = svg.append("g")
    .style("display", "none"); 

// Get the data
d3.json(dataURL, function(error, data) {
  if (error) throw error;

  // format the data
  data.forEach(function(d) {
      d.date = parseTime(d.date);
      d.count = +d.count;
  });

  // Scale the range of the data
  xScale.domain(d3.extent(data, function(d) { return d.date; }));
  yScale.domain([0, d3.max(data, function(d) { return d.count; })]);

  // Add the valueline path.
  lineSvg.append("path")
      .data([data])
      .attr("class", "line")
      .attr("d", valueline(data));

  // Add the X Axis
  svg.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(xScale));

  // Add the Y Axis
  svg.append("g")
      .call(d3.axisLeft(yScale));
 
  // Append the x line
    focus.append("line")
        .attr("class", "x")
        .style("stroke", "blue")
        .style("stroke-dasharray", "3,3")
        .style("opacity", 0.5)
        .attr("y1", 0)
        .attr("y2", height);

    // Append the y line
    focus.append("line")
        .attr("class", "y")
        .style("stroke", "blue")
        .style("stroke-dasharray", "3,3")
        .style("opacity", 0.5)
        .attr("x1", width)
        .attr("x2", width);

    // Append the circle at the intersection
    focus.append("circle")
        .attr("class", "y")
        .style("fill", "none")
        .style("stroke", "blue")
        .attr("r", 4);

    // Place the value at the intersection
    focus.append("text")
        .attr("class", "y1")
        .style("stroke", "white")
        .style("stroke-width", "3.5px")
        .style("opacity", 0.8)
        .attr("dx", 8)
        .attr("dy", "-.3em");

    focus.append("text")
        .attr("class", "y2")
        .attr("dx", 8)
        .attr("dy", "-.3em");

    // Place the date at the intersection
    focus.append("text")
        .attr("class", "y3")
        .style("stroke", "white")
        .style("stroke-width", "3.5px")
        .style("opacity", 0.8)
        .attr("dx", 8)
        .attr("dy", "1em");

    focus.append("text")
        .attr("class", "y4")
        .attr("dx", 8)
        .attr("dy", "1em"); 

    // Append a rectangle to capture mouse events.
    svg.append("rect")
        .attr("width", width)
        .attr("height", height)
        .style("fill", "none")
        .style("pointer-events", "all")
        .on("mouseover", function() { focus.style("display", null); })
        .on("mouseout", function() { focus.style("display", "none"); })
        .on("mousemove", mousemove);

    function mousemove() {
        var x0 = xScale.invert(d3.mouse(this)[0]),
            i = bisectDate(data, x0, 1),
            d0 = data[i - 1],
            d1 = data[i],
            d = x0 - d0.date > d1.date - x0 ? d1 : d0;

        focus.select("circle.y")
            .attr("transform",
                  "translate(" + xScale(d.date) + "," +
                                 yScale(d.count) + ")"); 

        focus.select("text.y1")
            .attr("transform",
                  "translate(" + xScale(d.date) + "," +
                                 yScale(d.count) + ")")
            .text(d.count);

        focus.select("text.y2")
            .attr("transform",
                  "translate(" + xScale(d.date) + "," +
                                 yScale(d.count) + ")")
            .text(d.count);

        focus.select("text.y3")
            .attr("transform",
                  "translate(" + xScale(d.date) + "," +
                                 yScale(d.count) + ")")
            .text(formatDate(d.date));

        focus.select("text.y4")
            .attr("transform",
                  "translate(" + xScale(d.date) + "," +
                                 yScale(d.count) + ")")
            .text(formatDate(d.date));

        focus.select(".x")
            .attr("transform",
                  "translate(" + xScale(d.date) + "," +
                                 yScale(d.count) + ")")
                       .attr("y2", height - yScale(d.count));

        focus.select(".y")
            .attr("transform",
                  "translate(" + width * -1 + "," +
                                 yScale(d.count) + ")")
                       .attr("x2", width + width);
    }

});

