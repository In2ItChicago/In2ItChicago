import hashlib
import pickle

class ObjectHash:
    @staticmethod
    def load():
        try:
            with open('/tmp/hashes', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return dict()
    
    @staticmethod
    def write(hashes):
        with open('/tmp/hashes', 'wb') as f:
            pickle.dump(hashes, f)

    @staticmethod
    def create_hash(obj):
        str_obj = str(obj).encode('utf-8')
        return hashlib.md5(str_obj).hexdigest()

    @staticmethod
    def get(key):
        hashes = ObjectHash.load()
        return hashes[key] if key in hashes else ''
    
    @staticmethod
    def set(key, value):
        hashes = ObjectHash.load()
        hashes[key] = value
        ObjectHash.write(hashes)