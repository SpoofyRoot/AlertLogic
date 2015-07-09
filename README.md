# AlertLogic API wrappers in Python
This is a simple set of wrappers for the Alert Logic API's in python.  This code is very early stage so use at your own risk.

Information about the various APIs can be found [online.](https://www.alertlogic.com/developer/) Alert Logic has a fairly large API set and I cover some of the more common functions here. I'll add support for other API's as I see fit.  

##Incident API Example 
```
>>> AlApiKey = 'yourApiKey'
>>> import Incidents as alIncidents
>>> inc = alIncidents.IncidentAPI(AlApiKey)
>>> incidents = inc.GetIncidents()
>>> incidents = inc.GetIncidents('06/01/2015','07/01/2015')
>>> incidents.Attackers
[[u'10.5.8.35'], [u'79.133.219.113'], [u'31.170.163.50'], [u'213.205.38.24', u'27.54.85.33', u'66.63.184.228', u'69.24.208.13', u'74.125.113.106', u'74.207.228.136', u'85.86.198.106'], [u'78.140.131.159'], [u'10.2.184.139'], [u'10.1.184.139'], [u'192.168.11.1', u'192.168.11.130'], [u'79.133.219.113'], [u'213.205.38.24', u'27.54.85.33', u'66.63.184.228', u'69.24.208.13', u'74.125.113.106', u'74.207.228.136', u'85.86.198.106']]
>>> incidents.Victims
[[u'10.5.8.48'], [u'192.168.0.2'], [u'10.0.0.6'], [u'172.29.0.116'], [u'10.0.2.15'], [u'10.2.184.143'], [u'10.1.184.143'], [u'192.168.11.128'], [u'192.168.0.2'], [u'172.29.0.116']]
>>> 
```

##Log Manager API Example
```
>>> import LogManager as LM
>>> lm = LM.AlertLogicLm(AlApiKey)
>>> lmSources = lm.GetSources()
>>> lmSources.count
147
>>> lmSources.Types
{'Windows': 0, 'Syslog': 146, 'FlatFile': 0, 'S3': 0, 'CloudTrail': 1}
>>> 
```

##Threat Manager API Example 
```
>>> import ThreatManager as TM
>>> tm = TM.AlertLogicTm(AlApiKey)
>>> tmAppliances = tm.GetAppliances()
>>> tmAppliances.Status
{'new': 0, 'offline': 2, 'warning': 0, 'ok': 3, 'error': 0}
>>> tmAppliances.totalMonthMBytes
4772.830846786499
>>> 
```

you get the idea. 

