from threading import Lock

connected_clients = 0
lock = Lock()

def increment_clients():
    global connected_clients
    with lock:
        connected_clients += 1

def decrement_clients():
    global connected_clients
    with lock:
        connected_clients = max(0, connected_clients - 1)
        
def has_clients():
    with lock:
        return connected_clients > 0