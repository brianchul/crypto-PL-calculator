import aiohttp
import random
import time
from flask import current_app


class SessionFetch():
    def __init__(self) -> None:
        self.MAX_RETRY = current_app.config['MAX_RETRY']
        pass


    async def fetch(self, session: aiohttp.ClientSession, url, param={}):

        statusCode = 0
        retryCount = 0
        while statusCode != 200 :
            if retryCount >= self.MAX_RETRY:
                break
            async with session.request(method="GET", url=url, params=param) as response:
                statusCode = response.status
                responseText = await response.text()
                if statusCode == 200:
                    return responseText
                elif statusCode != 429:
                   current_app.logger.warning("Unable to fetch transaction detail, statusCode: {code}, response: {response}".format(response=responseText, code=statusCode))
                   break
            sleepTime = random.randint(10,100)/100
            current_app.logger.warning("fetching transaction detail: {url} rate limited, retry count: {c}, wait for {t} second to retry".format(url=url, c=retryCount, t=sleepTime))
            time.sleep(sleepTime)
            retryCount += 1
        return 