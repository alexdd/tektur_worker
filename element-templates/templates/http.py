#    Tektur Worker - Camuda external task executor for ETL processes 
#    Copyright (C) 2020 - 2025  Alex Duesel, tekturcms@gmail.com

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

import json

def http_request_template():   
    return     {
        "name": "http-request",
        "id": "tektur.http-request",
        "appliesTo": [
            "bpmn:ServiceTask"
        ],
        "entriesVisible": {
            "multiInstance-loopCardinality": True,
            "parameterType-text": True,
            "parameterType": True,
            "parameterType-script": True,
            "parameterType-map": True,
            "_all": False,
            "outputs": True,
            "parameterType-list": True,
            "parameterName": True,
            "inputs": True,
            "multiInstance-elementVariable": True,
            "multiInstance-collection": True
        },
        "properties": [
            {
                "binding": {
                    "name": "camunda:type",
                    "type": "property"
                },
                "type": "Hidden",
                "value": "external"
            },
            {
                "binding": {
                    "name": "camunda:topic",
                    "type": "property"
                },
                "label": "Topic",
                "type": "String",
                "description": "Task implementation to be executed",
                "value": "http_request"
            },
            {
                "binding": {
                    "name": "camunda:asyncBefore",
                    "type": "property"
                },
                "type": "Hidden",
                "value": True
            },
            {
                "binding": {
                    "name": "camunda:asyncAfter",
                    "type": "property"
                },
                "type": "Hidden",
                "value": True
            },
            {
                "label": "method",
                "type": "Dropdown",
                "value": "get",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "method"
                },
                "description": "HTTP method",
                "constraints": {
                    
                },
                "choices": [
                    {
                        "name": "GET",
                        "value": "get"
                    },
                    {
                        "name": "POST",
                        "value": "post"
                    }
                ]
            },
            {
                "label": "host",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "host"
                },
                "description": "host of the webservice",
                "constraints": {
                    "notEmpty": True
                }
            },
            {
                "label": "port",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "port"
                },
                "description": "Port to use on the http server, defaults to 8000",
                "constraints": {
                    
                }
            },
            {
                "label": "endpoint",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "endpoint"
                },
                "description": "Path to endpoint without host and port part, e.g. \"/v1/documents\"",
                "constraints": {
                    "notEmpty": True
                }
            },
            {
                "label": "queryParameters",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "queryParameters"
                },
                "description": "Query parameters - These must be defined as Map in the \"Input/Output\" tab. If you need to pass multiple values for the same parameter, name each element with a unique suffix in brackets (i.e. foo[1], foo[2] ...). The actual indexes do not influence the order in which parameters are sent to the server.",
                "constraints": {
                    
                }
            },
            {
                "label": "XML exist-DB payload",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "existPayload"
                },
                "description": "XML Query for exist-DB for POST request",
                "constraints": {
                    
                }
            },
            {
                "label": "responseFilename",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "responseFilename"
                },
                "description": "Name of file to write response to",
                "constraints": {
                    
                }
            },
            {
                "label": "status",
                "type": "String",
                "value": "",
                "editable": False,
                "binding": {
                    "type": "camunda:outputParameter",
                    "source": "${ status }"
                },
                "description": "Status code of the HTTP response",
                "constraints": {
                    
                }
            }
        ]
    }
    