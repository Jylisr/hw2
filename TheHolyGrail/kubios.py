import urequests as requests
import ujson
import network
from time import sleep
from main import ppis

class Kubios:
    def __init__(self):
        pass

    def connect(self, ppis):
        APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
        CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
        CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"
        LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
        TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
        REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"

        response = requests.post(
         url = TOKEN_URL,
         data = 'grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
         headers = {'Content-Type':'application/x-www-form-urlencoded'},
         auth = (CLIENT_ID, CLIENT_SECRET))
        response = response.json() #Parse JSON response into a python dictionary

        access_token = response["access_token"] #Parse access token

        #Interval data to be sent to Kubios Cloud. Replace with your own data:

        intervals = ppis

        #Create the dataset dictionary HERE
        dataset = {
            "type": "RRI",
            "data": intervals,
            "analysis": {
                "type": "readiness"
                }
            } 
        
        #Make the readiness analysis with the given data

        response = requests.post(
         url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
         headers = { "Authorization": "Bearer {}".format(access_token), "X-Api-Key": APIKEY}, json = dataset) 
        response = response.json()
        #Print out the SNS and PNS values on the OLED screen here

        pns = response['analysis']['pns_index']
        sns = response['analysis']['sns_index']


    #The data sent to Kubios is the peak-to-peak intervals in milliseconds

