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

def move_folder_template():
    return     {
        "name": "move-folder",
        "id": "tektur.move-folder",
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
                "value": "move_folder"
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
                "label": "Source folder",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "source-folder"
                },
                "description": "Name of the folder to move.",
                "constraints": {
                    
                }
            },
            {
                "label": "Destination folder",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "destination-folder"
                },
                "description": "Path to the desitnation folder",
                "constraints": {
                    
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
                        "name": "external",
                        "value": "external"
                    }
                ]
            },
            {
                "label": "Delete",
                "type": "Dropdown",
                "value": "yes",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "delete"
                },
                "description": "Flag wether the folder should be deleted or not",
                "constraints": {
                    
                },
                "choices": [
                    {
                        "name": "yes",
                        "value": "yes"
                    },
                    {
                        "name": "no",
                        "value": "not"
                    }
                ]
            }
        ]
    }
    

def make_path_template():
    return     {
        "name": "make-path",
        "id": "tektur.make-path",
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
                "value": "make_path"
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
                "label": "Path to be created",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "path"
                },
                "description": "Name of the folder structure to be creaated.",
                "constraints": {
                    
                }
            }
        ]
    }
    

def delete_path_template():
    return     {
        "name": "delete-path",
        "id": "tektur.delete-path",
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
                "value": "delete_path"
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
                "label": "Path to be deleted",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "path"
                },
                "description": "Name of the folder structure to be deleted.",
                "constraints": {
                    
                }
            }
        ]
    }
    

def write_data_template():
    return    {
        "name": "write-data",
        "id": "tektur.write-data",
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
                "value": "write_data"
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
                "label": "Path",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "path"
                },
                "description": "The path to the target file.",
                "constraints": {
                    
                }
            },
            {
                "label": "Data",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "data"
                },
                "description": "The data string.",
                "constraints": {
                    
                }
            }
        ]
    }
    

def read_data_template():
    return     {
        "name": "read-data",
        "id": "tektur.read-data",
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
                "value": "read_data"
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
                "label": "Path",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "path"
                },
                "description": "Path to the source file.",
                "constraints": {
                    
                }
            },
            {
                "label": "data",
                "type": "String",
                "value": "",
                "editable": False,
                "binding": {
                    "type": "camunda:outputParameter",
                    "source": "${ data }"
                },
                "description": "Output variable containing the string data that was read.",
                "constraints": {
                    
                }
            }
        ]
    }
    