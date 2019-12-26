import requests, json, time
from settings import * 
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
    taskId = response[0]['id']
    taskId = str(taskId)
    print(str(response[0]['variables']))
    result = getattr(tasks, response[0]['topicName'])(response[0]['variables']) 
    response = {
        "workerId": WORKER_ID,   
    }
    if len(result)==0: 
        try:
            complete_url = (CAMUNDA_SERVER_URL + 'engine-rest/external-task/' + taskId + '/complete')
            complete = requests.post(complete_url, json=response)
            print('complete status code: ', complete.status_code)
        except: 
            print('complete request failed: '+taskId)
    else:
        try:
            failed_url = (CAMUNDA_SERVER_URL + 'engine-rest/external-task/' + taskId + '/failure')
            response["errorMessage"] = result
            failed = requests.post(failed_url, json=response)
            print('failed status code: ', failed.status_code)
        except: 
            print('failed request failed: '+taskId)
