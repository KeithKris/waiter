from src.chat import LlamaChat
from src.tts import locutus
import unittest
import json

def main():
  print("Llama LLM Chat - Type 'exit' to quit.")

  chat = LlamaChat()
  speak = locutus()

  menu = {
    1045: "Burger Combo",
    2178: "Chicken Sandwich",
    3321: "Grilled Cheese",
    4592: "Hot Dog",
    6127: "Caesar Salad",
    7489: "Chicken Tenders",
    8093: "Fish & Chips",
    9215: "BBQ Pulled Pork Sandwich",
    1056: "Breakfast Burrito",
    2347: "Cheese Pizza Slice",
    3698: "Pepperoni Pizza Slice",
    4823: "Mac & Cheese Bowl",
    5576: "Taco Trio",
    6782: "Philly Cheesesteak",
    7241: "Mozzarella Sticks",
    8450: "French Fries",
    9023: "Onion Rings",
    1162: "Soft Drink",
    2389: "Milkshake"
  }

  messages = [{"role": "system", "content": get_system_prompt()}]
               
  while True:
    user_input = input("\nYou: ")

    if user_input.lower() in ["exit", "quit"]:
      print("\nExiting. Goodbye!")
      break

    messages.append({"role": "user", "content": user_input})
    response = chat.get_response(messages)
    messages.append({"role": "assistant", "content": response})
    print(f"Llama: {response}")
    result = json.loads(response)
    if not result['order_complete']:
        speak.vocalize(result['say'])
        pass
    else:
        if len(result['item_number']) == 0:
            print ("invalid order")
            messages.append({"role": "system", "content": "The previous response was invalid. item_number cannot be null when order_complete is false. There is enough information to complete the order in this prompt. Complete it correctly. Use the say parameter in this response to talk to the user"})
            response = chat.get_response(messages)
            messages.append({"role": "assistant", "content": response})
            print(f"Llama: {response}")
        else:
            summary = summarize_order(result, menu)
            messages.append({"role": "system", "content": "The user has ordered the following " + summary + '''
                             Ensure each item matches what the user asked for. 
                             Ensure all items are valid on the menu. 
                             If the order is incorrect, set order_complete to false and ask the user for clarification in the say parameter of this response.'''})
            response = chat.get_response(messages)  
            messages.append({"role": "assistant", "content": response})
            result = json.loads(response)
            
            # Final order confirmation
            if result['order_complete']:
              print ("User has ordered")
              print (summary)
              messages = [{"role": "system", "content": get_system_prompt()}]
            else:
               print ("invalid order")
               print (f"Llama: {response}")


def get_system_prompt():
   return '''Role: You are an ordering assistant at "Big Pete's House of Munch."
Rules:
To communicate with the user, place your response in the say parameter.
Do not make up information or substitute items. If a user asks for something not on the menu, clarify that the item is not available.
Always check if what the user asks for is on the menu. If you are not sure, ask for more information.
Do not assume or guess. If the user describes an item not on the menu, do not match it to an existing item unless the description clearly aligns with a menu item.
Do not provide pricing information.
Use item names, not numbers, when speaking to the user.
Order Completion:
Always repeat the user's complete order back and ask them if they would like anything else before completing an order. You may skip this only if the user has already confirmed that the order is complete.
Double check if any invalid items are in the order. Ask for clarification if there are invalid items.
If items were ordered, item_numbers must contain all corresponding numeric item codes.
If no valid items were ordered, return an empty list.
Never omit item_numbers if items were ordered.
users may order multiple of the same item. Each item should be listed separately in item_numbers.
Menu Items:
    "Burger Combo":1045
    "Chicken Sandwich":2178
    "Grilled Cheese":3321
    "Hot Dog":4592
    "Caesar Salad":6127
    "Chicken Tenders":7489
    "Fish & Chips":8093
    "BBQ Pulled Pork Sandwich":9215
    "Breakfast Burrito":1056
    "Cheese Pizza Slice":2347
    "Pepperoni Pizza Slice":3698
    "Mac & Cheese Bowl":4823
    "Taco Trio":5576
    "Philly Cheesesteak":6782
    "Mozzarella Sticks":7241
    "French Fries":8450
    "Onion Rings":9023
    "Soft Drink":1162
    "Milkshake":2389
    This is an example of an incorrect response. Item_numbers cannot be empty when order_complete is true. {"order_complete": true, "say": "", "item_number": [ ]}
    This is an example of a correct response. {"order_complete": true, "say": "", "item_number": [  { "number": 3321, "special_instructions": "" }, { "number": 9023, "special_instructions": "" } ]'''
              
def summarize_order(order, menuitems):
    summary = ""
    for item in order['item_number']:
        summary = summary + menuitems.get(item['number'], "one or more item numbers are not on the menu") + "\n"
    return summary

if __name__ == "__main__":
  main()
