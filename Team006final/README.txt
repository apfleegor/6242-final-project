DESCRIPTION
Achieving academic success is a top priority for both students and institutions in the dynamic world of higher education. 
It is an intricate puzzle of selecting the right courses at the right time, considering prerequisites, course difficulty, 
and course professors. Making these decisions can be overwhelming, and students often seek answers to questions like, 
"Which combination of Georgia Tech (GT) classes and professors will yield the best and worst GPAs for my chosen courses?". 
Our project "OptiDule", aims to address these concerns by providing students with a powerful tool that enables them to 
discover the ideal combination of classes and professors that will maximize their GPAs, while also offering a tailored, 
optimal course schedule.

This README file will provide a quick guide into understanding, installing, and using OptiDule. Additionally, it is important
to understand the purpose of the remaining files in the deliverable:


The DOC folder
- contains the Final Report (team006report.pdf), a descriptive and thorough dive into the motivation, experimentation, and decisions that led
  to the completed OptiDule
- also contains the Final Poster (team006poster.pdf), a visual guide to the understanding the content of the 
  Final Report quickly

The CODE folder
- this contains all code required to install and run OptiDule:
  * app.py - launches Flask and "index.html", the main file containing the structural dashboard code.
  * optimize_final.py - Contains optimize.py and optimize_final.py scripts for course schedule optimization.
  * static folder - CSS and JavaScript files for the web interface, including class data in JSON format.
    - createTable.js: Handles the dynamic creation and manipulation of the Table that displays optimized course schedules.
    - graph.js: Responsible for generating and managing the interactive graphs for visualizing GPA forecasts and course selections.
    - optimize.js: Handles the optimization logic on the user side by processing user inputs and displaying the results.
    - run.js: Handles the interaction with the optimization backend and runs the other js files
  * data/: Constains GPA predictions for future years along with credit hour data, and a sample dataset for courses taken by an ISYE Major
    - raw_data: Contains raw data files on historical GPA used to generate the predictions
  * Forecasting: Notebooks for finding optimal ARIMA parameters and making predictions using raw data for GPA forecasting.

INSTALLATION

To set up the OptiDule project, follow these steps:

1. Clone the repository:
   ```
   git clone [repo-link]
   ```
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```


## EXECUTION

To run OptiDule:

1. **Start the Flask Server:**
   - Open your terminal or command prompt.
   - Navigate to the project's root directory where `app.py` is located.
   - Run the command:
     ```
     python app.py
     ```
   - This will start the Flask server and host the OptiDule application locally.

2. **Accessing the Dashboard:**
   - Once the Flask server is running, open your web browser.
   - Enter the URL that you see in the command prompt output: for example `http://127.0.0.1:8000/`
   - This will load the OptiDule dashboard.

3. **Using OptiDule:**
   - On the dashboard, start by entering the courses you plan to take.
   - Specify any constraints such as credit hour limits, summer courses, and prerequisites.
   - Click on the 'Optimize Schedule' button to generate your optimized course schedule.
   - The dashboard will display the recommended course sequence along with forecasted GPAs.
   - You can interact with the dashboard to explore different scenarios or modify your course selections.

4. **Exploring Further:**
   - Use the interactive graphs to understand the forecasted GPA trends for each course.
   - Hover over the graph points for detailed information about each course's predicted GPA and other relevant data.
   - Modify your selections or constraints and re-optimize as needed to explore different scheduling options.

5. **Shutting Down:**
   - When finished, you can shut down the Flask server by returning to your terminal or command prompt.
   - Press `CTRL + C` (on Windows) or `Command + C` (on Mac) to stop the server.

## Additional Resources

- For a detailed understanding of OptiDule's development and capabilities you can look at `team006report.pdf` in the DOC folder.
- The `team006poster.pdf` in the same folder provides a quick, visual summary of the project.
- Explore the `raw_data` in the `data` folder for in-depth insights into the historical GPA data used for forecasting.
---

License
Licensed under the MIT License.

Acknowledgements
Georgia Tech Institutional Research and Planning team for the data.
Team 6: Harrison Kwon, Devanshu Tiwari, Henry Wallace, Monishka Sinha, Feyzican Eser, Alexandra Pfleegor.