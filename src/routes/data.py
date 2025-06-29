# Import necessary FastAPI modules and helpers
from fastapi import FastAPI, APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import os
import aiofiles  # Async file I/O
import logging
from .schemes.data import ProcessRequest


# Import application settings and controllers
from helpers.config import get_settings, Settings
from controllers import DataController, ProjectController, ProcessController
from models import ResponseeSignal  # Enum for standardized response signals
from models.ProjectModel import ProjectModel
from models.ChunkModel import ChunkModel
from models.db_schemes import DataChunk
# from models.db_schemes import datachunk as DataChunk



# Use Uvicorn's logger for consistent error/output logging
logger = logging.getLogger("uvicorn.error")

# Define the router for data-related API endpoints
data_router = APIRouter(
    prefix="/api/v1/data",    # Base path for this router
    tags=["api_v1", "data"],  # Tags for grouping in Swagger docs
)

@data_router.get("/welcome/{project_id}")
async def project_welcome(project_id: str):
    return {"message": f"Welcome to project {project_id}"}

# ----------------------------------------------
# Endpoint: Upload a file to a specific project
# ----------------------------------------------

@data_router.post("/upload/{project_id}")
async def upload_data(request: Request, project_id: str, file: UploadFile,
                      app_settings: Settings = Depends(get_settings)):
    
    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )

    # Create an instance of the data controller
    datacontroller = DataController()
    
    # Validate file type and size
    is_valid, result_signal = datacontroller.validate_upload_file(file=file)

    # If validation fails, return 400 with the failure signal
    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal": result_signal
            }
        )

    # Determine the path to store the uploaded file
    project_dir_path = ProjectController().get_project_path(project_id=project_id)

    # Generate a unique file path and ID for the file
    file_path, file_id = datacontroller.generate_unique_filepath(
        orig_file_name=file.filename,
        project_id=project_id
    )

    try:
        # Save file in chunks to prevent memory overload
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
    
        # Log the error and return failure response
        logger.error(f"Error while uploading file: {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal": ResponseeSignal.FILE_UPLOAD_FAILED.value
            }
        )

    # Return success signal along with file ID
    return JSONResponse(
        content={
            "Signal": ResponseeSignal.FILE_UPLOAD_SUCCESS.value,
            "file_id": file_id,
        }
    )


# ----------------------------------------------
# Endpoint: Process a previously uploaded file
# ----------------------------------------------

@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request, project_id: str, process_request: ProcessRequest):

    # Extract parameters from the request body
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset



    project_model = await ProjectModel.create_instance(
        db_client=request.app.db_client
    )

    project = await project_model.get_project_or_create_one(
        project_id=project_id
    )


    # Create an instance of the process controller
    process_controller = ProcessController(project_id=project_id)

    # Load the contents of the file
    file_content = process_controller.get_file_content(file_id=file_id)

    # Process file into text chunks
    file_chunks = process_controller.process_file_content( 
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    # Handle processing failure
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "Signal": ResponseeSignal.PROCESSING_FAILED.value
            }
        )
    
    # Insert processed chunks into the database
    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,  # Start order from 1
            chunk_project_id=project.id,
        )
        for i, chunk in enumerate(file_chunks)
    ]

    chunk_model = await ChunkModel.create_instance(
        db_client=request.app.db_client
    )

    if do_reset == 1:
        _ = await chunk_model.delete_chunks_by_project_id(
            project_id=project.id
        )

    # Insert the chunks into the database
    no_records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)
    
    # Return success response with number of records processed
    return JSONResponse(
        content={
            "signal": ResponseeSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records
        }
    )
