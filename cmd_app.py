# main
# call by main_cmd.py
from twill.commands import * 
import datetime
import os.path
from pathlib import Path
import shutil
from datetime import datetime, timedelta
import time
import schedule
import edit_csv as ec
import fxdr_to_sql_v2 as fxdr
import config

def web_login():

    go('https://gt.itradesolution.com/gtjafx/production/index.php') 
    fv("1", "username", config.itrade_username)
    fv("1", "password", config.itrade_password)
    submit('0')



def download_csv():

    def web_download(yymmdd,target_url,csv_name):

        go(target_url)
        formclear('3')
        if csv_name != "Partial close ":
            #fv("1","from_day","2024-06-05")
            #fv("1","to_day","2024-06-05")
            fv("1","from_day",yymmdd[0:4]+'-'+yymmdd[4:6]+'-'+yymmdd[6:])
            fv("1","to_day",yymmdd[0:4]+'-'+yymmdd[4:6]+'-'+yymmdd[6:])
            submit('0','1')
        submit('0','3') # a new page which clear out html format with pure data is given
        save_html(csv_name+yymmdd+".csv") # itrade page have one more stop in between to auto save to .csv

    def check_file(input_path):
        checking = os.path.exists(input_path)
        return checking

    def cut_paste(from_path, to_path,yr, bb, ymd):

        if check_file(from_path):
            if not check_file(to_path):
                #create
                output_file = Path("//fsn1/Company Share/FUT_FX/FX/Day End Report/"+yr+"/"+bb+"/"+ymd+"/dummy.txt") # only create directories by create file first
                output_file.parent.mkdir(exist_ok=True, parents=True)
                #output_file.write_text(" ") # write sth into that dummpy file, BUT if disable this line, no file create --> no need to delete it back
                # cut and paste
                shutil.move(from_path, to_path) # cut and paste
                #shutil.copy(from_path, to_path) # copy and paste
            else:
                shutil.move(from_path, to_path)
                #shutil.copy(from_path, to_path)

    #tdy = datetime.today()
    tdy = datetime.today() - timedelta(days=1)
    yr = tdy.strftime("%Y")
    bb = tdy.strftime("%b")
    ymd = tdy.strftime("%Y%m%d")

    filetype_link ={'Partial close ':'https://gt.itradesolution.com/gtjafx/production/otherreport/O_PartialClose.php',
                    'LP trade record ':'https://gt.itradesolution.com/gtjafx/production/dailyreport/D_LPTradeList_New.php',
                    'DealList_':'https://gt.itradesolution.com/gtjafx/production/otherreport/O_DealList_RoundUpVersion.php',
                    'new DealList_':'https://gt.itradesolution.com/gtjafx/production/otherreport/O_DealList_createtime.php',
                    'Raw ':'https://gt.itradesolution.com/gtjafx/production/otherreport/O_DayEndRawData.php',
                    #'Log Checking Report ':'https://gt.itradesolution.com/gtjafx/production/otherreport/O_SfcsecurityLog.php' # same result as .csv button give out Garbled characters
                    }
    for file_type, fromlink in filetype_link.items():
        from_path = "C:\\Users\\Ichi\\Desktop\\quick_py\\partial\\" + file_type + ymd +".csv"
        to_path = "//fsn1/Company Share/FUT_FX/FX/Day End Report/"+yr+"/"+bb+"/"+ymd+"/"
        web_download(ymd,fromlink,file_type)
        if file_type == "Raw ":
            ec.edit_raw(from_path)
        if file_type == "new DealList_":
            fxdr.run_all()
            ec.edit_deal(from_path)
        cut_paste(from_path, to_path,yr, bb, ymd)
        # add if statement stop 19min if 'LP trade record '
        if file_type == "LP trade record ":
            time.sleep(29*60) # min x sec

            
            
            

web_login() 

download_csv()

