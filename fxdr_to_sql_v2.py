import mysql.connector
import pandas as pd
import deal_status as ds
import fxdr_to_csv as dr
import config

def run_all():

    try:
        from mysql.connector import (connection)

        print("starting")
        # MySQL connection
        db = connection.MySQLConnection(
            host="localhost",  # Replace with your MySQL host
            user="root",       # Replace with your MySQL username
            password=config.mysql_password,  # Replace with your MySQL password
            database="myDB"  # Replace with your MySQL database name
        )
        print("connect success")

        cursor = db.cursor()

        # testing
        dr.basic_run() # return "current_deal.csv" in folder
        print("testing ok!")

        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\partial\\fxdr\\current_deal.csv') 

        # Create a table in MySQL to hold the CSV data (customize as needed)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS deals (
                deals_table_id int primary key auto_increment,
                deals_ref int,
                deal_status varchar(20),
                product_type varchar(50),
                currency varchar(10),
                trade_date date,
                mature_date date,
                direction varchar(4),
                init_exposure decimal(15,2),
                var_margin decimal(13,2),
                deal_client_id int,
                foreign key(deal_client_id) references clients(client_id)
            )
        """)

        deri_trade = ds.DealStatus()

        # Iterate over the DataFrame rows and insert/update into the database
        for i, row in df.iterrows():
            # Check if the deal already exists
            #cursor.execute("SELECT deal_status FROM deals WHERE deals_ref = %s", (row['Our Ref'],))
            cursor.execute("""
            SELECT deal_status, init_exposure
            FROM deals
            WHERE deals_ref = %s
            """, (row['Our Ref'],))
            result = cursor.fetchone() # result = active/mature/liquidated/terminated/none

            if result: # result = active/mature/liquidated/terminated
                deal_status, remaining_exposure = result
                # If the deal exists, compare the deal_status
                if deal_status != row['Trade Status']: # old vs new
                #if result[0] != row['Trade Status']: # result[0] must be active if != row['Trade Status']
                    # Update the deal if the status has changed
                    sql = """
                    UPDATE deals
                    SET deal_status = %s, product_type = %s, currency = %s, trade_date = %s, mature_date = %s, direction = %s, var_margin = %s, deal_client_id = %s
                    WHERE deals_ref = %s
                    """
                    values = (
                        row['Trade Status'], row['Product'], row['Currency Pair'], row['Trade Date'],
                        row['Maturity Date'], row['Client Buy / Sell'], row['IM to input on dealist'], row['Account No.'],
                        row['Our Ref']
                    )
                    cursor.execute(sql, values)
                    # new add
                    deri_trade.generate_deal(row,"CloseMarket",remaining_exposure)
                # new add
                elif deal_status == "Active":
                    deri_trade.generate_deal(row,"Rollover",remaining_exposure)
                #Else: # mature/liquidated/terminated -> mature/liquidated/terminated = None

            else: # result = none -> Active = O + R
                # Insert the new deal if it does not exist


                # SQL foreign key problem: insert into Parent table then Child table
                cursor.execute("SELECT client_id FROM clients WHERE client_id = %s", (row['Account No.'],))
                client_result = cursor.fetchone()
                if not client_result:
                    cursor.execute("INSERT INTO clients (client_id, balance, fxd_limit) VALUES (%s, %s, %s)", (row['Account No.'],0,0))


                sql = """
                INSERT INTO deals (
                    deals_ref, deal_status, product_type, currency, trade_date, mature_date, direction, init_exposure, var_margin, deal_client_id
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    row['Our Ref'], row['Trade Status'], row['Product'], row['Currency Pair'], row['Trade Date'],
                    row['Maturity Date'], row['Client Buy / Sell'], row['Remaining Exposure'], row['IM to input on dealist'], row['Account No.']
                )
                cursor.execute(sql, values)
                # new add
                deri_trade.generate_deal(row,"OpenMarket",remaining_exposure)
                deri_trade.generate_deal(row,"Rollover",remaining_exposure)
                
        
        
        print("insert/update success!")

        # Commit the transaction
        db.commit()

        print("commit success!")
        
        # Close the connection
        cursor.close()
        db.close()

        print("FINISH")

        deri_trade.save_to_csv()
        
    except Exception as e:
        print(f"An error occurred: {e}")

