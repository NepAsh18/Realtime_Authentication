import heapq
from datetime import datetime
active_sessions = {}
expiry_heap = {}

def cleanup_expired_tokens():
    now  = datetime.now()
    while expiry_heap and expiry_heap[0][0] <= now:
        token_id = heapq.heappop(expiry_heap)
        active_sessions.pop(token_id, None)


def add_session(token_id, user_id, expiry):
    active_sessions[token_id] = user_id
    heapq.heappush(expiry_heap, (expiry, token_id))


def revoke_session(token_id):
    active_sessions.pop(token_id, None) 