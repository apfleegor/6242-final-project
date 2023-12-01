
// Function to draw interactive line chart
function drawInteractiveLineChart(gpas, semesters,prereqs, professors) {
    console.log("drawInteractiveLineChart called with data:", gpas);

    // Transform data
    let lowestGpa = 4;
    let highestGpa = 0;
    let courseData = [];
    Object.keys(gpas).forEach(course => {
        let maxGpa = d3.max(gpas[course][0]);
        let minGpa = d3.min(gpas[course][0]);
        gpas[course][0].forEach((gpa, semesterIndex) => {
            // let semesterIndex = index + 1;  // Adjust for zero-based indexing
            let professorName = professors[course] && professors[course][semesterIndex] ? professors[course][semesterIndex]  : "Unknown";
            lowestGpa = Math.min(lowestGpa, gpa);
            highestGpa = Math.max(highestGpa, gpa);
            courseData.push({ 
                course, 
                semester: semesterIndex + 1, 
                gpa, 
                professor : professorName,
                isMax: gpa === maxGpa,
                isMin: gpa === minGpa
            });
        });
    });


    // Group data by course
    let dataNest = d3.nest()
        .key(function(d) { return d.course; })
        .entries(courseData);

    // Dimensions and margins
    const margin = { top: 30, right: 50, bottom: 60, left: 50 };
    const width = 1100 - margin.left - margin.right;
    const height = 600 - margin.top - margin.bottom;

    // Remove existing SVG
    d3.select("#interactiveLineChart").selectAll("*").remove();

    // SVG container
    const svg = d3.select("#interactiveLineChart")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    // Tooltip
    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .style("visibility", "visible")
        .style("background", "grey")
        .offset([-10, 0])
        .html(function(d) {
            // tooltip contets
            // let maxGpa = d3.max(gpas[d.course][0]);
            // let minGpa = d3.min(gpas[d.course][0]);
            // let gpa = gpas[d.course][0][semesters[d.course] - 1];
            let maxGpa = d3.max(gpas[d.course][0]).toFixed(2);
            let minGpa = d3.min(gpas[d.course][0]).toFixed(2);
            let gpa = gpas[d.course][0][semesters[d.course] - 1].toFixed(2);
            // let gpa = gpa.toFixed(2);
            let prereqText = prereqs[d.course].length > 0 ? prereqs[d.course].join(", ") : "None";
            let professor = d.professor;
            return `Max GPA: ${maxGpa}<br>Min GPA: ${minGpa} <br> Model GPA: ${gpa} <br>Prereqs: ${prereqText} <br>Professor: ${professor}`;
        });

    svg.call(tip);

    // get max semester val
    const firstKey = Object.keys(gpas)[0];
    const maxSemester = gpas[firstKey][0].length;

    lowestGpa = Math.floor(lowestGpa * 10) / 10;
    highestGpa = Math.ceil(highestGpa * 10) / 10;
    highestGpa = Math.max(highestGpa, 4);


    // Scales
    const xScale = d3.scaleLinear().domain([1, maxSemester]).range([0, width]);
    const yScale = d3.scaleLinear().domain([lowestGpa, highestGpa]).range([height, 0]);

    // Colors
    const color = d3.scaleOrdinal(d3.schemeCategory10);

    // Add X and Y axis
    // Add X axis
    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(xScale)
        .tickFormat(d3.format('d')) // Format as integer
        .ticks(maxSemester) // Set the number of ticks to the maximum semester value
        .tickValues(d3.range(1, maxSemester + 1)) // Explicitly set tick values
    );

    svg.append("g").call(d3.axisLeft(yScale));

    // Line generator
    const line = d3.line()
        .x(d => xScale(d.semester))
        .y(d => yScale(d.gpa));

    // Draw the lines and squares for max GPA
    dataNest.forEach(function(d, i) {
        const group = svg.append("g").attr("class", "course-group");

        group.append("path")
            .data([d.values])
            .attr("class", "line")
            .style("stroke", function() { return color(d.key); })
            .style("stroke-width", "2px")
            .attr("fill", "none")
            .attr("d", line);

        // Draw triang for max GPA
        group.selectAll(".max-gpa-triangle")
            .data(d.values.filter(v => v.isMax))
            .enter().append("path")
            .attr("d", d3.symbol().type(d3.symbolTriangle).size(150))
            .attr("transform", function(d) { 
                return `translate(${xScale(d.semester)}, ${yScale(d.gpa)})`; 
            })
            .style("fill", function() { return color(d.key); })
            .on("mouseover", tip.show)
            .on("mouseout", tip.hide);


        // Draw circles for other points
        group.selectAll("circle")
            .data(d.values.filter(v => !v.isMax))
            .enter().append("circle")
            .attr("r", 5)
            .attr("cx", function(d) { return xScale(d.semester); })
            .attr("cy", function(d) { return yScale(d.gpa); })
            .style("fill", function() { return color(d.key); })
            .on("mouseover", tip.show)
            .on("mouseout", tip.hide); 
    });


    Object.keys(semesters).forEach(course => {
        let semester = semesters[course];
        svg.selectAll(".dot")
            .data(courseData.filter(d => d.course === course && d.semester === semester))
            .enter().append("path")
            .attr("d", d3.symbol().type(d3.symbolCross).size(250)) // Use symbolCross for "x"
            .attr("transform", d => `translate(${xScale(d.semester)}, ${yScale(d.gpa)})`)
            .attr("fill", color(course))
            .on("mouseover", tip.show)
            .on("mouseout", tip.hide);
    });


    // Interaction: Highlight the course's line and dim others
    svg.selectAll(".course-group")
        .on("mouseover", function(event, d) {
            // Dim all lines
            svg.selectAll(".line").style("opacity", 0.1);
            // Highlight hovered line
            d3.select(this).select(".line").style("opacity", 1);
        })
        .on("mouseout", function(event, d) {
            // Reset opacity
            svg.selectAll(".line").style("opacity", 1);
        });


    // Add legend
    const legendEntryWidth = 100; // Width of each legend entry
    const legendEntryHeight = 18; // Height of each legend entry
    const legendColumns = 2; // Number of columns in the legend


    const legend = svg.selectAll(".legend")
        .data(dataNest)
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) {
    // Calculate row and column position
            const col = i % legendColumns;
            const row = Math.floor(i / legendColumns);
            const x = width*1.02 - (legendColumns - col) * legendEntryWidth;
            const y = row * legendEntryHeight - height*0.05;
            return "translate(" + x + "," + y + ")";
        });

    legend.append("rect")
        .attr("width", 10)
        .attr("height", 10)
        .style("fill", function(d) { return color(d.key); });

    legend.append("text")
        .attr("x", 15)
        .attr("y", 10)
        .text(function(d) { return d.key; });

    // Add X and Y axis labels
    svg.append("text")
        .attr("transform", "translate(" + (width/2) + " ," + (height + margin.bottom - 20) + ")")
        .style("text-anchor", "middle")
        .text("Semester#");

    svg.append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 0 - margin.left)
        .attr("x",0 - (height / 2))
        .attr("dy", "1em")
        .style("text-anchor", "middle")
        .text("GPA");  
    console.log("Graph should be drawn now");
};