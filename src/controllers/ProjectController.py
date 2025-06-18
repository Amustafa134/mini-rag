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
        project_dir = os.path.join(self.file_dir, project_id)
        # return project_dir
        # Construct the full directory path for the given project ID
        project_dir = os.path.join(
            self.file_dir,
            project_id

        )    
        # return project_dir
        # If the directory doesn't exist, create it
        # if not os.path.exists(project_dir):
        os.makedirs(project_dir, exist_ok=True)

            # Return the final directory path (exists now in all cases)
        return project_dir
        