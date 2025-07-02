# 📊 Automated Trading Data Processing

This project automates the end-to-end workflow of downloading, transforming, and storing trading data from a secure website. It integrates scheduled execution, web automation, data cleaning, database updates, and deal status generation — all orchestrated through Python.

---

## 📁 Table of Contents

- Features
- Installation
- Usage
- Configuration
- Workflow Overview
- Modules
- Contributing
- License

---

## 🚀 Features

- Scheduled execution based on seasonal timing.
- Automated login and CSV download from a trading platform.
- Data cleaning and augmentation using Pandas.
- Integration with MySQL for deal tracking.
- Generation of structured deal commands.
- Robust error logging.

---

## 🛠️ Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/sleepySummer/auto_DayEnd.git
   cd auto_DayEnd
   ```

2. **Install dependencies:**
pip install -r requirements.txt

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

- **cerror_log_config.py:** Initializes error logging to error_log.txt.

## Workflow
(data_architecture.png)

## Modules

### main_cmd.py
- Schedules and launches cmd_app.py in a new command prompt.
- Seasonal timing: Summer (05:01), Winter (06:01), Tue–Sat.

### cmd_app.py
- Logs into the trading site.
- Downloads multiple CSV reports.
- Processes and moves files to a shared network directory.
- Triggers data cleaning and database updates.

### edit_csv.py
- edit_raw(): Cleans raw data by removing test entries.
- edit_deal(): Appends test deals to DealList CSV.

### fxdr_to_csv.py
- Refreshes and loads data from FXDR_v5.xlsm.
- Cleans and exports to current_deal.csv.

### fxdr_to_sql_v2.py
- Loads current_deal.csv into MySQL.
- Inserts or updates deal records.
- Generates deal commands via DealStatus.

### deal_status.py
- Creates structured deal commands (OpenMarket, Rollover, CloseMarket).
- Saves output to new_testdeal.csv.

### error_log_config.py
- Configures error logging to error_log.txt.

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