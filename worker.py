import requests, time, os, json, logging
from settings import CAMUNDA_SERVER_URL, POLL_INTERVAL, WORKING_DIR, WORKER_ID
import tasks
from errors import TaskError

logging.basicConfig(filename="requests.log", format='%(asctime)s - %(message)s')
log = logging.getLogger('urllib3') 
fetch_url = CAMUNDA_SERVER_URL+'engine-rest/external-task/fetchAndLock'

class CamundaWorker:

    """This worker polls the Camunda BPMN engine for scheduled tasks, which will be 
    executed by the tasks module. Currently the following tasks are available:
        - aws: S3 list bucket content
        - aws: S3 put a file into a bucket
        - aws: S3 get a file from a bucket
        - exist-db: load xml files ino the db
        - http: send a get or post request to a webservice
        - mail: send an email with an attachment
        - xslt: transform XML using XSLT
        - zip: zip or extract files
    It may be used e.g. for XML ETL processes ...
    """
    
    def __init__(self):
        self.running = True
        self.run()
        
    def run(self):
        while self.running: 
            try:
                log.setLevel(logging.INFO)
                res = requests.post(fetch_url, json = {"workerId": WORKER_ID,
                                               "maxTasks":1,
                                               "usePriority":"true",
                                               "topics":  [{"topicName": topic,
                                                            "lockDuration": 30000,
                                                            "deserializeValues": "true"} 
                                                            for topic in dir(tasks) if callable(getattr(tasks, topic))]})
                response = json.loads(res.text)
            except:  
                response = []
                print('Engine is down')
        
            if len(response) == 0:
                time.sleep(POLL_INTERVAL)
                continue
      
            taskId = str(response[0]['id'])
            processInstanceId = str(response[0]['processInstanceId'])
            tmp_path = os.path.join(WORKING_DIR, processInstanceId)
            os.makedirs(tmp_path, exist_ok=True)
            log.setLevel(logging.DEBUG)
            try:
                variables = getattr(tasks, response[0]['topicName'])(tmp_path, response[0]['variables']) 
                complete = requests.post(CAMUNDA_SERVER_URL + 'engine-rest/external-task/' + taskId + '/complete', 
                                         json = {"workerId": WORKER_ID,
                                                 "variables": variables})
            except TaskError as te:
                failed = requests.post(CAMUNDA_SERVER_URL + 'engine-rest/external-task/' + taskId + '/failure',
                                       json = {"workerId": WORKER_ID, 
                                               "errorMessage" : te.message, 
                                               "errorDetails" : te.details})

CamundaWorker()
