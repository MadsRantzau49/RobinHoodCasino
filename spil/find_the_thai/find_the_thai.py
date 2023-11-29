import random
from flask import Flask, render_template, request

#Making it a webpage
app = Flask(__name__)

@app.route('/')
def index():
    
    return render_template("index.html", len_list=len_list, player=dbu_players_list, economy_list=economy_list)
  


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5001',debug=True)