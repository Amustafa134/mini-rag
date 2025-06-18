from enum import Enum

class ResponseeSignal(Enum):
    
    
    FILE_TYPE_NOT_SUPPORTED = "File Type Not Supported"
    FILE_SIZE_EXCEEDED = "File size exceede"
    FILE_UPLOAD_SUCCESS = "File upload success"
    FILE_UPLOAD_FAILED = "File upload failed"
    FILE_VALIDATED_SUCCESS = "File validated successfuly"