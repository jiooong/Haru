from flask import Flask, render_template, request, jsonify
from bson.objectid import ObjectId

app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.cu1k4vq.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/add')
def signup():
    return render_template('add.html')


# @app.route('/modify')
# def detail():
#     print("arg:", request.args.get("idx"))
#     if request.args.get("idx"):
#         bulletin = mongo.db.diary
#         print("idx :", type(idx))
#         print("ObjectID(idx) :" , type(ObjectId(idx)))
#         print(bulletin.find_one({"_id": ObjectId(idx)}))
#         if bulletin.find_one({"_id": ObjectId(idx)}):
#             bulletin_data = bulletin.find_one({"_id" : ObjectId(idx)})
#             print(bulletin_data)
#             if bulletin_data != "" :
#                 db_data = {
#                     "id"
#                     "title"
#                     "content"
#                 }
#                 return render_template('modify.html', db_data = db_data)

@app.route('/modify')
def detail():
    num = request.args.get("num")
    return render_template('modify.html',num=num)


@app.route('/guestbook', methods=["GET"])
def get_diary():
    num =request.args.get("num")
    if num is not None:
        num = int(num)
        if num == 'null':
            return jsonify({'error': 'Invalid diary id.'}), 400
        
        diary_info = db.diary.find_one({'num': int(num)}, {'_id': False})
        return jsonify({ 'data': diary_info})
    else:
        all_diary = list(db.diary.find({},{'_id':False}))
        return jsonify({'result': all_diary})
    

@app.route("/guestbook", methods=["POST"])
def guestbook_post():
    
    diary_list = list(db.diary.find({}, {'_id': False}))
    count = len(diary_list) + 1
    
    title_receive = request.form['title_give']
    comment_receive = request.form['comment_give']
    
    doc = {
        'num':count,
        'title':title_receive,
        'comment':comment_receive
    }
    db.diary.insert_one(doc)

    return jsonify({'msg': '등록완료'})

@app.route("/guestbook", methods=["DELETE"])
def guestbook_delete(): 
    num = request.args.get("num")
    if num is not None:
        num = int(num)
        if num == 'null':
            return jsonify({'error': 'Invalid diary id.'}), 400
        
        diary_info = db.diary.find_one({'num': int(num)}, {'_id': False})
        db.diary.delete_one(diary_info)
        
        return jsonify({'msg': '삭제완료'})
    

# @app.route("/guestbook", methods=["GET"])
# def guestbook_get():
#     all_diary = list(db.diary.find({},{'_id':False}))
#     return jsonify({'result': all_diary})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
