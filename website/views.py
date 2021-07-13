from flask import session, Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User, Score, Score_UpDown
from . import db
import json
import math


views = Blueprint('views', __name__)



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    users = User.query.all()
    s = Score.query.all()
    if request.method == 'POST':
        note = request.form.get('note')
        

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')

    No_entity = False
    if len(current_user.scores) == int(0):
      No_entity = True

    No_entity_2 = False
    if len(s) <= int(4):
      No_entity_2 = True
    
    print(No_entity)

    score_sum = 0
    sum_score_len = len(current_user.scores)
    if sum_score_len != 0:
      for n in current_user.scores:
        score_sum += int(n.data) 

    print(score_sum)

    if sum_score_len != 0:
      average_score = score_sum / sum_score_len
    else:
      average_score = 0
    
    
    average_score = math.floor(average_score)

    if sum_score_len != 0:
      latest_score = int(current_user.scores[-1].data)
    else:
      latest_score = 0
  
    correct = 0
    incorrect = 0
    if len(current_user.scores_updown) != 0:
      for n in current_user.scores_updown:
        correct += int(n.correct)
        incorrect += int(n.incorrect)
    else:
      pass

    correct_raw = int(correct /10)
    incorrect_raw = int(incorrect /10)

    Overall_Questions = correct+ incorrect

    if Overall_Questions == 0:
      correct = 0
      incorrect = 0
    else:
      correct = int(correct / Overall_Questions * 100)
      incorrect = int(incorrect / Overall_Questions * 100)

    SCORE_ALL = Score.query.all()

    SCORE_LIST = []

    for n in SCORE_ALL:
      
      SCORE_LIST.append(n.data)
      sorted(SCORE_LIST)
    

    print(SCORE_LIST)

    Higest_Score = SCORE_LIST[-1]

    Higest_Score_User = []

    for n in SCORE_ALL:
      if n.data == Higest_Score:
        Higest_Score_User.append(n.user_id)

    Higest_Score_User_listx = ""
    for n in users:
      if Higest_Score_User[-1] == n.id:
        Higest_Score_User_listx = n.first_name

    print(Higest_Score_User_listx)

    y = [1, 1, 2, 2]

    print(predict(1, y))



    total_visits_count = visits(1)
    

    return render_template("home.html", user=current_user, users = users, No_entity = No_entity, s=s, average_score = average_score, latest_score=latest_score, No_entity_2=No_entity_2, correct=correct, incorrect=incorrect, correct_raw= correct_raw, incorrect_raw = incorrect_raw, total_visits_count = total_visits_count, Higest_Score = Higest_Score, Higest_Score_User_listx = Higest_Score_User_listx)

@views.route('/test', methods=['GET', 'POST'])
@login_required
def test():
  return render_template("index2.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/delete-user', methods=['POST'])
def delete_user():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = User.query.get(noteId)
    if note:
        
      db.session.delete(note)
      db.session.commit()

    return jsonify({})

result = [1, 1]

def visits(n):
    
    num = result[0] + result[-1]
    result.append(num+13)
    print(result)
    del result[1]
    return result[-1]

def predict(x, y):
  return y
