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

import secure_settings, os

JAVA_CMD = "java"
TIDY_CMD = "C:\\Program Files\\tidy 5.8.0\\bin\\tidy.exe"
DIFF_CMD = "C:\\gnuwin32\\bin\\diff.exe"
XMLLINT_CMD = "C:\\xml\\bin\\xmllint.exe"
CAMUNDA_SERVER_URL = "http://localhost:8080/"
WORKER_ID = "TekturWorker"
POLL_INTERVAL = 1
WORKING_DIR = "C:\\processes"
SAXON_JAR = "C:\\release\\teditor\\lib\\saxon9.jar"
JING_JAR = "C:\\bin\\jing.jar"
TRANG_JAR = "C:\\bin\\trang.jar"
EXIST_DB_CLIENT = "C:\\exist\\bin\\client.bat"
EXIST_DB_SERVER_PORT = "localhost:8081"
EMAIL_SERVER = secure_settings.EMAIL_SERVER
EMAIL_ADDRESS = secure_settings.EMAIL_ADDRESS 
EMAIL_PASSWORD = secure_settings.EMAIL_PASSWORD
EMAIL_USER = secure_settings.EMAIL_USER
HTTP_RETRIES = 3
HTTP_TIMEOUT = 20
CLEAR_WORKING_DIR = True
SCHEMATRON_DIR = "schematron"
RELAXNG_XSLT_DIR = os.path.join("xslt","relaxng")
TEMPLATE_OUTPUT_FILENAME = "C:\\camodeler\\resources\\element-templates\\tektur_worker.json"
AWS_CREDS = {
    "endpoint_url" : "http://localhost:9000",
    "aws_access_key_id" : secure_settings.AWS_ID,
    "aws_secret_access_key" : secure_settings.AWS_SECRET,
    "region_name" : "eu-central-1" }
