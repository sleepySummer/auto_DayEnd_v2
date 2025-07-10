import logging
import csv
import os
import pandas as pd
import error_log_config 

exclude_strings = ['HouseTest_itradeuse','Test Audit 1','Test Audit 2','Test Audit 3','Test FX','Test IT','Tony Leung']

################
# with open(),open(): allow input/output both done in the loop 
def edit_raw(raw_name):
  try:
  
    with open(raw_name, mode ='r', encoding='utf-8') as inp, open('new_raw.csv', mode ='w', newline='', encoding='utf-8') as out: # newline='' allow no newline, default is add a empty space new row
      csvFile = csv.reader(inp)
      writer = csv.writer(out, quoting=csv.QUOTE_ALL) # Use QUOTE_ALL to quote all fields # without this setting, all data element output will become normal that is no ""
      for lines in csvFile:
          if not any(exclude in lines for exclude in exclude_strings):
            writer.writerow(lines) 
      inp.close()
      out.close()
    os.remove(raw_name)
    os.rename('new_raw.csv', raw_name)
  except Exception as e:
    logging.error(f"Error occurred while editing raw file: {e}")

def edit_deal(deal_name):
  #dtype_spec = {'Order #': str,
                #'Name': str}
  try:

    df1 = pd.read_csv(deal_name, dtype=str) # csv into df -> ac name 123555 still 123555, not 123555.0
    df2 = pd.read_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\partial\\new_testdeal.csv')
    df1= pd.concat([df1, df2], ignore_index=True) # after .concat -> 123555 become 123555.0
    
    # Write the filtered DataFrame to a new CSV file with all elements quoted
    df1.to_csv(deal_name, index=False, quoting=csv.QUOTE_ALL) # .to_csv will not cause 123555 become 123555.0
  except Exception as e:
    logging.error(f"Error occurred while editing deal file: {e}")
