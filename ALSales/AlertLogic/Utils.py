import requests

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