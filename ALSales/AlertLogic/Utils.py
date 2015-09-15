import requests
import time
from requests.packages import urllib3
urllib3.disable_warnings()
class Utils():
    '''
    Datacenter is either us or uk. 
    name is the name of the appliance. Avoid using special characters
    and make sure the name is not over 15 chars long. 
    IP of course is the ip address of the host
    '''
    def ClaimAppliance(self,ip,apikey,datacenter,name):
        url = 'http://' + ip + '/aws.php'
        data = {'dcpost': datacenter,'app_name': name ,'reg_key':apikey}
        r = requests.post(url, data=data)
    """
    Return true if the appliance is bootstrapping
    """
    def IsBootStrapping(self,ip):
        url = 'http://' + ip + '/'
        r = requests.get(url)

        if(r.text.find('Bootstrap') < 0):
            return False
        return True
    
    """
    Loop waiting for appliance to come online and claim it. 
    """
    def WaitAndClaim(self,ip,apikey,datacenter,name):

        status = True
        while status:
            try:
                status = self.IsBootStrapping(ip)
                print("Appliance is bootstrapping, waiting")
                time.sleep(60)
            except requests.exceptions.RequestException as e:
                print("Appliance is offline, waiting")
                pass

        if(status == False):
            print("Claiming appliance")
            self.ClaimAppliance(ip,apikey,datacenter,name)
    '''
    Datacenter is either us or uk. 
    name is the name of the appliance. Avoid using special characters
    and make sure the name is not over 15 chars long. 
    IP of course is the ip address of the host
    '''
    def ClaimWSMAppliance(self,ip,apikey,datacenter,name):
        url = 'https://' + ip + ':4849/aws.php'
        data = {'dcpost': datacenter,'app_name': name ,'reg_key':apikey}
        r = requests.post(url, data=data,verify=False)
    """
    Return true if the appliance is bootstrapping
    """
    def IsWSMBootStrapping(self,ip):
        url = 'https://' + ip + ':4849'
        r = requests.get(url,verify=False)

        if(r.text.find('Bootstrap') < 0):
            return False
        return True
    
    """
    Loop waiting for appliance to come online and claim it. 
    """
    def WaitAndClaimWSM(self,ip,apikey,datacenter,name):

        status = True
        while status:
            try:
                status = self.IsWSMBootStrapping(ip)
                print("Appliance is bootstrapping, waiting")
                time.sleep(60)
            except requests.exceptions.RequestException as e:
                print("Appliance is offline, waiting")
                pass

        if(status == False):
            print("Claiming appliance")
            self.ClaimWSMAppliance(ip,apikey,datacenter,name)

