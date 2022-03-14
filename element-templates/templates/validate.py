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

def create_schematron_template():
    return      {
        "name": "create-schematron",
        "id": "tektur.geerate-schematron-xslt",
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
                "value": "generate_schematron_xslt"
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
                "label": "Schematron",
                "type": "Text",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "schematron"
                },
                "description": "Inline Schematron rules document to process. Parameter schematron-file must be empty.",
                "constraints": {
                    
                }
            },
            {
                "label": "Schematron File",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "schematron-file"
                },
                "description": "Name of the input file that contains the Schematron rules.",
                "constraints": {
                    
                }
            },
            {
                "label": "Schematron XSLT",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "schematron-xslt"
                },
                "description": "Name of the result file which contains the compiled schematron rules.",
                "constraints": {
                    
                }
            }
        ]
    }
    

def batch_validate_xml_template():
    return     {
        "name": "batch-validate",
        "id": "tektur.batch_validate",
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
                "value": "batch_validate_xml"
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
                "label": "input-folder",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "input-folder"
                },
                "description": "Name of the folder containing XML files to be validated",
                "constraints": {
                    
                }
            },
            {
                "label": "log-file",
                "type": "String",
                "value": "",
                "editable": True,
                "binding": {
                    "type": "camunda:inputParameter",
                    "name": "log-file"
                },
                "description": "Name of the log file to write the validation result to",
                "constraints": {
                    
                }
            },
            {
                "label": "valid",
                "type": "String",
                "value": "",
                "editable": False,
                "binding": {
                    "type": "camunda:outputParameter",
                    "source": "${ valid }"
                },
                "description": "Boolean result of the validation",
                "constraints": {
                    
                }
            }
        ]
    }
    