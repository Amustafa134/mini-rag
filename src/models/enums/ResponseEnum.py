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
    PROJECT_NOT_FOUND_ERROR = "Project not found"
    INSERT_INTO_VECTORDB_ERROR = "Insert into vectordb error"
    INSERT_INTO_VECTORDB_SUCCESS = "Insert into vectordb success"
    VECTORDB_COLLECTION_RETRIEVED = "VectorDB collection retrieved"
    VECTORDB_SEARCH_ERROR = "VectorDB Search Error"
    VECTORDB_SEARCH_SUCCESS = "VectorDB Search Success"