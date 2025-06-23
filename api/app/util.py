import os
from supabase import create_client, Client
import json
import logging
import asyncio

from app.config import SUPABASE_KEY, SUPABASE_URL

log_queue = asyncio.Queue()

class QueueHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        asyncio.create_task(log_queue.put(log_entry))

queue_handler = QueueHandler()
queue_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger = logging.getLogger("app")
logger.addHandler(queue_handler)
logger.setLevel(logging.INFO)

supabase: Client = create_client(supabase_key=SUPABASE_KEY, supabase_url=SUPABASE_URL)