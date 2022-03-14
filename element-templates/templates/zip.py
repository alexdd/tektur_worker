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

def file_unzip_template():
    return      {
        "name": "unzip",
        "id": "tektur.unzip",
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
                "value": "file_unzip"
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
                "label": "ZIP Filename",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "zipFilename"
                },
                "description": "",
                "constraints": {
                    
                }
            },
            {
                "label": "Output Folder",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "outputFolder"
                },
                "description": "Result will be extracted to the specified folder.",
                "constraints": {
                    
                }
            }
        ]
    }

def file_zip_template():
    return     {
        "name": "zip",
        "id": "tektur.zip",
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
                "value": "file_zip"
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
                "label": "ZIP File",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "zipFilename"
                },
                "description": "Name of ZIP file to create",
                "constraints": {
                    
                }
            },
            {
                "label": "Input Folder",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "inputFolder"
                },
                "description": "Name of the Folder to be zipped",
                "constraints": {
                    
                }
            },
            {
                "label": "Include Parent Directory",
                "type": "Dropdown",
                "value": "true",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "includeDir"
                },
                "description": "Boolean flag if the parent folder should be included",
                "constraints": {
                    
                },
                "choices": [
                    {
                        "name": "Yes",
                        "value": "true"
                    },
                    {
                        "name": "No",
                        "value": "false"
                    }
                ]
            }
        ]
    }
    