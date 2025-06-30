# Import base controllers and necessary modules

from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from models.enums.ProcessingEnum import ProcessingEnum
from models import ProcessingEnum


# LangChain document loaders and text splitter
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter 


class ProcessController(BaseController):

    def __init__(self, project_id: str):
        super().__init__()
        
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id=project_id)

    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]
    

    # def get_file_loader(self, file_id: str):

    #     file_ext = self.get_file_extension(file_id=file_id)
    #     file_path = os.path.join(
    #         self.project_path,
    #         file_id
    #     )

    #     if not os.path.exists(file_path):
    #         return None

    #     if file_ext == ProcessingEnum.TXT.value:
    #         # For text files, use TextLoader
    #         return TextLoader(file_path, encoding="utf-8")
        
    #     if file_ext == ProcessingEnum.PDF.value:
    #         return PyMuPDFLoader(file_path)
        
    #     return None  # Unsupported file type

    def get_file_loader(self, file_id: str):
        # Get the file name from the file_id from the database
        


        file_ext = self.get_file_extension(file_id)
        file_path = os.path.join(self.project_path, file_id)
        print(f"DEBUG loader: ext={file_ext}, path={file_path}")

        if not os.path.exists(file_path):
            return None

        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)

        return None
    
            
    # def get_file_content(self, file_id: str):

    #     loader = self.get_file_loader(file_id=file_id)
    #     if loader:
    #         return loader.load()
        
    #     return None  # Loader not found or unsupported file type

    def get_file_content(self, file_id: str):
        
        loader = self.get_file_loader(file_id)
        if loader is None:
            # Explicitly handle unsupported or missing files
            raise ValueError(f"No loader found for file: {file_id}")
        return loader.load()



    def process_file_content(
        self, file_content: list, file_id: str,
        chunk_size: int=100, overlap_size: int=20
    ):
    
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        # Extract content and metadata from each document
        file_content_texts = [
            rec.page_content 
            for rec in file_content
        ]
        
        file_content_metadata = [
            rec.metadata 
            for rec in file_content
        ]

        # Create overlapping chunks of text, retaining metadata
        chunks = text_splitter.create_documents(
            file_content_texts,
            metadatas=file_content_metadata
        )

        return chunks


