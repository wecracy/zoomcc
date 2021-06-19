#-*-coding:utf-8-*-

import requests
class ZoomInterface():
    __instance = None
    url = ""
    seq_count = 0

    @classmethod
    def __getInstance(cls):
      return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
      cls.__instance = cls(*args, **kargs)
      cls.instance = cls.__getInstance
      return cls.__instance

    def setURL(self, url):
        if url.startswith('https://us02wmcc.zoom.us/closedcaption'):
            self.url = url
            return True
        else:
            return False

    def sendCC(self, text, lang):
        if self.url.startswith('https://us02wmcc.zoom.us/closedcaption'):
            resp = requests.post(self.url, params = {'seq': str(self.seq_count), 'lang': lang}, data=text.encode('utf-8'), headers = {'Content-type': 'text/plain; charset=utf-8'})
            if resp.status_code == 200:
                self.seq_count = self.seq_count + 1
                return True
        return False
