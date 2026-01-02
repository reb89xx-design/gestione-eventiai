import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.environ.get("AGENZIA_DB", os.path.join(BASE_DIR, "agenzia.db"))
