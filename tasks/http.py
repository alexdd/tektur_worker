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

import requests, json
from requests.adapters import HTTPAdapter
from requests.exceptions import ConnectionError, Timeout
from settings import HTTP_RETRIES, HTTP_TIMEOUT 
from errors import TaskError

class URLRunner:
    
    def __init__(self, url, method, parameters):
        self.url = url
        self.method = method
        self.response = None
        
    def run(self, session):
        if self.method == "GET":
            param_string = "?" + "&".join([key+"="+self.parameters[key] 
                                           for key in self.parameters.keys()])
            self.response = session.get(self.url + param_string, timeout=HTTP_TIMEOUT) 
        else:
            data = json.dumps(self.parameters)           
            self.response = session.post(self.url, data=data, timeout=HTTP_TIMEOUT) 

class URLAdapter:
    
    def __init__(self, url, variables):
        adapter = HTTPAdapter(max_retries=HTTP_RETRIES)
        self.session = requests.Session()
        self.session.mount(url, adapter)
        self.url = url
        self.variables = variables
        self.runner = URLRunner(self.url, 
                                self.variables["method"]["value"],
                                self.variables["queryParameters"]["value"])
        
    def request(self):
        try:
            self.runner.run(self.session)
        except ConnectionError as ce:
            raise TaskError("HTTP Error! request url!", str(ce))  
        except Timeout:
            raise TaskError("HTTP Error! request timed out url!", self.url) 
  
def http_request(process_dir, variables):
    url = "http://"+ \
          variables["host"]["value"] + ":" + \
          variables["port"]["value"] + \
          variables["endpoint"]["value"]       
   # adapter = URLAdapter(url, variables)
    
    print ("http request called!")
    print ("method: "+variables["method"]["value"])
    print ("host: "+variables["host"]["value"])
    print ("port: "+variables["port"]["value"])
    print ("endpoint: "+variables["endpoint"]["value"])
    print ("queryParameters: "+str(variables["queryParameters"]["value"]))
    print ("JSONfile: "+variables["JSONfile"]["value"])
    print ("responseFilename: "+variables["responseFilename"]["value"])
    return {}
