import json
import requests

# TODO: Add tests

class Fixer:

    def __init__(self, https=True):
        if https:
            self.api_url = 'https://api.fixer.io/'
        else:
            self.api_url = 'http://api.fixer.io/'

    def latest(self, base=None, symbols=None, date=None):
        req = date if date else 'latest'
        if base:
            req += '?base={}'.format(base)
        if symbols:
            req += '&' if base else '?'
            req += 'symbols={}'.format(','.join(symbols))
        return self._request(req)

    def _request(self, req):
        resp = None
        print('req: {}'.format(req))
        try:
            r = requests.get(self.api_url + req)
            resp = json.loads(r.content.decode('utf-8'))
        except:
            print('exception in _request')
        return resp


if __name__ == '__main__':
    f = Fixer()
    print(f.latest(base='EUR', symbols=['EUR', 'RUB'],  date='2010-01-03'))
