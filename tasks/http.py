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

import requests, json, os
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, Timeout
from settings import HTTP_RETRIES, HTTP_TIMEOUT 
from errors import TaskError

class URLRunner:
    
    def __init__(self, url, method, parameters):
        self.url = url
        self.method = method
        self.response = None
        self.parameters = parameters
        
    def run(self, session):
        if self.method == "GET":
            param_string = "?" + "&".join([key+"="+self.parameters[key] 
                                           for key in self.parameters.keys()])
            self.response = session.get(self.url + param_string, timeout=HTTP_TIMEOUT) 
        else:
            data = self.parameters           
            self.response = session.post(self.url, data=data, timeout=HTTP_TIMEOUT) 

class URLAdapter:
    
    def __init__(self, url, variables, payload):
        adapter = HTTPAdapter(max_retries=HTTP_RETRIES)
        self.session = requests.Session()
        self.session.mount(url, adapter)
        self.url = url
        self.variables = variables
        self.runner = URLRunner(self.url, self.variables["method"]["value"], payload)
        
    def request(self):
        try:
            self.runner.run(self.session)
        except ConnectionError as ce:
            raise TaskError("HTTP Error! request url!", str(ce))  
        except Timeout:   
            raise TaskError("HTTP Error! request timed out url!", self.url) 
        
    def response_code(self):
        return self.runner.response.status_code
  
    def response_data(self):
        return self.runner.response.text
  
def http_request(process_dir, variables):
    url = "http://"+ \
          variables["host"]["value"] + ":" + \
          variables["port"]["value"] + "/" + \
          variables["endpoint"]["value"] 
    if variables["existPayload"]["value"]:
        try:
            payload = open(os.path.join(process_dir, variables["existPayload"]["value"]), "r").read()
        except Exception as err:
            raise TaskError("HTTP Error! Cannot read request data", str(err)) 
    else:
        payload = variables["queryParameters"]["value"]     
    adapter = URLAdapter(url, variables, payload)
    adapter.request()
    try:
        open(os.path.join(process_dir, variables["responseFilename"]["value"]), "w").write(adapter.response_data())
    except Exception as err:
        raise TaskError("HTTP Error! Cannot write response data", str(err)) 
    return {"status": {"value": adapter.response_code()}}
 