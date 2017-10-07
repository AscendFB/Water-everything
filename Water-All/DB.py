#!/usr/bin/env python
"""
"""
import os
import json
import base64
import requests
import numpy as np
from plant_detection import CeleryPy
from plant_detection import ENV
f


class DB(object):
    
    def __init__(self):
        """Set initial attributes."""
        self.plants = {'known': [], 'save': [],
                       'remove': [], 'safe_remove': []}
        self.water_seq = {'seq_id': []}
        self.seq = {'ready_seq' : []}

        self.seq_number = []

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
                        'y': point['y'],
                        'radius': point['radius']})
            self.plants['known'] = plants


    def count_downloaded_plants(self):
        plant_count = len(self.plants[plants])
        log(plant_count,message_type= 'info',title= 'Water-All')
        
          
       

    def print_identified(self):
        """Output text including data about identified detected plants."""
        def _identified_plant_text_output(title, action, plants):
            print("\n{} {}.".format(
                len(self.plants[plants]), title))
            if len(self.plants[plants]) > 0:
                print("Plants at the following machine coordinates "
                      "( X Y ) with R = radius {}:".format(action))
            for plant in self.plants[plants]:
                print("    ( {x:5.0f} {y:5.0f} ) R = {r:.0f}".format(
                    x=plant['x'],
                    y=plant['y'],
                    r=plant['radius']))

                  


        # Print known
        _identified_plant_text_output(
            title='known plants inputted',
            action='are to be saved',
            plants='known')




    def load_sequences_from_app(self):
        response = self.api_get('sequences')
        app_sequences = response.json()
        if response.status_code == 200:
            sequences = []
            water_seq = []
            for seq in app_sequences:
                if seq['kind'] == 'sequence':
                 sequences.append({
                   'sequence_name': seq['name'],
                   'sequence_id' : seq['id']})
                if seq['name'] == 'FW_water_all':
                    water_seq.append({
                        seq['id']})
            self.seq['ready_seq'] = sequences
            self.water_seq['seq_id'] = water_seq
            #print (self.water_seq['seq_id'])
            self.seq_number = seq[u'id']
            print (self.seq_number)




    #def ex_sequence(self):
    #    CeleryPy.execute_sequence(sequence_id=self.seq_number)                                    
                    

            

    def loop_plant_points(self): 
        count =0
        plant_count=len(self.plants['known'])
        while count<2:                   
                for plant in self.plants['known']:
                      CeleryPy.move_absolute(
                    location=[plant['x'],plant['y'] ,0],
                    offset=[0, 0, 0],
                    speed=800)
                      count+=1

                      CeleryPy.execute_sequence(sequence_id=self.seq_number)
                      #self.water_sequence()

                      
                                       
                
                                
                                     
    def water_sequence(self):
                      CeleryPy.write_pin(number=10,value=1,mode=0)
                      CeleryPy.wait(5000)
                      CeleryPy.write_pin(number=10,value =0,mode =0)        