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

def s3_get_template():
    return      {
        "name": "s3-get",
        "id": "tektur.s3-get",
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
                "value": "s3_get"
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
                "label": "bucket",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "bucket"
                },
                "description": "Name of the S3 bucket.",
                "constraints": {
                    
                }
            },
            {
                "label": "key",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "key"
                },
                "description": "Key of object to fetch.",
                "constraints": {
                    
                }
            },
            {
                "label": "filename",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "filename"
                },
                "description": "Name of the file to fetch object to. The file name is relative to the current local workspace.",
                "constraints": {
                    
                }
            }
        ]
    }
    
def s3_list_template():
    return     {
        "name": "s3-list",
        "id": "tektur.s3-list",
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
                "value": "s3_list"
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
                "label": "bucket",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "bucket"
                },
                "description": "Name of the S3 bucket.",
                "constraints": {
                    
                }
            },
            {
                "label": "key",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "key"
                },
                "description": "Key of files to match, may include * and ? as wildcards",
                "constraints": {
                    
                }
            },
            {
                "label": "objects",
                "type": "String",
                "value": "",
                "editable": False,
                "binding": {
                    "type": "camunda:outputParameter",
                    "source": "${ objects }"
                },
                "description": "Result of listing",
                "constraints": {
                    
                }
            }
        ]
    }  

def s3_put_template():
    return     {
        "name": "s3-put",
        "id": "tektur.s3-put",
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
                "value": "s3_put"
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
                "label": "bucket",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "bucket"
                },
                "description": "Name of the S3 bucket.",
                "constraints": {
                    
                }
            },
            {
                "label": "key",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "key"
                },
                "description": "Key to put object to.",
                "constraints": {
                    
                }
            },
            {
                "label": "filename",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "filename"
                },
                "description": "Name of the file to put. The file name is relative to the current local workspace.",
                "constraints": {
                    "notEmpty": True
                }
            },
            {
                "label": "location",
                "type": "Dropdown",
                "value": "process",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "location"
                },
                "description": "Location of the file to upload",
                "constraints": {
                    
                },
                "choices": [
                    {
                        "name": "process",
                        "value": "process"
                    },
                    {
                        "name": "custom",
                        "value": "custom"
                    }
                ]
            }
        ]
    }
    