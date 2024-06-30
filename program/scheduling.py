import schedule
import time
from func_messaging import send_message
from datetime import datetime

def job():
    print("This job runs every N minutes")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_message(f"message sending from AWS EC2,{timestamp}")

# Schedule job every N minutes
N = 1  # Change this to your desired interval
schedule.every(N).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)