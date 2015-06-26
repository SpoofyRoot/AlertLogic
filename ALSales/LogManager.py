import json
import urllib2
import base64

class AlertLogicLm(object):
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

    def GetAppliances(self):
        url = 'https://publicapi.alertlogic.net/api/lm/v1/appliances'
        app = Appliances(self.request(url))
        return app

    def GetCredentials(self):
        url = 'https://publicapi.alertlogic.net/api/lm/v1/credentials'
        app = Credentials(self.request(url))
        return app
    def GetSources(self):
        url = 'https://publicapi.alertlogic.net/api/lm/v1/sources'
        app = Sources(self.request(url))
        return app
    def GetPolicies(self):
        url = 'https://publicapi.alertlogic.net/api/lm/v1/policies'
        app = Policies(self.request(url))
        return app


class Appliances(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
        self._count = None
    
    @property
    def count(self):
        return len(self.__dict__['appliances'])

class Credentials(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
        self._count = None
    @property
    def count(self):
        return len(self.__dict__['credentials'])

class Sources(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
        self._count = None

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

    @property
    def totalMonthMBytes(self):
        self.total = 0
        for i in self.__dict__['sources']:
            for value in i.itervalues():
                self.total = self.total + value['stats']['last_month_bytes']
        return self.bytesto(self.total,'m')
    @property
    def count(self):
        return len(self.__dict__['sources'])

    @property
    def Types(self):
        typeWindows = 0
        typeSyslog = 0
        typeFlatFile = 0
        typeS3 = 0
        typeCloudTrail = 0
        numberOfSources = 0
       
        for i in self.__dict__['sources']:
            numberOfSources= numberOfSources + 1
            if i.get('eventlog'):
                typeWindows = typeWindows + 1
            if i.get("s3aws"):  
                typeCloudTrail = typeCloudTrail + 1
            if i.get("syslog"):
                typeSyslog = typeSyslog + 1
            if i.get("flatfile"):
                typeFlatFile = typeFlatFile + 1
            if i.get('s3'):
                typeS3 = typeS3 + 1
        d = {}
        d['Windows'] = typeWindows
        d['CloudTrail'] = typeCloudTrail
        d['Syslog'] = typeSyslog
        d['S3'] = typeS3
        d['FlatFile'] = typeFlatFile
        return d

    @property
    def Status(self):
        ok = 0
        offline = 0
        warning = 0
        new = 0
        error = 0
       
        for i in self.__dict__['sources']:
            if i.get('eventlog'):
                if i['eventlog']['status']['status'] == 'ok':
                    new = new + 1
                if i['eventlog']['status']['status'] == 'error':
                    error = error + 1
                if i['eventlog']['status']['status'] == 'warning':
                    warning = warning + 1
                if i['eventlog']['status']['status'] == 'offline':
                    offline = offline + 1
                if i['eventlog']['status']['status'] == 'ok':
                    ok = ok + 1
            if i.get("s3aws"): 
                if i['s3aws']['status']['status'] == 'ok':
                    new = new + 1
                if i['s3aws']['status']['status'] =='error':
                    error = error + 1
                if i['s3aws']['status']['status'] == 'warning':
                    warning = warning + 1
                if i['s3aws']['status']['status'] == 'offline':
                    offline = offline + 1
                if i['s3aws']['status']['status'] == 'ok':
                    ok = ok + 1
            if i.get("syslog"):
                if i['syslog']['status']['status'] == 'ok':
                    new = new + 1
                if i['syslog']['status']['status'] == 'error':
                    error = error + 1
                if i['syslog']['status']['status'] == 'warning':
                    warning = warning + 1
                if i['syslog']['status']['status'] == 'offline':
                    offline = offline + 1
                if i['syslog']['status']['status'] == 'ok':
                    ok = ok + 1
            if i.get("flatfile"):
                if i['flatfile']['status']['status'] == 'ok':
                    new = new + 1
                if i['flatfile']['status']['status'] == 'error':
                    error = error + 1
                if i['flatfile']['status']['status'] == 'warning':
                    warning = warning + 1
                if i['flatfile']['status']['status'] == 'offline':
                    offline = offline + 1
                if i['flatfile']['status']['status'] =='ok':
                    ok = ok + 1
            if i.get('s3'):
                if i['s3']['status']['status'] =='ok':
                    new = new + 1
                if i['s3']['status']['status'] == 'error':
                    error = error + 1
                if i['s3']['status']['status'] == 'warning':
                    warning = warning + 1
                if i['s3']['status']['status'] == 'offline':
                    offline = offline + 1
                if i['s3']['status']['status'] == 'ok':
                    ok = ok + 1
        d = {'ok':ok, 'warning':warning,'offline':offline,'error':error,'new':new}
        return d

class Policies(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)
        self._count = None

    @property
    def count(self):
        return len(self.__dict__['policies'])