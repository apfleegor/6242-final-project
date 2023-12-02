function optimize_from_html(course_list, pre_reqs_list) {

    var minHours = document.getElementById('minPrompt').value;
    var maxHours = document.getElementById('maxPrompt').value;
    var summer_bool = document.getElementById('summerPrompt').value;

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

        if (data.opt_log=="ERROR") {
            alert("Infeasible. Please check your inputs.");

        } else {
            console.log("here2")
            createTable(data.opt_log, summer_final);
            drawInteractiveLineChart(data.gpas, data.semesters, data.prereqs, data.professors);
        }
    })
    .catch(error => console.error('Error:', error));
}