// tooltip for the interactive chart
const tooltip = d3.select("body").append("div")
    .attr("id", "tooltip")
    .style("position", "absolute")
    .style("visibility", "hidden")
    .style("pointer-events", "none")
    .style("padding", "6px")
    .style("background", "rgba(0, 0, 0, 0.8)")
    .style("color", "#fff")
    .style("border-radius", "4px")

const classes_url = "../static/classes.json"

// Loads in first course after DOM loads in
d3.json(classes_url).then(function(data){

    classes = data;

    var courseBox = document.getElementById("datalistOptions")

    // Loops through courses to create dropdown
    for(var i = 0; i < classes.length; i++) {
        var course1 = document.createElement("option");
        course1.value = classes[i];
        course1.text = classes[i];
        courseBox.appendChild(course1);
    };

    // To limit to 8 courses inputted (to be changed)
    var courseCount = 2;
    var MAX_CLASSES = 40; // approximately one undergraduate degree

    // Function to dynamically add select box
    function addSelectionBox() {

    // Check if reached max
    if(courseCount >= MAX_CLASSES) {
        return;
    }

    // Increment counter
    courseCount++;

    // Create select element 
    var newCourse = document.createElement("input");

    // Set attributes
    // <input class="form-control" list="datalistOptions" id="coursePrompt" placeholder="Type to search...">
    newCourse.setAttribute("class", "form-control");
    newCourse.setAttribute("list", "datalistOptions");
    newCourse.setAttribute("id", "coursePrompt");
    newCourse.setAttribute("placeholder", "Type to search...");


    for(var i = 0; i < classes.length; i++) {
        var course = document.createElement("option");
        course.value = classes[i];
        course.text = classes[i]; 
        newCourse.appendChild(course);
    }

    // new pre-req box
    // Create select element 
    var newPre = document.createElement("input");

    // Set attributes
    newPre.setAttribute("class", "form-control");
    newPre.setAttribute("list", "preOptions");
    newPre.setAttribute("id", "preReqPrompt");
    newPre.setAttribute("placeholder", "Enter prereqs...");

    document.getElementById("newCourseClick").appendChild(newCourse);
    document.getElementById("newPre").appendChild(newPre);

    }
    // ADDING A NEW CLASS
    document.getElementById("addSelect")
            .addEventListener("click", addSelectionBox);

});



// get the courses from the selection into the schedule
document.getElementById("optimize").addEventListener("click", function() {

    // console.log("------")
    // console.log(document.getElementById("maxPrompt").value)

    // code for interactive line chart
    document.getElementById("Interactive_Graph").innerText = " \
    The interactive graph below plots GPA against semester number. \n\n \
    Each inputted class's projected GPAs are shown for every semester, with each '▲' designating \
    the semester where GPA is projected to be highest, and each '➕' designating which semester \
    is recommended, based on maximizing total GPA.\n\n Hover over each course to \
    compare Optidule's choice to other semesters! Hovering over a marked datapoint will show the max and min GPA achievable for \
    that course, the GPA achieved by Optidule's choice, along with the professor teaching it and its pre-requisites. ";

    // working on getting info from course selection
    course_div = document.getElementById("courseSelection")
    options = course_div.getElementsByTagName("input")

    courses_list = []
    for (let i=0; i<options.length; i++) {
        courses_list.push(options[i].value)
    }
    // console.log(courses_list)

    // get prereqs
    pre_div = document.getElementById("preReq")
    pre_options = pre_div.getElementsByTagName("input")

    pre_reqs_list = []
    for (let i=0; i<pre_options.length; i++) {
        pre_reqs_list.push([pre_options[i].value])
    }
    // console.log(pre_reqs_list)

    optimize_from_html(courses_list, pre_reqs_list)
});


// Event listener for 'Clear Classes' button
document.getElementById("clearClasses").addEventListener("click", function() {
    // Get all input elements within #courseSelection
    var inputs = document.getElementById("courseSelection").getElementsByTagName("input");

    // Iterate over each input and clear its value
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].value = "";
    }

    // clear pre-requisite values
    var prereqs = document.getElementById("preReq").getElementsByTagName("input");
    // var options = document.getElementById("preOptions").getElementsByTagName("option");
    // console.log(options)
    for (let i=0; i<prereqs.length; i++) {
        prereqs[i].value = "";
        prereqs[i].removeAttribute("list")
    }

    // // clear options
    var options = document.getElementById("preOptions");
    // console.log(options.lastChild)
    while (options.firstChild) {
        options.removeChild(options.lastChild);
    }
});

document.getElementById("pre_reqs").addEventListener("click", function() {
    course_div = document.getElementById("courseSelection")
    options = course_div.getElementsByTagName("input")

    courses_list = []
    for (let i=0; i<options.length; i++) {
        courses_list.push(options[i].value)
    }

    var courseBox = document.getElementById("preOptions")
    // console.log(courseBox)

    // Loops through courses to create dropdown
    for(var i = 0; i < courses_list.length; i++) {
        var course1 = document.createElement("option");
        course1.value = courses_list[i];
        course1.text = courses_list[i];
        courseBox.appendChild(course1);
    };

    help_pre = document.getElementById("preReq").getElementsByTagName("input");
    for (let i=0; i<help_pre.length; i++) {
        help_pre[i].setAttribute("list", "preOptions")
    }
})