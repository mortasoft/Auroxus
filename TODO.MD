# TODO

## Threads in Flask 
https://flask.palletsprojects.com/en/2.3.x/patterns/celery/
https://stackoverflow.com/questions/40989671/background-tasks-in-flask
https://stackoverflow.com/questions/26491265/using-celery-with-flask-app-context-gives-popped-wrong-app-context-assertione/64926330#64926330
https://dev.to/itz_salemm/how-to-use-celery-with-flask-2k1m


```python
import threading
import subprocess

def run_nmap():
    result = subprocess.run(['nmap', '-sP', '192.168.1.0/24'], stdout=subprocess.PIPE)
    return result.stdout.decode('utf-8')

@app.route('/scan')
def scan():
    thread = threading.Thread(target=run_nmap)
    thread.start()
    return 'Scanning network in background...'
```