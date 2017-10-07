import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

#from plant_detection.PlantDetection import PlantDetection
#from tests.test_celerypy import CeleryScript
from plant_detection.CeleryPy import log
from plant_detection.PlantDetection import PlantDetection
from new_test.DB import DB







if __name__ == "__main__":

    log("Lets do this.", message_type='info', title='Water-All')
    plantdb.count_downloaded_plants()
    

    plantdb= DB()

    plantdb.load_plants_from_web_app()   #Get plant points from Webapp
    plantdb.load_sequences_from_app()    #Get sequences and determine the sequence id
    plantdb.loop_plant_points()          #Move to plant points and water them with the Water on/off sequence
