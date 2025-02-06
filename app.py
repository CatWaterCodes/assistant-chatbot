from flask import Flask, render_template
from flask import request
import OllamaManager
import subprocess

app = Flask(__name__)

@app.route('/')
def run_app():
    return render_template("index.html")

@app.route('/prompt/', methods=['POST'])
def prompt():
    print("prompt called. prompt")
    try:
        json = request.get_json()
        print("prompt: " + json['prompt'])
        response = OllamaManager.chat(json['prompt'])
        return response
    
    except Exception as error:
        return "An error occured: " + str(error)
    
if __name__ == "__main__":
    OllamaManager.run_model()
    print("works")
    app.run(debug=True)