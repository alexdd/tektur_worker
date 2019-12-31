import requests, time, os, json, logging
from settings import CAMUNDA_SERVER_URL, POLL_INTERVAL, WORKING_DIR, WORKER_ID
import tasks
from errors import TaskError

logging.basicConfig(filename="requests.log", format='%(asctime)s - %(message)s')
log = logging.getLogger('urllib3') 
 
fetchAndLockPayload = {"workerId": WORKER_ID,
  "maxTasks":1,
  "usePriority":"true",
  "topics":  [{"topicName": topic,
               "lockDuration": 30000,
               "deserializeValues": "true"} 
               for topic in dir(tasks) if callable(getattr(tasks, topic))]
} 

fetch_url = CAMUNDA_SERVER_URL+'engine-rest/external-task/fetchAndLock'

while True: 
    log.setLevel(logging.INFO)
    try:
        res = requests.post(fetch_url, json=fetchAndLockPayload)
        body = res.text    
    except:  
        print('Engine is down')

    while body == '[]':
        time.sleep(POLL_INTERVAL)
        res = requests.post(fetch_url, json=fetchAndLockPayload)
        body = res.text
    
    response = json.loads(body)
    taskId = str(response[0]['id'])
    processInstanceId = str(response[0]['processInstanceId'])
    tmp_path = os.path.join(WORKING_DIR, processInstanceId)
    os.makedirs(tmp_path, exist_ok=True)
    log.setLevel(logging.DEBUG)
    try:
        getattr(tasks, response[0]['topicName'])(tmp_path, response[0]['variables']) 
        complete = requests.post(CAMUNDA_SERVER_URL + 'engine-rest/external-task/' + taskId + '/complete', 
                                 json = {"workerId": WORKER_ID})
    except TaskError as te:
        failed = requests.post(CAMUNDA_SERVER_URL + 'engine-rest/external-task/' + taskId + '/failure',
                               json = {"workerId": WORKER_ID, 
                                       "errorMessage" : te.message.decode("UTF-8"), 
                                       "errorDetails" : te.details.decode("UTF-8") })
