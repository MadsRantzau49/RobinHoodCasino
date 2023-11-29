import random
from flask import Flask, render_template, request

#Making it a webpage
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/find_the_thai.html', methods=['POST','GET'])
def find_the_thai():
    numbers_of_thais = 5
    
    if request.method == 'POST':
        placedBet = int(request.form['placedBet'])
        choosenThai = int(request.form['choosenThai'])
        result = random.randint(0,5)
        if result == choosenThai:
            profit = placedBet * 5
        else:
            profit = -1* placedBet

        return render_template("find_the_thai.html",numbers_of_thais=numbers_of_thais, profit=profit,choosenThai=choosenThai,placedBet=placedBet,result=result)
    else:
        return render_template("find_the_thai.html",numbers_of_thais=numbers_of_thais)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='5001',debug=True)
