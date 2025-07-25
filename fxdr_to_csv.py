import pandas as pd
import logging    # pyhton build-in Lib
import csv
import win32com.client
import os
import error_log_config

fxdr_path = "T:\\FXDR\\FXDR_v5.xlsm"

def refresh_file(file):
    xlapp = win32com.client.DispatchEx("Excel.Application")
    path = os.path.abspath(file)
    wb =  xlapp.Workbooks.Open(path)
    wb.RefreshAll()
    xlapp.CalculateUntilAsyncqueriesDone()
    wb.SaveAs(path.replace(".xlsm", "_refreshed_temp.xlsm"))
    xlapp.Quit()

def load_bal_data(file_path):
    try:
        refresh_file(file_path)
        dtype_spec = {
            'Our Ref': str,
            'Account No.': str
            }
        refreshed_path = file_path.replace(".xlsm", "_refreshed_temp.xlsm")
        data = pd.read_excel(refreshed_path, sheet_name="Deal", dtype=dtype_spec)  # specific setting for FOCCP file # without note++ edit, the ClientID remain obj ??
        os.remove(refreshed_path) 
        logging.info(f"Data loaded successfully from {file_path}")
        return data
    except Exception as e:
        logging.error(f"Error loading data from {file_path}: {e}")
        raise


def basic_run():

    try:
        df = load_bal_data(fxdr_path) # ac no. 123555 become 123555.0 here into df
        df = df.drop(df.iloc[:, 28:55],axis = 1)
        df = df.dropna(axis=0, thresh=2) # thresh=1, then at least have 1 non-nan'row keep, as a result all row keep; but thresh=2, do not meet 2 non-nan value's row drop, = what I want
        df.to_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\partial\\fxdr\\current_deal.csv', encoding='utf-8', index=False, quoting=csv.QUOTE_ALL)
    except Exception as e:
        logging.error(f"Error in basic_run: {e}")
        raise
