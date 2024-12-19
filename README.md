# Automated Trading Data Processing

This project automates the process of scheduling, downloading, data transformation, updating latest trade status, and storing trading data from a specified website. It includes functionalities for logging into the website, downloading various types of trading reports, processing the data using Python, Pandas and SQL and saving the processed data to a specified directory.

## Table of Contents

- Installation
- Usage
- Configuration
- Features
- Modules
- Contributing
- License

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/sleepySummer/auto_DayEnd.git
    cd auto_DayEnd.git
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Set Up Configuration:**
   - Create a seperated `config.py` file in the project directory with your individual login credentials:
     ```python
     # config.py
     itrade_username = "your_username"
     itrade_password = "your_password"
     mysql_password = "your_password"
     ```

2. **Run the Script:**
   - Execute the main script, or scheduler, to start the process:
     ```sh
     python main_cmd.py
     ```

## Configuration

- **config.py:** This file contains the login credentials required to access the trading website. Ensure this file is in the same directory as `main_cmd.py` and is not included in version control for security reasons.

## Workflow
- add a chart here like that de project

## Modules

### main_cmd.py
- Independently opens the main script in a new command prompt at scheduled times and closes the prompt after execution to ensure login credentials are cleared.

### cmd_app.py
- Handles the main workflow include logging in, downloading CSV files, processing data, and moving them to the appropriate directory.

### edit_csv.py
- Contains functions for editing and processing CSV files.

### fxdr_to_sql_v2.py
- Contains functions for processing FXDR data and integrating it into the deal list.

### deal_status.py
- Comparing with mysql database and generates the lalest deal status. Saves the processed result to a CSV file.

## License
- Copyright (c) 2024 [Ian Chi]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
