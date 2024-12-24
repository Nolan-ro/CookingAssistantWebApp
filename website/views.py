from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
from flask import session  
import json

views = Blueprint('views', __name__)
@views.route("/")
@login_required
def home():
    print("User authenticated:", current_user.is_authenticated)  #
    return render_template("home.html", user=current_user)

@views.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]
    bot_response = get_bot_response(user_input)
    return jsonify({"response": bot_response})



import openai
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI key
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_bot_response(user_input):
    # Initialize messages 
    if 'messages' not in session:
        system_message = """You are a professional chef and cooking assistant. Follow these rules:
            1. If a user gives you some ingredients, list five to ten meals that contain as many of the ingredients as possible and ask them to choose.
            2. Provide recipes in this format: 1) Ingredients with measurements list 2) Step-by-step instructions on how to cook the meal using the recipe.
            3. Don't give a recipe until the user has confirmed a meal.
            4. Keep responses concise but informative."""
        
        session['messages'] = [
            {"role": "system", "content": system_message}
        ]
    
    # Add user message to history
    session['messages'].append({"role": "user", "content": user_input})
    
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return "Error: OpenAI API key not found"
            
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=session['messages'],
            max_tokens=500,
            temperature=0.7
        )
        
        # Get and store bot's response
        bot_response = response.choices[0].message.content.strip()
        bot_response = bot_response.replace('\n', '<br>')
        session['messages'].append({"role": "assistant", "content": bot_response})
        
        # Force session to update
        session.modified = True
        
        return bot_response
        
    except Exception as e:
        return f"Error: {str(e)}"
# @views.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     if request.method == 'POST': 
#         note = request.form.get('note')#Gets the note from the HTML 

#         if len(note) < 1:
#             flash('Note is too short!', category='error') 
#         else:
#             new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
#             db.session.add(new_note) #adding the note to the database 
#             db.session.commit()
#             flash('Note added!', category='success')

#     return render_template("home.html", user=current_user)


# @views.route('/delete-note', methods=['POST'])
# def delete_note():  
#     note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()

#     return jsonify({})
