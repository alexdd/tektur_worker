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

import secure_settings

JAVA_CMD = "java"
TIDY_CMD = "tidy"
DIFF_CMD = "diff"
XMLLINT_CMD = "xmllint"
CAMUNDA_SERVER_URL = "http://localhost:8081/"
WORKER_ID = "TekturWorker"
POLL_INTERVAL = 1
WORKING_DIR = "C:\\processes"
SAXON_JAR = "C:\\release\\teditor\\lib\\saxon9.jar"
EXIST_DB_CLIENT = "C:\\exist-db\\bin\\client.bat"
EMAIL_SERVER = secure_settings.SERVER
EMAIL_ADDRESS = secure_settings.ADDRESS 
EMAIL_PASSWORD = secure_settings.PASSWORD
EMAIL_USER = secure_settings.USER
HTTP_RETRIES = 3
HTTP_TIMEOUT = 20
CLEAR_WORKING_DIR = True
SCHEMATRON_DIR = "schematron"