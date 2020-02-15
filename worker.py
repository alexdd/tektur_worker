#    Tektur Worker - Camuda external task executor for ETL processes 
#    Copyright (C) 2020  Alex Duesel, tekturcms@gmail.com

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests, time, os, json, logging, shutil
from settings import *
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
        - transform: transform XML using XSLT or Tidy HTML
        - zip: zip or extract files
        - pathio: create or delete folder structures
        
    It may be used e.g. for XML ETL processes ...
    """
    
    def __init__(self):
        self.running = True
        self.run()
        
    def run(self):
        
        # poll Camunda server for tasks to be executged in a loop 
        
        processInstanceId = None
        
        while self.running: 
                   
            # delete working directory if process execution has been finished
            
            if processInstanceId:
                res = requests.get(CAMUNDA_SERVER_URL + 'engine-rest/process-instance/' + processInstanceId)
                process_status = json.loads(res.text)
                if res.status_code == 404 or process_status["ended"]:
                    shutil.rmtree(os.path.join(WORKING_DIR, processInstanceId), ignore_errors=True)
           
            # fetch task definitions to be scheduled
            
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
            
            # determine the task ID and make a temp working directory
            
            taskId = str(response[0]['id'])
            processInstanceId = str(response[0]['processInstanceId'])
            tmp_path = os.path.join(WORKING_DIR, processInstanceId)
            os.makedirs(tmp_path, exist_ok=True)
            log.setLevel(logging.DEBUG)
            
            try:
                
                # try to process the task
                
                variables = getattr(tasks, response[0]['topicName'])(tmp_path, response[0]['variables']) 
                
                # send a complete request if successfuly finished processing along with the updated variables state
                
                complete = requests.post(CAMUNDA_SERVER_URL + 'engine-rest/external-task/' + taskId + '/complete', 
                                         json = {"workerId": WORKER_ID,
                                                 "variables": variables})
            except TaskError as te:
                
                # Notify Camunda server in case that the task execution has failed
                
                failed = requests.post(CAMUNDA_SERVER_URL + 'engine-rest/external-task/' + taskId + '/failure',
                                       json = {"workerId": WORKER_ID, 
                                               "errorMessage" : te.message, 
                                               "errorDetails" : te.details})
                   
CamundaWorker()
