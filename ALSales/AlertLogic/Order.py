import requests
import base64
import json

class Order(object):
    def __init__(self, api_key):
        self.api_key = base64.encodestring('%s:' % api_key).replace('\n', '')
        self.headers = {'Authorization': "Basic %s" % self.api_key }
        self.headers['Content-type'] = 'application/json'
        self.headers['Accept'] = 'application/json'


    def Create(self,custid,name,public_ip):
        endpoint = 'https://api.alertlogic.net/api/order/v2'
        sku = {'sku':name,'public_ip':public_ip, 'claim_type':'post'}
        d = {'customer_id':custid}
        skuList = []
        skuList.append(sku)
        d['skus'] = skuList
        data = json.dumps(d)
        r = requests.post(endpoint,data=data, headers=self.headers, verify=False)
        print r.text
        return r