# Import base controller and necessary libraries
from .BaseController import BaseController
from fastapi import UploadFile
from models import ResponseeSignal
import os

class ProjectController(BaseController):
    
    def __init__(self):
        # Inherit initialization from BaseController
        super().__init__()

    def get_project_path(self, project_id: str):
        
        project_dir = os.path.join(
            self.file_dir,
            project_id
        )  # Construct the project directory path using the file directory and project ID
        
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)  # Create the project directory if it does not exist

        return project_dir
