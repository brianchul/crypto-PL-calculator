import redis, json
from collections.abc import Callable
from flask import current_app

class getOrSetCache:
    def __init__(self):
        self.redis = redis.Redis(host=current_app.config["REDIS_URL"] or "localhost", port=current_app.config["REDIS_PORT"] or 6379)


    def findOrSet(self, key:str, callback:Callable[[str], list] or None,  timeout:int=None):
        try:
            data = self.findKey(key)
            if data is not None:
                return json.loads(data.decode('utf8'))
            else:
                data = callback()
                if timeout is not None:
                    self.setWithExpire(key, json.dumps(data), timeout)
                else:
                    self.setKey(key, json.dumps(data))
                return data
        except Exception as e:
            print(e)

    def hashValueHasChange(self, hash:str, key:str, value:str) -> bool:
        if self.redis.hget(hash, key).decode("utf8") != value or self.redis.hget(hash, key) is None:
            return True
        else:
            return False


    def findKey(self, key:str):
        return self.redis.get(key)

    def setKey(self, key:str, value:str):
        return self.redis.set(key, value)

    def setWithExpire(self, key:str, value:str, expire: int):
        return self.redis.setex(key, value)

    def hashSet(self, hash:str, key:str, value:str):
        return self.redis.hset(hash, key, value)

    def hashGet(self, hash:str, key:str):
        return json.loads(self.redis.hget(hash, key).decode("utf8"))