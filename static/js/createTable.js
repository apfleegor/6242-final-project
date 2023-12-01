
// -----------------------------------------------------------------------------
// CREATING TABLE
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


    // Initialize variables for GPA calculation
    let totalGPA = 0;
    let numCourses = 0;
    let currentYearIndex = 0;
    let semesterIndex = 0; // 0: Fall, 1: Spring, 2: Summer (if applicable)

    optimize_output[2].forEach((semesterCourses) => {
    // Determine if it's a new academic year
    if (semesterIndex === 0) {
    // Create a new row for the new academic year
        var row = body_select.insertRow(-1);
        row.insertCell(0).innerHTML = year_list[currentYearIndex];
        row.insertCell(1); // Fall
        row.insertCell(2); // Spring
    if (summer === 1) {
        row.insertCell(3); // Summer
    }
    row.insertCell(summer === 1 ? 4 : 3); // End of Year GPA
    } else {
        // Access the existing row for the current academic year
        row = body_select.rows[currentYearIndex];
    }

    // Fill in course details and accumulate GPA
    semesterCourses.forEach(course => {
        let courseInfo = `${course[0]}: ${course[1].toFixed(2)}`;
        row.cells[semesterIndex + 1].innerHTML += courseInfo + "<br>";
        totalGPA += course[1];
        numCourses++;
    });

    // Move to the next semester
    semesterIndex++;
    if ((semesterIndex === 2 && summer === 0) || (semesterIndex === 3 && summer === 1)) {
        // Calculate average GPA and display
        let averageGPA = numCourses > 0 ? (totalGPA / numCourses).toFixed(2) : "N/A";
        row.cells[row.cells.length - 1].innerHTML = averageGPA;

        // Reset for the next year
        totalGPA = 0;
        numCourses = 0;
        semesterIndex = 0;
        currentYearIndex++;
    }
    });
}