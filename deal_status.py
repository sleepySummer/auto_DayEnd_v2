import pandas as pd
import csv
from datetime import datetime, timedelta
import logging
import error_log_config

class DealStatus:
    def __init__(self):
        self.df3 = pd.DataFrame(columns=['Command Time', 'Creation Time', 'Order #', 'Name', 'Command Type',
       'Symbol', 'Order Type', 'Lots', 'Value of Contract', 'Base Currency',
       'CCY IM', 'Initial Margin', 'CCY MM', 'Maintenance Margin',
       'Open Price', 'Close Price', 'Transaction Fee', 'Rollover', 'PnL',
       'Turnover', 'Order Credit', 'Value Date', 'Indicator', 'Reason'])

    def symbol_suffix(self, products):
        if products == "CNY NDF":
            return "_FW"
        elif products == "Forward":
            return "_FWD"
        elif products == "FX Accumulator":
            return "_AC"
        else:
            logging.warning(f"Unexpected product name: {products}")
            return "_UNKNOWN"

    def turnover_input(self,comm_type,notional):
        if comm_type == "Rollover":
            return 0
        else:
            return round(notional,0)

    def valuedate_iput(self,comm_type,mature):
        if comm_type == "Rollover":
            return None
        else:
            return datetime.strptime(mature, "%Y-%m-%d").strftime("%Y%m%d") + "\x01" # SOH at the back of the valuedate

    def indicator_input(self,comm_type,product):
        if comm_type == "Rollover":
            return None
        elif product == "Forward":
            return "FWD"
        elif product == "FX Accumulator":
            return "AC"

    # new add method
    def close_price_input(self,comm_type):
        if comm_type == "CloseMarket":
            return 1
        else:
            return 0



    # fxdr into deallist
    def generate_deal(self, row, CommandType, starting_notional):

        try:
            trade_date = datetime.strptime(row['Trade Date'], "%Y-%m-%d").strftime("%m/%d/%Y")
            trade_time = datetime.strptime(row['Deal time '], "%H:%M:%S").strftime("%I:%M:%S %p")
            new_row = {
                'Command Time': datetime.today().strftime("%m/%d/%Y") + " 04:59:59" + " AM", # CloseMarket need manual edit as no data provide
                'Creation Time': trade_date + " " + trade_time,
                'Order #': row['Our Ref'],
                'Name': row['Account No.'],
                'Command Type': CommandType,# loop outside if statement
                'Symbol': row['Currency Pair'] + self.symbol_suffix(row['Product']),
                'Order Type': row['Client Buy / Sell'],
                'Lots': round(starting_notional/100000,1), # from sql
                'Value of Contract': round(round(starting_notional/100000,1)*100000,0), # from sql
                'Base Currency': row['Exposure Currency'],
                'CCY IM': "USD",
                'Initial Margin': row['IM to input on dealist'],
                'CCY MM': "USD",
                'Maintenance Margin': row['IM to input on dealist'],
                'Open Price': 1,
                'Close Price': self.close_price_input(CommandType), # fix close price not always 0
                'Transaction Fee': 0,
                'Rollover': 0,
                'PnL': 0,
                'Turnover': self.turnover_input(CommandType,row['Remaining Exposure (USD)']),
                'Order Credit': 0,
                'Value Date': self.valuedate_iput(CommandType,row['Maturity Date']),
                'Indicator': self.indicator_input(CommandType,row['Product Type']),
                'Reason': None,

                # Add other columns as needed, initializing them with appropriate values
            }
            # Append the new row to df3
            self.df3 = pd.concat([self.df3, pd.DataFrame([new_row])], ignore_index=True)
        except Exception as e:
            logging.error(f"Error generating deal for Order #{row['Our Ref']}: {e}", exc_info=True)
            raise

    def save_to_csv(self):
        self.df3.to_csv('new_testdeal.csv', index=False, quoting=csv.QUOTE_ALL)

