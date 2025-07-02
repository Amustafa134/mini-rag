from ..LLMInterface import LLMInterface
from openai import OpenAI
import logging


class OpenAIProvider(LLMInterface):
                                                 # "https://api.openai.com/v1"
    def __init__(
            self, api_key: str, api_url: str=None,
            defualt_input_max_characters: int=1000,
            defualt_generation_max_output_tokens: int=1000,
            defualt_generation_temperature: float=0.1,
    ):
        
        self.api_key = api_key
        self.api_url = api_url
        
        self.default_input_max_characters = defualt_input_max_characters
        self.default_generation_max_output_tokens = defualt_generation_max_output_tokens
        self.default_generation_temperature = defualt_generation_temperature

        self.generation_model_id = None
        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key = self.api_key,
            api_url = self.api_url
        )

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id
        
    def set_embeddings_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size


    def process_text(self, text: str):
        return text[:self.defualt_input_max_characters].strip()

    def generate_text(self, prompt: str, chat_history: list=[],max_output_tokens: int = None,
                      temperature: float = None):
        
        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Generation model ID is not set.")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_temperature
        
    
    def embed_text(self, text: str, document_type: str):

        if not self.client:
            self.logger.error("OpenAI client is not initialized.")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set.")
            return None
        
        response = self.client.embeddings.create(
            model=self.embedding_model_id,
            input=text,
        )

        if not response or not response.dataa or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Failed to get embedding from OpenAI API.")
            return None
    
        return response.data[0].embedding
    
    
    def construct_prompt(self, prompt: str, role: str):
            return {
            "role": role,
            "content": self.process_text(prompt)
        }