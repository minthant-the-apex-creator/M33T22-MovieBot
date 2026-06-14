import os

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

DATABASE_URL = os.environ.get("DATABASE_URL", "")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

ADMINS = [36306629]
AUTH_CHANNEL = int(os.environ.get("AUTH_CHANNEL", 0)) if os.environ.get("AUTH_CHANNEL") else None

AUTO_DELETE_TIME = int(os.environ.get("AUTO_DELETE_TIME", 86400))
FLOOD_TIME = int(os.environ.get("FLOOD_TIME", 600))

PICS = (os.environ.get('PICS', 'https://graph.org/file/01ddfcb1e8203879a63d7.jpg https://graph.org/file/d69995d9846fd4ad632b8.jpg'))
