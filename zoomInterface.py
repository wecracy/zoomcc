#-*-coding:utf-8-*-

import requests
import json

class ZoomInterface():
    __instance = None
    url = ""
    seq_count_file_name = "seq_count_temp.txt"
    seq_count_table = {}

    @classmethod
    def __getInstance(cls):
      return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
      cls.__instance = cls(*args, **kargs)
      cls.instance = cls.__getInstance
      return cls.__instance

    def _setSeqCount(self, url, count):
        seq_count_file = open(self.seq_count_file_name, "w+", encoding='UTF8')
        self.seq_count_table[url] = count
        json.dump(self.seq_count_table, seq_count_file)
        seq_count_file.close()

    def _loadSeqCount(self):
        try:
            seq_count_file = open(self.seq_count_file_name, "r", encoding='UTF8')
            seq_count_table = json.load(seq_count_file)
            seq_count_file.close()
            return seq_count_table
        except:
            return dict()

    def setURL(self, url):
        try:
            if url.startswith('https://') and "closedcaption" in url:
                self.url = url
                self.seq_count_table = self._loadSeqCount()
                if url not in self.seq_count_table.keys():
                    self._setSeqCount(url, 0)
                return (True, "")
            else:
                return (False, "바른 주소가 아닙니다.")
        except:
            return (False, "알 수 없는 오류가 발생하였습니다.")
    
    def sendCC(self, text, lang):
        try:
            if self.url.startswith('https://') and "closedcaption" in self.url:
                resp = requests.post(self.url, params = {'seq': str(self.seq_count_table[self.url]), 'lang': lang}, data=text.encode('utf-8'), headers = {'Content-type': 'text/plain; charset=utf-8'})
                if resp.status_code == 200:
                    self._setSeqCount(self.url, self.seq_count_table[self.url]+1)
                    return (True, "")
                else:
                    return (False, "자막을 보내는 것을 실패하였습니다("+str(resp.status_code) +")")
            else:
                return (False, "Zoom URL을 바르게 설정하세요.")
        except:
            return (False, "알 수 없는 오류가 발생하였습니다.")
