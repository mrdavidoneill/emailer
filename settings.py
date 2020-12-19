import os
from dotenv import load_dotenv
load_dotenv()

MESSAGE = os.getenv("MESSAGE")
SUBJECT = os.getenv("SUBJECT")
FROM_ADDRESS = os.getenv("FROM_ADDRESS")
TO_ADDRESS = os.getenv("TO_ADDRESS")
FROM_PWD = os.getenv("FROM_PWD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
