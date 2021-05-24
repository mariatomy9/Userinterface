from flask import Flask
import time
from plyer import notification
import threading

app = Flask(__name__)

def msg():
    
    while True:
        notification.notify(
            title='HEADING HERE',
            message='DESCRIPTION HERE',
            timeout=2,
            )
        time.sleep(7)

@app.route('/')
def hello_world():
    threading.Thread(target=msg).start()
    return "Hello, world"


if __name__ == '__main__':
   app.run()