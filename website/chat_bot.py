from flask import session
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI key
openai.api_key = os.getenv('OPENAI_API_KEY')


# Get bot response from OpenAI API based on user input and chat history.
# Adds user input and bot response to chat history
# eturns bot response.
def get_bot_response(user_input, chat_history):
    # Initialize messages 
 

    # Add new user message
    chat_history.append({"role": "user", "content": user_input})



    
    
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "Error: OpenAI API key not found"
            
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat_history,
            max_tokens=500,
            temperature=0.7
        )
        
        # Get and store bot's response
        bot_response = response.choices[0].message.content.strip()

        chat_history.append({"role": "assistant", "content": bot_response})

        bot_response = bot_response.replace('\n', '<br>')
        
        
        # Force session to update
        session.modified = True
        
        return bot_response
        
    except Exception as e:
        return f"Error: {str(e)}"