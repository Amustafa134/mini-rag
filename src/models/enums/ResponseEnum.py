from enum import Enum

class ResponseeSignal(Enum):
    

    # General response signals
    FILE_VALIDATED_SUCCESS = "File validated successfully"
    FILE_TYPE_NOT_SUPPORTED = "File Type Not Supported"
    FILE_SIZE_EXCEEDED = "File size exceeded"
    FILE_UPLOAD_SUCCESS = "File upload successful"
    FILE_UPLOAD_FAILED = "File upload failed"
    PROCESSING_SUCCESS = "Processing successful"
    PROCESSING_FAILED = "Processing failed"
    NO_FILES_FOUND = "No files found for the project"
    FILE_ID_ERROR = "No file_id provided or file_id is not a string"