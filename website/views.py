from flask import session, Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User, Score, Score_UpDown
from . import db
import json
import math
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy.stats import kurtosis, skew
from scipy.stats.stats import pearsonr  
from statistics import mean


views = Blueprint('views', __name__)

admin = ['taegue52@daum.net']



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
      n.data = int(n.data)
      SCORE_LIST.append(n.data)
      
    print(SCORE_LIST)
    SCORE_LIST.sort()
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

    for n in admin:
      print(n)

    total_visits_count = visits(1) 

    #Prediction-------------------------------
    score_list = []
    prediction_list = []
    pp_prediction_list= []
    Pearson = []
    res_prediction_score = 0
    res_res_prediction_score = 0
    tag = "D"

    if len(current_user.scores) < 3:
      predicted_score = 0
    else:
      X_train = []
      Y_train = []

      lin_reg = LinearRegression()

      for x in range(0, len(current_user.scores)):
        prediction_list.append(current_user.scores[x].data)
        if(x < 2):
          pass
        else:
          X_train.append([current_user.scores[x-2].data, current_user.scores[x-1].data])
          Y_train.append([current_user.scores[x].data])


      X_train = np.array(X_train)
      Y_train = np.array(Y_train)

      reg = lin_reg.fit(X_train, Y_train)

      predicted_score = reg.predict(np.array([[current_user.scores[-2].data,current_user.scores[-1].data]]))

      predicted_score= round(predicted_score[0][0])

      if(predicted_score < 0):
        predicted_score = 0
      elif(predicted_score > 100):
        predicted_score = 100

      prediction_list.append(predicted_score)
      print(prediction_list)


      length = len(prediction_list)-3

      

      for x in range(0, 20): 
        lX_train = []
        lY_train = []
        for a in range(0, len(prediction_list)):
          if(a < len(prediction_list)-2):
            lX_train.append([prediction_list[a], prediction_list[a+1]])
            lY_train.append([prediction_list[a+2]])

        lX_train = np.array(lX_train)
        lY_train = np.array(lY_train)

        lreg = lin_reg.fit(lX_train, lY_train)

        lpredicted_score = lreg.predict(np.array([[prediction_list[-2],prediction_list[-1]]]))

        lpredicted_score= round(lpredicted_score[0][0])

        if(lpredicted_score < 0):
          lpredicted_score = 0
        elif(lpredicted_score > 100):
          lpredicted_score = 100

        prediction_list.append(lpredicted_score)

        lX_train = lX_train.tolist()
        lY_train = lY_train.tolist()

      print(lX_train)
      print(lY_train)

      
      print(length)

      pp_prediction_list = lY_train[length:]
      print(pp_prediction_list)




      res_prediction_score = pp_prediction_list[-1]

      res_res_prediction_score = res_prediction_score[0]

      if len(current_user.scores) >= 3:
        if(res_res_prediction_score >= 70):
          tag = "A"
        elif(res_res_prediction_score < 70 and res_res_prediction_score >= 40):
          tag = "B"
        else:
          tag = "C"

      
          

    #End of Prediction-------------------------------

    #Prediction Average 
    avg_res = 0

    avg = 0
    num = 0
    if len(current_user.scores) >= 3:
      for n in current_user.scores:
        num +=1
        y = n.data
        score_list.append(n.data)
        avg += y
      
      for x in pp_prediction_list:
        num+=1
        y = x[0]
        avg += y

      avg_res = avg / num
      avg_res = round(avg_res)

    #End of Prediction Average-------------------------
    
    if len(current_user.scores) >= 3:
      final_list = score_list + res_prediction_score

    #print(final_list)

    #Skewness
    if len(current_user.scores) >= 3:
      skew_final = skew(final_list)
    else:
      skew_final = 0

    #Kurtosis
    if len(current_user.scores) >= 3:
      kurt_final = kurtosis(final_list)
    else:
      kurt_final = 0

    #Variance
    if len(current_user.scores) >= 3:
      var_final = np.var(final_list,ddof=1)
    else:
      var_final = 0

    #Standard_Deviation
    if len(current_user.scores) >= 3:
      std_final = np.std(final_list)
    else:
      std_final = 0

    #Minimum Value
    if len(current_user.scores) >= 3:
      min_final = min(final_list)
    else:
      min_final = 0

    #Maximum_Value
    if len(current_user.scores) >= 3:
      max_final = max(final_list)
    else:
      max_final = 0

    #Maximum_Value
    if len(current_user.scores) >= 3:
      data = np.array(final_list)
      q3, q1 = np.percentile(data, [75 ,25])
      iqr = q3 - q1
    else:
      iqr = 0

    #Pearson Correlation
    if len(current_user.scores) >= 3:
      for m in range(0, len(final_list)):
        Pearson.append(m+1)

      correlation, p_value = pearsonr(Pearson, final_list)

    else:
      correlation = 0

    #Covariance
    if len(current_user.scores) >= 3:
      covariance = np.cov(Pearson, final_list)[0,1]

    else:
      covariance = 0

    #User Analysis
    U_B = 0
    U_I = 0
    U_A = 0
    U_all = User.query.all()
    

    for u in range(0, len(U_all)):

      sum = 0
      aveg = 0
      for m_m in range(0, len(U_all[u].scores)):
        sum += U_all[u].scores[m_m].data
        

      if(len(U_all[u].scores) >=1):
        aveg = sum / len(U_all[u].scores)
      else:
        aveg = 0


      if(aveg >=70):
        U_A+=1
      elif(aveg <70 and aveg >= 30):
        U_I+=1
      else:
        U_B +=1

    print(U_B)
    print(U_I)
    print(U_A)


      
    

    return render_template("home.html", user=current_user, users = users, No_entity = No_entity, s=s, average_score = average_score, latest_score=latest_score, No_entity_2=No_entity_2, correct=correct, incorrect=incorrect, correct_raw= correct_raw, incorrect_raw = incorrect_raw, total_visits_count = total_visits_count, Higest_Score = Higest_Score, Higest_Score_User_listx = Higest_Score_User_listx, admin = admin, predicted_score = predicted_score, trial = len(current_user.scores), pp_prediction_list = pp_prediction_list, res_prediction_score = res_prediction_score, avg_res = avg_res, skew_final = skew_final, kurt_final = kurt_final, var_final = var_final, std_final = std_final, min_final = min_final, max_final = max_final, iqr = iqr, correlation = correlation, covariance= covariance, res_res_prediction_score = res_res_prediction_score, tag = tag, U_B = U_B, U_I = U_I, U_A = U_A)

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
