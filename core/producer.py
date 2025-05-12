import asyncio, os
from channels.layers import get_channel_layer
from pymongo import MongoClient
from .connection_tracker import has_clients

# MongoDB setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["fortishell_logs"]
collection = db["logs"]

LOG_FILE_PATH = "/home/wadii/pfe/code/fortishell-backend/core/test/logs/test.txt"

def parse_log_line(line):
    parts = line.split(" ")
    log_dict = {}
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            log_dict[key] = value.strip('"')
    return log_dict

def start_log_producer():
    """Start the background async task."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(produce_logs())
    
async def produce_logs():
    print("Log Producer Started")
    channel_layer = get_channel_layer()
    
    while True:
        if not has_clients():
            await asyncio.sleep(1)
            continue
        
        if not os.path.exists(LOG_FILE_PATH):
            await asyncio.sleep(1)
            continue
        
        with open(LOG_FILE_PATH, 'r') as f:
            for line in f:
                if not has_clients():
                    break
                
                line = line.strip()
                if not line:
                    continue
                
                log_dict = parse_log_line(line)
                result = collection.insert_one(log_dict)
                log_dict["_id"] = str(result.inserted_id)
                
                await channel_layer.group_send(
                    "logs_group",
                    {
                        "type": "send_log",
                        "log": log_dict
                    }
                )
                await asyncio.sleep(1)