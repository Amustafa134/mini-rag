# Import settings helper and standard libraries
from helpers.config import get_settings, Settings
import os
import random
import string


class BaseController:
    def __init__(self):

        # Load application settings from config
        self.app_settings = get_settings()

        # Set base directory two levels up from the current file
        self.base_dir = os.path.dirname(os.path.dirname(__file__))

        # Define the directory for storing files under assets/files
        self.file_dir = os.path.join(
           self.base_dir ,
           "assets/files"
        )
        
    def generate_random_string(self, length: int = 12):
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k = length))
    