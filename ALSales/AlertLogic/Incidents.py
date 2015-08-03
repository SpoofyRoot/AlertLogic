import json
import urllib2
import base64
import time
import datetime

class IncidentAPI(object):
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

    def DateToUnix(self, date):
        return int(time.mktime(datetime.datetime.strptime(date, "%m/%d/%Y").timetuple()))

    def GetIncidents(self,startDate,endDate):
        url = 'https://api.alertlogic.net/api/incident/v3/incidents'
        query = '?create_date=' + str(self.DateToUnix(startDate)) + '..' + str(self.DateToUnix(endDate))
        return Incidents(self.request(url+query))


class Incidents(object):
    def __init__(self, j):
        self.IncidentList = json.loads(j)

    @property
    def count(self):
        return len(self.IncidentList)
    @property
    def Threats(self):
        high = 0
        low = 0
        medium = 0
        critical = 0

        for i in self.IncidentList:
            if i['threat_rating'] == 'High':
                high = high + 1
            if i['threat_rating'] == 'Low':
                low = low + 1
            if i['threat_rating'] == 'Medium':
                medium = medium + 1
            if i['threat_rating'] == 'Critical':
                critical = critical + 1
        return {'High':high,'Low':low,'Medium':medium,'Critical':critical}

    @property
    def Victims(self):
        victList = []
        for i in self.IncidentList:
            victList.append(i.get('victims'))
        return victList

    @property
    def Attackers(self):
        attackers = []
        for i in self.IncidentList:
            attackers.append(i.get('attackers'))
        return attackers

    @property
    def Geoip(self):
        attackerGeo = []
        for i in self.IncidentList:
            attackerGeo.append(i.get('geoip'))
        return attackerGeo

       