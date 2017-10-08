import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from CeleryPy import log
from DB import DB







if __name__ == "__main__":

    log("Lets do this.", message_type='info', title='Water-everything')

    

    plantdb= DB()

    plantdb.load_plants_from_web_app()   #Get plant points from Webapp
    plantdb.count_downloaded_plants()    #Print Plantcount in log
    plantdb.load_sequences_from_app()    #Get sequences and determine the sequence id
    plantdb.loop_plant_points()          #Move to plant points and water them with the Water on/off sequence
