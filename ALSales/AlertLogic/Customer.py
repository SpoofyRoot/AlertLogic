import json
import urllib2
import base64
import time
import datetime

class Customer(object):
    def __init__(self, api_key):
        self.api_key = base64.encodestring('%s:' % api_key).replace('\n', '')
        self.user_agent = "SalesMonitoringAgent"

    def request(self, endpoint):
        """

        :rtype : json string
        """
        request = urllib2.Request(endpoint)
        request.add_header("Authorization", "Basic %s" % self.api_key)
        request.add_header('User-Agent', self.user_agent)
        request.add_header('Accept', 'application/json')
        response = urllib2.urlopen(request)
        return response.read().decode('utf8')

    def postRequest(self, endpoint, data):
        """

        :rtype : json string
        """
        request = urllib2.Request(endpoint)
        request.add_header("Authorization", "Basic %s" % self.api_key)
        request.add_header('User-Agent', self.user_agent)
        request.add_header('Accept', 'application/json')
        response = urllib2.urlopen(request,data)
        return response.read().decode('utf8')

    def get(self, cust_id):
        data = self.request('https://api.alertlogic.net/api/customer/v1/' + cust_id)
        return json.loads(data)

    def create(self,name):
        d = {'customer_name':name}
        data = json.dumps(d)
        return json.loads(self.postRequest('https://api.alertlogic.net/api/customer/v1/',data))