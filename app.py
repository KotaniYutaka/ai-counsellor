import os

import openai
from datetime import timedelta 
from flask import Flask, redirect, render_template, request, url_for, session, jsonify

app = Flask(__name__)
openai.api_key = "-----"
app.secret_key = '-----'
app.permanent_session_lifetime = timedelta(minutes=10) 




@app.route("/", methods=("GET", "POST"))
def index():
    session['conversation'] = ''
    return render_template("index.html")




@app.route("/output", methods=['Get', 'POST'])
def output():
    animal = request.json['user_input']
    
    
  
        

    conversation = session.get("conversation", "------<br>")
    session["conversation"] = conversation
    message = handle_input(animal, "me", "you")
        
        
        #session["conversation"] = ''
           


        #return redirect(url_for("index", result=response.choices[0].text))
    return jsonify(message)







def generate_prompt(conversation_history):
    return f" pretend to be a counsellor and have a conversation in 25 words after  'you:'. Respond only with text, and do not include code, etc.\n\n{conversation_history}"

def handle_input(
               input_str : str,
                USERNAME : str,
                 AI_NAME : str,
                 ):
    """Updates the conversation history and generates a response using GPT-3."""
    # Update the conversation history
    conversation = session["conversation"]
    conversation += f"{USERNAME}: {input_str}<br>"
    conversation += f"{AI_NAME}: "
   
    # Generate a response using GPT-3
    message = openai.Completion.create(
                model="text-davinci-003",
                prompt=generate_prompt(conversation),
                temperature=0.6,
                max_tokens = 100,
               )
    # Update the conversation history
    conversation += f"{message.choices[0].text}<br> "
    
    session['conversation'] = conversation
      
    return message.choices[0].text
