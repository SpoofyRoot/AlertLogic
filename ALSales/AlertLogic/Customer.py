import json
import requests
import base64
from requests.packages import urllib3



class Customer(object):
    def __init__(self, api_key):
        self.api_key = base64.encodestring('%s:' % api_key).replace('\n', '')
        self.headers = {'Authorization': "Basic %s" % self.api_key }
        self.headers['Content-type'] = 'application/json'
        urllib3.disable_warnings()
        self.headers['Accept'] = 'application/json'


    def create(self,name):
        d = {'customer_name':name}
        url = 'https://api.alertlogic.net/api/customer/v1'
        r = requests.post(url, data=json.dumps(d), headers=self.headers, verify=False)
        print r.text
        return json.loads(r.text)

    def status(self,provisionId):
        data = requests.get('https://api.alertlogic.net/api/customer/v1/status/' + provisionId,headers=self.headers,verify=False)
        return json.loads(data.text)

    def get(self,customerId):
        data = requests.get('https://api.alertlogic.net/api/customer/v1/' + customerId,headers=self.headers,verify=False)
        return json.loads(data.text)