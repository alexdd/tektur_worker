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

import sys, json, templates
from errors import Error
from settings import TEMPLATE_OUTPUT_FILENAME

def create_element_template_structure():
    definition = []
    for template in dir(templates):
        if template.endswith("_template"):
            definition.append(getattr(templates, template)())
    return json.dumps(definition[1:])

# create element_templates JSON file for Camunda modeller 

if __name__ == '__main__':
    sys.stdout = sys.stderr
    try:
        f = open(TEMPLATE_OUTPUT_FILENAME, "w")
        f.write(create_element_template_structure())
        f.close()
        print("Template file successfully written!")    
    except Error as e:
        print("Error writing template file!")
        print(e.message)

        
    

    
        
    