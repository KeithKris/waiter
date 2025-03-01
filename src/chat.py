from ollama import chat
from src.schema import Order
from .config import (
  OLLAMA_MODEL
)

class LlamaChat:
  def get_response(self, messages):
    response = chat(
        model=OLLAMA_MODEL,
        messages=messages,
        format=Order.model_json_schema()
    )
    return response.message.content