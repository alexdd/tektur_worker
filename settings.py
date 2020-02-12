import secure_settings

JAVA_CMD = "java"
TIDY_CMD = "tidy"
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