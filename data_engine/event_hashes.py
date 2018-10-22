import hashlib
class EventHashes:
    hash_list = dict()

    @staticmethod
    def create_hash(obj):
        str_obj = str(obj).encode('utf-8')
        return hashlib.md5(str_obj).hexdigest()

    @staticmethod
    def get(key):
       return EventHashes.hash_list[key] if key in EventHashes.hash_list else ''
    
    @staticmethod
    def set(key, value):
        EventHashes.hash_list[key] = value