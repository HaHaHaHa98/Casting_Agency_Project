from dotenv import load_dotenv
import os

load_dotenv()
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
ALGORITHMS = os.environ.get("ALGORITHMS")
API_AUDIENCE = os.environ.get("API_AUDIENCE")
DATABASE_URL = os.environ.get("DATABASE_URL")
DATABASE_TEST_URL = os.environ.get("DATABASE_TEST_URL")
CASTING_ASSISTANT = os.environ.get("CASTING_ASSISTANT")
CASTING_DIRECTOR = os.environ.get("CASTING_DIRECTOR")
EXECUTIVE_PRODUCER = os.environ.get("EXECUTIVE_PRODUCER")
