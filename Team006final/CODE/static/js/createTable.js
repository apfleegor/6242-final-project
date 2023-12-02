function createTable(optimize_output, summer) {
    // Access the HTML elements for the table and its body
    var table_select = document.getElementById("schedule");
    var body_select = document.getElementById("tableBody");

    // Clear all existing rows in the table to prepare for new data
    while (table_select.rows.length > 0) {
        table_select.deleteRow(0);
    }

    // List of academic years for labeling rows
    let year_list = ['2024-2025', '2025-2026', '2026-2027', '2027-2028', '2028-2029', '2029-2030', '2030-2031', '2031-2032'];

    // Create table header with conditional inclusion of the Summer column
    var header = table_select.createTHead();
    var head_row = header.insertRow(0);
    var cellCount = summer === 1 ? 5 : 4; // Number of cells changes based on summer term inclusion

    // Adding column headers to the table
    head_row.insertCell(0).innerHTML = "Year";
    head_row.insertCell(1).innerHTML = "Fall";
    head_row.insertCell(2).innerHTML = "Spring";
    if (summer === 1) {
        head_row.insertCell(3).innerHTML = "Summer"; // Add summer column if summer courses are included
    }
    head_row.insertCell(cellCount - 1).innerHTML = "End of Year GPA"; // GPA column

    let currentYearIndex = 0;
    let semesterIndex = 0; // 0: Fall, 1: Spring, 2: Summer (if applicable)
    let totalGPA = 0;
    let numCourses = 0;

    optimize_output[2].forEach((semesterCourses, index, semesterArray) => {
        // Reset GPA calculation variables at the start of each academic year
        if (semesterIndex === 0) {
            totalGPA = 0;
            numCourses = 0;
        }

        // Determine if it's a new academic year
        var row;
        if (semesterIndex === 0) {
            row = body_select.insertRow(-1);
            row.insertCell(0).innerHTML = year_list[currentYearIndex];
            row.insertCell(1); // Fall
            row.insertCell(2); // Spring
            if (summer === 1) {
                row.insertCell(3); // Summer
            }
            row.insertCell(summer === 1 ? 4 : 3); // End of Year GPA cell
        } else {
            row = body_select.rows[currentYearIndex];
        }

        // Fill in course details and accumulate GPA for the semester
        semesterCourses.forEach(course => {
            let courseInfo = `${course[0]}: ${course[1].toFixed(2)}`;
            row.cells[semesterIndex + 1].innerHTML += courseInfo + "<br>";
            totalGPA += course[1];
            numCourses++;
        });

        // Check if it's the last semester in the academic year or the last semester data available
        if (semesterIndex === 2 && summer === 0 || semesterIndex === 3 && summer === 1 || index === semesterArray.length - 1) {
            let averageGPA = numCourses > 0 ? (totalGPA / numCourses).toFixed(2) : "N/A";
            row.cells[row.cells.length - 1].innerHTML = averageGPA;

            // Move to the next academic year
            currentYearIndex++;
            semesterIndex = 0;
        } else {
            // Move to the next semester
            semesterIndex++;
        }
    });


    // Extract the overall GPA from the output and display in the last row
    let overallGPA = optimize_output[0];
    var overallGPARow = body_select.insertRow(-1);
    overallGPARow.insertCell(0).innerHTML = "Predicted Cumulative GPA";
    var gpaCell = overallGPARow.insertCell(1);
    gpaCell.colSpan = cellCount - 1;
    gpaCell.innerHTML = `<strong>${overallGPA.toFixed(2)}</strong>`;
    gpaCell.style.textAlign = "center";
}
