class EventHashes:
    hash_list = dict()

    @staticmethod
    def get(key):
       return EventHashes.hash_list[key] if key in EventHashes.hash_list else ''
    
    @staticmethod
    def set(key, value):
        EventHashes.hash_list[key] = value