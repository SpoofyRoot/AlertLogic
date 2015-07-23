import json
import urllib2
import base64
import PasswordGenerator as pg

class User(object):
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

    def delRequest(self,endpoint):
        request = urllib2.Request(endpoint)
        request.add_header("Authorization", "Basic %s" % self.api_key)
        request.add_header('User-Agent', self.user_agent)
        request.add_header('Accept', 'application/json')
        request.get_method = lambda: 'DELETE'
        response = urllib2.urlopen(request)
        return response.read()

    def create(self,cust_id,firstName,lastName,email):
        password=pg.generate_pass()
        cust = { "customer_id": cust_id,"first_name": firstName,"last_name": lastName,"email": email ,"password": password}
        data = json.dumps(cust)
        resp = json.loads(self.postRequest('https://api.alertlogic.net/api/user/v1',data))
        print('User ID is %d for %s and password is %s ' % (resp['user_id'],cust['email'],password))

    def get(self):
        data = self.request('https://api.alertlogic.net/api/user/v1')
        print json.loads(data)

    def delete(self,user_id):
        url = 'https://api.alertlogic.net/api/user/v1/' + str(user_id)
        return self.delRequest(url)
        



