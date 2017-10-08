#!/usr/bin/env python
"""
"""
import os
import json
import base64
import requests
import numpy as np
import CeleryPy
from CeleryPy import log
import ENV






class DB(object):
    
    def __init__(self):
        """Set initial attributes."""
        self.plants = {'known': [], 'save': [],
                       'remove': [], 'safe_remove': []}
        self.water_seq = {'seq_id': []}
        self.seq = {'all_sequences' : []}
        self.sorted_coords = {'sorted':[]}
        self.found_sequence=0

        self.seq_number = 0

        # API requests setup
        try:
            api_token = os.environ['API_TOKEN']
        except KeyError:
 #           api_token = 'x.eyJpc3MiOiAiLy9zdGFnaW5nLmZhcm1ib3QuaW86NDQzIn0.x'
             api_token = 'eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJoZWhlMTIzNEBob3RtYWlsLmRlIiwiaWF0IjoxNTA3Mzc2NTY2LCJqdGkiOiI2ODQ1M2NiZC1kMTJkLTQxOTktYTdjNC1iNTY2ZDU1YzJmMDEiLCJpc3MiOiIvL215LmZhcm1ib3QuaW86NDQzIiwiZXhwIjoxNTEwODMyNTY2LCJtcXR0IjoibXF0dC5mYXJtYm90LmlvIiwib3NfdXBkYXRlX3NlcnZlciI6Imh0dHBzOi8vYXBpLmdpdGh1Yi5jb20vcmVwb3MvZmFybWJvdC9mYXJtYm90X29zL3JlbGVhc2VzL2xhdGVzdCIsImZ3X3VwZGF0ZV9zZXJ2ZXIiOiJodHRwczovL2FwaS5naXRodWIuY29tL3JlcG9zL0Zhcm1Cb3QvZmFybWJvdC1hcmR1aW5vLWZpcm13YXJlL3JlbGVhc2VzL2xhdGVzdCIsImJvdCI6ImRldmljZV8xNyJ9.zp9OTN54jIzx18efKaliu0EuPl0AnzX7igd0rxaON1pdEqzrbwg-zGRv-1DI2AmQhjpb_472pV86yA2QOiqahmzum8z259Y4IVB1HsVXwhIBzOuCDzXuD_hFToRxoqtbTU4ySDaCudH8nuODin9B0SjzJgqEay_R1P8qXgrhpZKIrzRuzrfgWZDLbeD7Vmqm-SDNg0vKe0dvYNTrHVF6Yc0rO807U9TKM0uBN5IiPlwUKf3UHHCV-C0-t0fcFFqKaVo0Q6SFZcqWucwcqu3uOtgkqM-h8uIDk1eQytUTvKK0MTZ56Kh91VTXQMy3_9MlViH866r70o72w5OzNqljTA'
        try:
            encoded_payload = api_token.split('.')[1]
            encoded_payload += '=' * (4 - len(encoded_payload) % 4)
            json_payload = base64.b64decode(encoded_payload).decode('utf-8')
            server = json.loads(json_payload)['iss']
        except:  # noqa pylint:disable=W0702
            server = '//my.farmbot.io'
        self.api_url = 'http{}:{}/api/'.format(
            's' if 'localhost' not in server else '', server)
        self.headers = {'Authorization': 'Bearer {}'.format(api_token),
                        'content-type': "application/json"}
        self.errors = {}

    def api_get(self, endpoint):
        """GET from an API endpoint."""
        response = requests.get(self.api_url + endpoint, headers=self.headers)
        self.api_response_error_collector(response)
        self.api_response_error_printer()
        return response

    def api_response_error_collector(self, response):
        """Catch and log errors from API requests."""
        self.errors = {}  # reset
        if response.status_code != 200:
            try:
                self.errors[str(response.status_code)] += 1
            except KeyError:
                self.errors[str(response.status_code)] = 1

    def api_response_error_printer(self):
        """Print API response error output."""
        error_string = ''
        for key, value in self.errors.items():
            error_string += '{} {} errors '.format(value, key)
        print(error_string)





 
    def load_plants_from_web_app(self):
        """Download known plants from the FarmBot Web App API."""
        response = self.api_get('points')
        app_points = response.json()
        if response.status_code == 200:
            plants = []
            for point in app_points:
                if point['pointer_type'] == 'Plant':
                    plants.append({
                        'x': point['x'],
                        'y': point['y'],})
                        #'radius': point['radius']})            #We don't need radius for watering.
            self.plants['known'] = plants
            self.sorted_coords = sorted(self.plants['known'])



    def count_downloaded_plants(self):
        plant_count = len(self.plants['known'])
        log( "{} plants were detected." .format(plant_count)
            ,message_type= 'info',title= 'Water-everything')
             
       

        


    def load_sequences_from_app(self):
        water_seq = []
        sequences = []
        response = self.api_get('sequences')
        app_sequences = response.json()
        if response.status_code == 200:
            for seq in app_sequences:
                if seq['kind'] == 'sequence':
                 sequences.append({
                   'sequence_name': seq['name'],
                   'sequence_id' : seq['id']})
                if seq['name'] == 'FW_water_everything':
                  water_seq.append(seq['id'])
                  log("Sequence found.", message_type= 'info', title= 'Water-everything')
                  self.found_sequence=1
                  

                if self.found_sequence == 0:    
                    water_seq[:] = []

                  
                if self.found_sequence == 1:
                    [int(i) for i in water_seq]
                    self.seq_number = int(i)




       
           

    def loop_plant_points(self): 
        #count = 0                               Counter to limit the points for tests.      
        if self.found_sequence == 1 :
            for plant in self.sorted_coords:
                #if count < 3:
                   CeleryPy.move_absolute(
                    location=[plant['x'],plant['y'] ,0],
                    offset=[0, 0, 0],
                    speed=800)
                   CeleryPy.execute_sequence(sequence_id= self.seq_number)
                   #count +=1
        else:
            log("Can't find sequence called 'FW_water_everything'", message_type= 'error', title= 'Water-everything')            


          