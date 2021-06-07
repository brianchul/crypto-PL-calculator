import aiohttp
import random
import time


class SessionFetch():
    MAX_RETRY = 10
    def __init__(self) -> None:
        pass


    async def fetch(self, session: aiohttp.ClientSession, url, param={}):

        statusCode = 0
        retryCount = 0
        while statusCode != 200 :
            if retryCount >= self.MAX_RETRY:
                break
            async with session.request(method="GET", url=url, params=param) as response:
                statusCode = response.status
                if statusCode == 200:
                    responseText = await response.text()
                    return responseText
            sleepTime = random.randint(10,100)/100
            print("rate limited: count {c}, wait for {t} second to retry".format(c=retryCount, t=sleepTime))
            time.sleep(sleepTime)
            retryCount += 1
        return ""