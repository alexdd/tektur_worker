import requests, json, time, os, json
from settings import CAMUNDA_SERVER_URL, POLL_INTERVAL, WORKING_DIR, WORKER_ID
import tasks
 
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
    error = getattr(tasks, response[0]['topicName'])(tmp_path, 
                                                      response[0]['variables']) 
    response = {
        "workerId": WORKER_ID,   
    }
    if not error: 
        try:
            complete_url = (CAMUNDA_SERVER_URL + 'engine-rest/external-task/' + taskId + '/complete')
            complete = requests.post(complete_url, json=response)
            print('complete status code: ', complete.status_code)
        except: 
            print('complete request failed: '+taskId)
    else:
        try:
            failed_url = (CAMUNDA_SERVER_URL + 'engine-rest/external-task/' + taskId + '/failure')
            response["errorMessage"] = error["errorMessage"]
            response["errorDetails"] = error["errorDetails"]
            failed = requests.post(failed_url, json=response)
            print('failed status code: ', failed.status_code)
        except: 
            print('failed request failed: '+taskId)
