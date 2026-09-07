import gradio as gr
from Assistant import agent
import os
from dotenv import load_dotenv

load_dotenv()

INITIAL_MSG = "Hello! I'm your Smart Shop Assistant. Ask me the price of anything."

def chat(message, history):
    return agent(message)

with gr.Blocks() as app:
    gr.Markdown("## 🛍️ Smart Shop Assistant")
    chatbot = gr.Chatbot(value=[{"role": "assistant", "content": INITIAL_MSG}], label="Chat with Shop Assistant", height=400)
    msg = gr.Textbox(label="Type your message here...", placeholder="How much are the shoes?")
    def user_send(user_message, chat_history):
        chat_history.append({"role": "user", "content": user_message})
        return "", chat_history
    def bot_reply(chat_history):
        last_user_msg = chat_history[-1]["content"]
        bot_response = chat(last_user_msg, chat_history)
        chat_history.append({"role": "assistant", "content": bot_response})
        return chat_history
    
    msg.submit(user_send, [msg, chatbot], [msg, chatbot], queue=False).then(bot_reply, chatbot, chatbot)
    gr.Examples(["How much are the shoes?", "What is the price of a hat?", "Tell me the cost of a bag.", "How much do shorts cost?", "What is the price of pants?", "How much is a jacket?", "Tell me the cost of a t-shirt.", "How much do socks cost?", "What is the price of a scarf?", "How much are gloves?"], inputs=msg)

app.launch(theme=gr.themes.Soft(), server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 10000)))