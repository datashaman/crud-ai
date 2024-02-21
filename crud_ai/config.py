from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENSEARCH_HOST = os.environ.get("OPENSEARCH_HOST", "http://127.0.0.1:9200")
