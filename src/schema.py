from pydantic import BaseModel

class Item(BaseModel):
    number: int
    special_instructions: str

class Order(BaseModel):
    order_complete: bool
    say: str
    item_number: list[Item]
        
	