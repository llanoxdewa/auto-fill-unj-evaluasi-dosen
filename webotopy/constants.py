# from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from enum import Enum 


# all expected events 
class Events(Enum):
    VISIBLE     = 1
    CLICKABLE   = 2
    EXISTS      = 3   


# maping the Events into EC object
EVENTS_MAP = {
    Events.VISIBLE      : EC.visibility_of_element_located,
    Events.CLICKABLE    : EC.element_to_be_clickable,
    Events.EXISTS       : EC.presence_of_element_located       
}

