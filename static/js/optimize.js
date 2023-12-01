function optimize_from_html(course_list, pre_reqs_list) {
    // console.log(course_list)
    // console.log("----------------")

    var minHours = document.getElementById('minPrompt').value;
    var maxHours = document.getElementById('maxPrompt').value;
    var summer_bool = document.getElementById('summerPrompt').value;

    console.log(summer_bool)
    console.log(minHours)
    console.log(maxHours)

    // convert to 0 or 1
    summer_final = 0;
    if (summer_bool=="yes") {
        summer_final = 1;
    }

    // Send the selected number to the server
    fetch('/run_optimization', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            'summer' : summer_final, 
            'minHours' : minHours, 
            'maxHours' : maxHours,
            'course_list': course_list,
            'prereqs': pre_reqs_list
        })
    })
    .then(response => response.json())
    .then(data => {
        // console.log("testing")
        // Update the result on the webpage
        // console.log(data.opt_log)
        // console.log("GPA DATA:", data.gpas)
        // console.log("Semester DATA:",data.semesters)
        // console.log("Prereqs DATA:",data.prereqs)
        // console.log("Profs DATA:",data.professors)


        if (data.opt_log=="ERROR") {
            alert("Infeasible. Please check your inputs.");
            // error_message()

        } else {
            console.log("here2")
            createTable(data.opt_log, summer_final);
            drawInteractiveLineChart(data.gpas, data.semesters, data.prereqs, data.professors);
        }
        // drawInteractiveLineChart(dummy_gpas, dummy_semesters, dummy_prereqs, dummy_professors)

        // document.getElementById('optimization_results').innerText = 'RESULTS:\n' + data.opt_log;
    })
    .catch(error => console.error('Error:', error));
}