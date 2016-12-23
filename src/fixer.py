import json
import requests
from datetime import datetime

# TODO: Add tests

# WARNING: Response date can be different with request date
# req: 2010-01-03?base=EUR&symbols=EUR,RUB
# {'date': '2009-12-31', 'base': 'EUR', 'rates': {'RUB': 43.154}}

# There may be no information about currency on given day in history

class Fixer:

    date_format = '%Y-%m-%d'
    min_date = datetime.strptime('1999-10-01', date_format)
    _allowed_curr = ['EUR', 'SEK', 'HRK', 'CHF', 'AUD', 'CAD', 'IDR', 'BRL', 'ILS',
        'HKD', 'JPY', 'GBP', 'PHP', 'MYR', 'NZD', 'CNY', 'KRW', 'THB', 'USD', 'CZK',
        'NOK', 'ZAR', 'TRY', 'DKK', 'BGN', 'MXN', 'HUF', 'PLN', 'RUB', 'RON', 'INR',
        'SGD']

    def __init__(self, https=True):
        if https:
            self.api_url = 'https://api.fixer.io/'
        else:
            self.api_url = 'http://api.fixer.io/'

    def latest(self, base=None, symbols=None, date=None):
        if date:
            try:
                conv_date = datetime.strptime(date, self.date_format)
            except ValueError:
                raise ValueError('Wrong date format, shoud be {}'.format(self.date_format))
            if not (self.min_date <= conv_date <= datetime.today()):
                raise ValueError('Too old/new date. Min date: {0} Max date(today): {1}'.format(self.min_date, datetime.today()))
        req = date if date else 'latest'
        if base:
            if base not in self._allowed_curr:
                raise ValueError("Currency {} is not supported".format(base))
            req += '?base={}'.format(base)
        if symbols:
            for symb in symbols:
                if symb not in self._allowed_curr:
                    raise ValueError("Currency {} is not supported".format(base))
            req += '&' if base else '?'
            req += 'symbols={}'.format(','.join(symbols))
        return self._request(req)

    def convert(self, cur_from, cur_to, amount=1.0, date=None):
        if cur_from not in self._allowed_curr:
            raise ValueError("Currency {} is not supported".format(cur_from))
        if cur_to not in self._allowed_curr:
            raise ValueError("Currency {} is not supported".format(cur_to))
        resp = self.latest(base=cur_from, symbols=[cur_to], date=date)
        if 'rates' in resp and cur_to in resp['rates']:
            return float(resp['rates'][cur_to]) * amount
        return None

    @classmethod
    def get_allowed_curr(cls):
        return cls._allowed_curr

    def _request(self, req):
        resp = None
        print('req: {}'.format(req))
        try:
            r = requests.get(self.api_url + req)
            resp = json.loads(r.content.decode('utf-8'))
        except:
            print('exception in _request')
        return resp


def main():
    f = Fixer()
    print(f.convert('EUR', 'RUB', 1000))
    print(f.convert('EUR', 'RUB', 1000, '2014-01-03'))
    print(f.latest())
    print(f.latest(base='EUR', symbols=['EUR', 'RUB'],  date='2014-01-03'))

if __name__ == '__main__':
    main()
