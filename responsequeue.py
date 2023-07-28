from collections import defaultdict, deque


class ResponseQueue:
    def __init__(self):
        self.messages_by_client = defaultdict(deque)

    def add_message(self, cid, message):
        self.messages_by_client[cid].append(message)

    def get_message(self, cid):
        if cid in self.messages_by_client:
            user_queue = self.messages_by_client[cid]
            if user_queue:
                return user_queue.popleft()
            else:
                return None
        else:
            return None
