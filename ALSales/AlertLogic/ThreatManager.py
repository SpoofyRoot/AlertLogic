import json
import urllib2
import base64
import requests
from requests.packages import urllib3

class AlertLogicTm(object):
    def __init__(self, api_key):
        self.api_key = base64.encodestring('%s:' % api_key).replace('\n', '')
        self.user_agent = "SalesMonitoringAgent"
        self.headers = {'Authorization': "Basic %s" % self.api_key }
        self.headers['Content-type'] = 'application/json'
        self.headers['Accept'] = 'application/json'
        urllib3.disable_warnings()

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

    def bytesto(self,bytes, to, bsize=1024):
        """convert bytes to megabytes, etc.
           sample code:
               print('mb= ' + str(bytesto(314575262000000, 'm')))

           sample output:
               mb= 300002347.946
        """

        a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
        r = float(bytes)
        for i in range(a[to]):
            r = r / bsize

        return(r)

    def GetAppliances(self, CustID=None):
        url = 'https://publicapi.alertlogic.net/api/tm/v1/appliances'
        if(CustID != None):
                url = 'https://publicapi.alertlogic.net/api/tm/v1/' + str(CustID) + '/appliances/'
        data = requests.get(url,headers=self.headers,verify=False)
        return json.loads(data.text)

    def GetPolicies(self, CustID=None):
        url = 'https://publicapi.alertlogic.net/api/tm/v1/policies/'
        if(CustID != None):
                url = 'https://publicapi.alertlogic.net/api/tm/v1/' + str(CustID) + '/policies/'
        data = requests.get(url,headers=self.headers,verify=False)
        return json.loads(data.text)

    def GetProtectedHosts(self,CustID=None):
        url = 'https://publicapi.alertlogic.net/api/tm/v1/protectedhosts/'
        if(CustID != None):
            url = 'https://publicapi.alertlogic.net/api/tm/v1/' + CustID + '/protectedhosts/'
        data = requests.get(url,headers=self.headers,verify=False)
        return json.loads(data.text)

    """
    Code updates assignment policy, can be modified to include appliances, 
    change policy name, or add other data with minor changes.  
    appliances is expected to be a list of appliance UUIDs 
    """
    def UpdateAssignmentPolicy(self,id,name,appliances=None):
        policyData = {"name":name,"type":"appliance_assignment"}
        applianceList = []
        if(appliances != None):
            for appliance in appliances:
                applianceList.append(appliance)
            policyData['appliances'] = applianceList
        url = "https://publicapi.alertlogic.net/api/tm/v1/policies/" + id
        policy = {'policy':policyData}
        r = requests.post(url, data=json.dumps(policy), headers=self.headers, verify=False)

    """
    method to update host policy name
    """
    def UpdateHostPolicy(self,id,name,tags=None):
        policyData = {"name":name,"type":"tmhost"}
        policyData['tmhost'] = {'encrypt': True}

        # if we have tags add them
        tagList = []
        for tag in tags:
            tagList.append({'name':tag})
        if(len(tagList>0)):
            policyData['tags'] = tagList
        policy = {'policy':policyData}
        url = "https://publicapi.alertlogic.net/api/tm/v1/policies/" + id
        r = requests.post(url, data=json.dumps(policy), headers=self.headers, verify=False)

    @property
    def appliances(self):
        url = 'https://publicapi.alertlogic.net/api/tm/v1/appliances'
        app = Appliances(self.request(url))
        return app.appliances

    
    @property
    def protectedhosts(self):
        url = 'https://publicapi.alertlogic.net/api/tm/v1//protectedhosts'
        hosts = ProtectedHosts(self.request(url))
        return hosts

class Policies(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

class Appliances(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
        
    def bytesto(self,bytes, to, bsize=1024):
        a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
        r = float(bytes)
        for i in range(a[to]):
            r = r / bsize
        return(r)

    @property
    def count(self):
        return len(self.__dict__['appliances'])

    @property
    def Status(self):
        error = 0
        ok = 0
        warning = 0
        new = 0
        offline = 0
        for i in self.__dict__['appliances']:
            if i['appliance']['status']['status'] == 'ok':
                ok = ok + 1
            if i['appliance']['status']['status'] == 'error':
                error = error + 1
            if i['appliance']['status']['status'] == 'offline':
                offline = offline + 1
            if i['appliance']['status']['status'] == 'warning':
                warning = warning + 1
            if i['appliance']['status']['status'] == 'new':
                new = new + 1
        d = {'error':error,'offline':offline,'new':new,'warning':warning,'ok':ok}
        return d

    @property
    def totalMonthMBytes(self):
        self.total = 0
        for i in self.__dict__['appliances']:
            if 'last_month_total_bytes' in i['appliance']['stats'].keys():
                self.total = self.total + i['appliance']['stats']['last_month_total_bytes']
        return self.bytesto(self.total,'m')

    @property
    def totalDayMBytes(self):
        self.total = 0
        for i in self.__dict__['appliances']:
            if 'last_day_total_bytes' in i['appliance']['stats'].keys():
                self.total = self.total + i['appliance']['stats']['last_day_total_bytes']
        return self.bytesto(self.total,'m')






class Sources(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

    @property
    def count(self):
        return len(self.__dict__['sources'])

    @property
    def totalMonthMBytes(self):
        self.total = 0
        for i in self.__dict__['sources']:
            if 'last_month_total_bytes' in i['source']['stats'].keys():
                self.total = self.total + i['source']['stats']['last_month_total_bytes']
        return self.bytesto(self.total,'m')

    @property
    def totalDayMBytes(self):
        self.total = 0
        for i in self.__dict__['sources']:
            if 'last_day_total_bytes' in i['source']['stats'].keys():
                self.total = self.total + i['source']['stats']['last_day_total_bytes']
        return self.bytesto(self.total,'m')

class ProtectedHosts(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
    @property
    def count(self):
        return len(self.__dict__['protectedhosts'])

    @property
    def totalMonthMBytes(self):
        self.total = 0
        for i in self.__dict__['protectedhosts']:
            if 'last_month_total_bytes' in i['protectedhost']['stats'].keys():
                self.total = self.total + i['protectedhost']['stats']['last_month_total_bytes']
        return self.bytesto(self.total,'m')

    @property
    def Status(self):
        total = 0
        error = 0
        ok = 0
        warning = 0
        new = 0
        offline = 0
        
        for i in self.__dict__['protectedhosts']:
            if i['protectedhost']['status']['status'] == 'error':
                error = error + 1
            if i['protectedhost']['status']['status'] == 'ok':
                ok = ok + 1
            if i['protectedhost']['status']['status'] == 'warning':
                warning = warning + 1
            if i['protectedhost']['status']['status'] == 'new':
                new = new + 1
            if i['protectedhost']['status']['status'] == 'offline':
                offline = offline + 1
        d = {'error':error,'offline':offline,'new':new,'warning':warning,'ok':ok}
        return d

    @property
    def totalDayMBytes(self):
        self.total = 0
        for i in self.__dict__['protectedhosts']:
            if 'last_day_total_bytes' in i['protectedhost']['stats'].keys():
                self.total = self.total + i['protectedhost']['stats']['last_day_total_bytes']
        return self.bytesto(self.total,'m')