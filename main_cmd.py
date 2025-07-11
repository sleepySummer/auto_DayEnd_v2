# https://puremonkey2010.blogspot.com/2019/05/python-python-schedule.html
# https://hahow.in/creations/622c59e9a7ab280006222379
# solve unpredictable auto-logout problem of itrade
# kill cmd and re-open a new one everytime
import os
import time
import schedule

# work well, self open cmd --> run this .py --> on time execute commond line at new cmd --> finish all line inside --> kill it
def cmd_line():
    os.system('start cmd /k "cmd_app.py"')  # direct execute the code with showing directory first
    os.system("taskkill /f /im cmd.exe") # it will close cmd when nothing is running, but main_app2.py keep looping = will not close, need a app.py out of loop, loop outside

#os.system("start cmd") # directory start at where this .py locate, that is C:\Users\Ichi\Desktop\quick_py\partial>

def get_season_input():
    while True:
        season = input("Summer/Winter?: ")
        if season in ["Summer", "Winter"]:
            return season
        else:
            print("Invalid input. Please enter 'Summer' or 'Winter'.")

season = get_season_input()

if season == "Summer":
    schedule.every().tuesday.at("05:01").do(cmd_line)
    schedule.every().wednesday.at("05:01").do(cmd_line)
    schedule.every().thursday.at("05:01").do(cmd_line)
    schedule.every().friday.at("05:01").do(cmd_line)
    schedule.every().saturday.at("05:01").do(cmd_line)
elif season == "Winter":
    schedule.every().tuesday.at("06:01").do(cmd_line)
    schedule.every().wednesday.at("06:01").do(cmd_line)
    schedule.every().thursday.at("06:01").do(cmd_line)
    schedule.every().friday.at("06:01").do(cmd_line)
    schedule.every().saturday.at("06:01").do(cmd_line)


print("Scheduler started. Waiting for the scheduled time...")

while True:
        schedule.run_pending()
        time.sleep(10)


