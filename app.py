from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@wkdtmddus.wgnp3i4.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/add')
def signup():
    return render_template('add.html')

@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    doc = {
        'title':title_receive,
        'comment':comment_receive
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': '등록완료'})

@app.route("/guestbook", methods=["GET"])
def guestbook_get():
    all_diary = list(db.diary.find({},{'_id':False}))
    return jsonify({'result': all_diary})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)