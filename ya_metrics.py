# https://alexeygorodinsky.github.io/

import requests


APP_ID = '177521d4e0a041d99e9e421ff838282d'
METRICS_URL = 'https://api-metrika.yandex.ru/stat/v1/data'
COUNTERS_URL = 'https://api-metrika.yandex.ru/management/v1/counters'
TOKEN = 'AQAAAAACK3jIAAUTprL9QNfgS0NWsAYSk6jSSvs'


class YaMetricsManagment:
    metrics_url = METRICS_URL
    counters_url = COUNTERS_URL

    def __init__(self, token):
        self.token = token
        self.headers = self.get_headers()

    def get_headers(self):
        return {'Authorization': 'OAuth{}'.format(self.token)}

    def get_request(self, url, params=None):
        return requests.get(url, params=params, headers=self.headers)

    def get_counters(self):
        return self.get_request(self.counters_url)

    @staticmethod
    def metrics_counter(data):
        print(data['data'][0]['metrics'])


class YaMetricsReports(YaMetricsManagment):

    def __init__(self, token, counter_id):
        self.counter_id = counter_id
        super().__init__(token)

    def get_metrics_data(self, metrics):
        params = {
            'id': self.counter_id,
            **metrics
        }
        return self.get_request(self.metrics_url, params).json()

    def get_visits_stat(self):
        return self.get_metrics_data({'metrics': 'ym:s:visits'})

    def get_views_stat(self):
        return self.get_metrics_data({'metrics': 'ym:s:pageviews'})

    def get_users_stat(self):
        return self.get_metrics_data({'metrics': 'ym:s:users'})


metrics_counter = YaMetricsReports.metrics_counter
counters_list = [c['id'] for c in YaMetricsManagment(TOKEN).get_counters().json()['counters']]

for counter_id in counters_list:
    ya_reports = YaMetricsReports(TOKEN, counter_id)
    print('Номер счетчика:{}'.format(counter_id))
    print('Количество посещений страницы:')
    metrics_counter(ya_reports.get_visits_stat())
    print('Число просмотров страницы:')
    metrics_counter(ya_reports.get_views_stat())
    print('Число посетителей:')
    metrics_counter(ya_reports.get_users_stat())
