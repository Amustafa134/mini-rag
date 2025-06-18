# Import necessary FastAPI modules and helpers
from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
import aiofiles  # Async file I/O
import logging

logger = logging.getLogger("uvicorn.error")     # Use Uvicorn's logger for consistent logging

# Import application settings and controllers
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController
from models import ResponseeSignal   # Enum for standardized response signals

# Define the router for data-related API endpoints
data_router = APIRouter(
    prefix = "/api/v1/data",    # Base path for this router
    tags = ["api_v1", "data"],  # Tags for grouping in Swagger docs
)

# Endpoint: Upload a file associated with a specific project
@data_router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    

    # Create an instance of the data controller
    datacontroller = DataController()
    
    # Validate file type and size
    is_valid, result_signal = await datacontroller.validate_upload_file(file=file)


    # If validation fails, return 400 Bad Request with the failure signal
    if not is_valid:
        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
            "Signal": result_signal
            }
        
        )

    # Retrieve the directory path where the file should be saved
    project_dir_path = ProjectController().get_project_path(project_id = project_id)
    
    # Generate a unique file path for the upload
    file_path, file_id = datacontroller.generate_unique_filepath(
        orig_file_name = file.filename,
        project_id = project_id
    )
    
    try:
        # Save the uploaded file in chunks to avoid memory overload
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)

    except Exception as e:   
        
        # Log any file writing issues and return a failure response
        logger.error(f"Error while upload file: {e}")

        return JSONResponse(
            status_code = status.HTTP_400_BAD_REQUEST,
            content = {
            "Signal": ResponseeSignal.FILE_UPLOAD_FAILED.value
            }
        
        )        

    # Return a success signal if file was uploaded successfully
    return JSONResponse(
        content = {
        "Signal": ResponseeSignal.FILE_UPLOAD_SUCCESS.value,
        "file_id": file_id
        }
    )