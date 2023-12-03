# 6242-final-project

index.html - dashboard style deliverable

**Quick Start**
1. `git clone` repo to your local directory
2. run `python app.py` (flask file) on command line
3. click on link to locally run index.html  

data folder - contains data and a cleaner notebook for any cleaning needed

--- NEW README DRAFT below

# OptiDule: GPA Optimization and Course Scheduling Tool

## Overview

OptiDule is a dynamic, data-driven application designed to optimize students' academic schedules at Georgia Tech by forecasting GPA trends and suggesting the most beneficial course sequences. This tool is particularly useful for maximizing GPA based on past course data, semester trends, and various constraints like credit hours and prerequisites.

## Features

- **GPA Forecasting:** Utilizes ARIMA models to predict future course GPAs based on historical data.
- **Schedule Optimization:** Provides optimized academic schedules that balance GPA potential and course load.
- **Interactive Dashboard:** A user-friendly web interface built with Flask and Bootstrap for easy navigation and visualization.
- **Customizable Constraints:** Accommodates user preferences for credit hours, summer courses, and prerequisites.

## Installation

To set up the OptiDule project, follow these steps:

1. Clone the repository:
   ```
   git clone [repo-link]
   ```
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the OptiDule application:

1. Navigate to the project directory.
2. Start the Flask server:
   ```
   python app.py
   ```
3. Access the web interface via your browser at `http://127.0.0.1:8000/` or whatever address you see in the terminal.

## Project Structure

- `app.py`: The main Flask application file.
- `data/`: Contains historical GPA data and course information.
- `models/`: ARIMA model scripts for GPA forecasting.
- `optimization/`: Scripts for course schedule optimization.
- `templates/`: HTML templates for the Flask app.
- `static/`: CSS and JavaScript files for the web interface.

## Data Files

- `data/raw_data contents`: Historical GPA data for courses at Georgia Tech.
- `data/ contents`: Information about courses, including prerequisites and credit hours and GPA predictions

## Contributing

We welcome contributions to OptiDule. To contribute, please:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgements

- Georgia Tech Institutional Research and Planning team for providing the data.
- Team 6 members: Harrison Kwon, Devanshu Tiwari, Henry Wallace, Monishka Sinha, Feyzican Eser, Alexandra Pfleegor for their invaluable contributions.
