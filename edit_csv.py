import csv
import os
import pandas as pd


exclude_strings = ['HouseTest_itradeuse','Test Audit 1','Test Audit 2','Test Audit 3','Test FX','Test IT','Tony Leung']

################
# with open(),open(): allow input/output both done in the loop 
def edit_raw(raw_name):
  
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
  
def edit_deal(deal_name):
  #dtype_spec = {'Order #': str,
                #'Name': str}

  df1 = pd.read_csv(deal_name, dtype=str) # csv into df -> ac name 123555 still 123555, not 123555.0
  
  df2 = pd.read_csv('C:\\Users\\Ichi\\Desktop\\quick_py\\partial\\new_testdeal.csv')

  df1= pd.concat([df1, df2], ignore_index=True) # after .concat -> 123555 become 123555.0
  

  # Write the filtered DataFrame to a new CSV file with all elements quoted
  df1.to_csv(deal_name, index=False, quoting=csv.QUOTE_ALL) # .to_csv will not cause 123555 become 123555.0



################
# omit write into a [] first, result in alot [] inside [], but hard to seperate them out when write back to .csv file
'''
filtered_line = []
with open('raw.csv', mode ='r') as file: 
  csvFile = csv.reader(file)
  for lines in csvFile: # csvFile is '_csv.reader', lines is 'list'
    if not any(exclude in lines for exclude in exclude_strings):
      filtered_line.append(lines) # filtered_line = [[],[],[],......,[]]

# Open the CSV file in append mode 
with open('new_raw.csv', mode='w', newline='') as file: 
    writer = csv.writer(file) 
    writer.writerow(filtered_line)  # Write the new row 

print("done")
'''




###################
# Done by pandas
'''
import pandas as pd
import csv

# Read the CSV file into a DataFrame
df = pd.read_csv('raw.csv')

# Filter out the rows containing the specified strings
exclude_strings = ['HouseTest_itradeuse', 'Test Audit 1', 'Test Audit 2', 'Test Audit 3', 'Test FX', 'Test IT']
filtered_df = df[~df.apply(lambda row: any(exclude in row.values for exclude in exclude_strings), axis=1)]

# Write the filtered DataFrame to a new CSV file with all elements quoted
filtered_df.to_csv('new_raw.csv', index=False, quoting=csv.QUOTE_ALL)

print("done")
'''
##################
'''
nname = input("input raw file full name:")
#nname = os.path.join("directory", nname)
#print(nname)
edit_raw(nname)
'''
