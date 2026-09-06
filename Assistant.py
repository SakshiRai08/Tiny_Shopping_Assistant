import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("GROQ_API_KEY"),
                base_url="https://api.groq.com/openai/v1")

PRICES = {"shoes": 799, "hat": 399, "bag": 1420, "shorts": 1299, "pants": 1699, "jacket": 2999, "t-shirt": 499, "socks": 199, "scarf": 599, "gloves": 699}

def get_price(item):
    print(f"🔧 tool called: get_price({item})")
    return f"₹{PRICES.get(item.lower(), 'unknown')}"

tools = [{
    "type": "function",                                   
    "function": {
        "name": "get_price",                       
        "description": "Get the price of a shop item. Use ONLY for shop items.",
        "parameters": {
            "type": "object",
            "properties": {"item": {"type": "string", "description": "the item name"}},
            "required": ["item"],
        },
    },
}]


def agent(user_message):
    system_prompt = """You are Smart Shop Assistant, a helpful assistant that can provide information about shop items and their prices. You have access to a tool called get_price that can be used to retrieve the price of a specific item. Use this tool when the user asks for the price of an item. If the user asks for something unrelated to shop items -> you MUST NOT call any tool and you MUST reply EXACTLY with: "I'm sorry, I can only provide information about shop items and their prices. Please ask me about a specific item."Be friendly and short. After giving price, say "Anything else I can help with?"."""
    messages = [{"role": "system", "content": system_prompt}, 
                {"role": "user", "content": user_message}]

    response = client.chat.completions.create(     
        model="openai/gpt-oss-20b", messages=messages, tools=tools, tool_choice="auto")
    msg = response.choices[0].message

    if msg.tool_calls:
        
        for call in msg.tool_calls:
            if call.function.name == "get_price":
                args = json.loads(call.function.arguments) 
                result = get_price(args["item"])
                messages.append(msg)
                messages.append({"role": "tool", "tool_call_id": call.id, "content": result})
                response = client.chat.completions.create(model="openai/gpt-oss-20b", messages=messages)
                item_name = args["item"]
                return f"The price of {item_name} is {result}. Anything else I can help with?"

    return msg.content