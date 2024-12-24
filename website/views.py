from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
from flask import session  
import json
from .chat_bot import get_bot_response

views = Blueprint('views', __name__)
@views.route("/")
@login_required
def home():
    # Initialize new chat history for the current user
    session[f'chat_history_{current_user.id}'] = []
    system_message = """You are a professional chef and cooking assistant. Follow these rules:
        1. If a user gives you some ingredients, list five to ten meals that contain as many of the ingredients as possible and ask them to choose.            
        2. Provide recipes in this format: Header with recipe name. Ingredients with measurements list. Numbered step-by-step instructions on how to cook the meal using the recipe.
        3. Don't give a recipe until the user has confirmed a meal.
        4. When proving a recipe, provide the recipe in the format specified in rule 2 and do not add any additional text.
        5. Keep responses concise but informative."""
    
    session[f'chat_history_{current_user.id}']  = [
        {"role": "system", "content": system_message}
    ]
 
    return render_template("home.html", user=current_user)

@views.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form["user_input"]
    bot_response = get_bot_response(user_input, session[f'chat_history_{current_user.id}'])
    return jsonify({"response": bot_response})

@views.route("/saved_recipes")
@login_required
def saved_recipes():
    return render_template("saved_recipes.html", user=current_user)




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
