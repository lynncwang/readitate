from flask import Flask, send_from_directory, request, render_template
import requests
import json
from emotion_subject import emotion_subject_dict
app = Flask(__name__)

@app.route("/")
def home():
    return send_from_directory('templates','index.html')

def createUrl(subjects):
    query = '+'.join(subjects)
    full_query = "http://openlibrary.org/search.json?subject="+query
    return full_query

@app.route("/query", methods= ['POST'])
def searchUrl():
    try:
        user_input = request.form['emotion']
        if user_input in emotion_subject_dict:
            user_subjects = emotion_subject_dict[user_input]
        else:
            user_subjects = ['nobel_prize_winners','fiction']
        full_query = createUrl(user_subjects)
        resp = requests.get(full_query)
        data = json.loads(resp.text)
        books = []

        for i in range(29):
            book = {}
            if 'title_suggest' in data['docs'][i]:
                book['title'] = data['docs'][i]['title_suggest'].title()
            if 'author_name' in data['docs'][i]:
                book['author'] = data['docs'][i]['author_name'][0].title()
            else: book['author'] = 'Author unknown'
            if 'cover_i' in data['docs'][i]:
                book['cover_i']=data['docs'][i]['cover_i']
            else: book['cover_i']=0
            books.append(book)
        print books
        return render_template('results.html', books=books)

    except Exception as e:
        print e
        
@app.route("/about")
def hello():
    return render_template('aboutus.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/how")
def how():
    return render_template('how.html')

if __name__ == "__main__":
    app.run()
