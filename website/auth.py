from flask import Flask, session, Blueprint, render_template, request, flash, redirect, url_for
from .models import User, db, Note, Score, Score_UpDown
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import math
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from sqlalchemy import delete





auth = Blueprint('auth', __name__)

admin = ['pigeonchicken4@gmail.com']



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email)
        

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    

    return render_template("login.html", user=current_user, admin = admin)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', category='success')
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/leveltest', methods=['GET', 'POST'])
@login_required
def leveltest():
  if request.method == 'POST':

        choice_list=[]
        correct_list=[['q1_1', None, None, None], [None, None, None, 'q2_4'], [None, None, 'q3_3', None], [None, 'q4_2', None, None], ['q5_1', None, None, None], [None, None, None, 'q6_4'], [None, 'q7_2', None, None], ['q8_1', None, None, None], [None, 'q9_2', None, None], [None, None, None, 'q10_4'] ]
        result = 0
        category_count = 0
        score = 0
        
        q1_1 = request.form.get('q1_1')
        q1_2 = request.form.get('q1_2')
        q1_3 = request.form.get('q1_3')
        q1_4 = request.form.get('q1_4')
        category_count += 1
        choice_list.append([q1_1,q1_2,q1_3,q1_4])
        
        q2_1 = request.form.get('q2_1')
        q2_2 = request.form.get('q2_2')
        q2_3 = request.form.get('q2_3')
        q2_4 = request.form.get('q2_4')
        category_count += 1
        choice_list.append([q2_1,q2_2,q2_3,q2_4])

        q3_1 = request.form.get('q3_1')
        q3_2 = request.form.get('q3_2')
        q3_3 = request.form.get('q3_3')
        q3_4 = request.form.get('q3_4')
        category_count += 1
        choice_list.append([q3_1,q3_2,q3_3,q3_4])
        
        q4_1 = request.form.get('q4_1')
        q4_2 = request.form.get('q4_2')
        q4_3 = request.form.get('q4_3')
        q4_4 = request.form.get('q4_4')
        category_count += 1
        choice_list.append([q4_1,q4_2,q4_3,q4_4])
        
        q5_1 = request.form.get('q5_1')
        q5_2 = request.form.get('q5_2')
        q5_3 = request.form.get('q5_3')
        q5_4 = request.form.get('q5_4')
        category_count += 1
        choice_list.append([q5_1,q5_2,q5_3,q5_4])
        
        q6_1 = request.form.get('q6_1')
        q6_2 = request.form.get('q6_2')
        q6_3 = request.form.get('q6_3')
        q6_4 = request.form.get('q6_4')
        category_count += 1
        choice_list.append([q6_1,q6_2,q6_3,q6_4])
        
        q7_1 = request.form.get('q7_1')
        q7_2 = request.form.get('q7_2')
        q7_3 = request.form.get('q7_3')
        q7_4 = request.form.get('q7_4')
        category_count += 1
        choice_list.append([q7_1,q7_2,q7_3,q7_4])
        
        q8_1 = request.form.get('q8_1')
        q8_2 = request.form.get('q8_2')
        q8_3 = request.form.get('q8_3')
        q8_4 = request.form.get('q8_4')
        category_count += 1
        choice_list.append([q8_1,q8_2,q8_3,q8_4])
        
        q9_1 = request.form.get('q9_1')
        q9_2 = request.form.get('q9_2')
        q9_3 = request.form.get('q9_3')
        q9_4 = request.form.get('q9_4')
        category_count += 1
        choice_list.append([q9_1,q9_2,q9_3,q9_4])
        
        q10_1 = request.form.get('q10_1')
        q10_2 = request.form.get('q10_2')
        q10_3 = request.form.get('q10_3')
        q10_4 = request.form.get('q10_4')
        category_count += 1
        choice_list.append([q10_1,q10_2,q10_3,q10_4])
        
        correct_list_len = len(correct_list) 
        print(correct_list_len) 
        list_internal_size = 4

        print(choice_list)

        i = 0
        n = 0
        print(choice_list)
        
        for i in range(0, correct_list_len):
          if choice_list[i] == correct_list[i]:
            score += 1

        result = score * 10


        new_note = Score(data=math.floor(result), user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        flash('Score added!', category='success')

        scores = Score.query.all()

        new_note = Score_UpDown(correct=math.floor(result), incorrect= int(category_count*10)-math.floor(result), user_id=current_user.id)
        db.session.add(new_note)
        db.session.commit()
        

        
        


        return render_template("leveltest_result.html", user=current_user, result = result, scores=scores, admin = admin)
        
       
        


  return render_template("leveltest.html", user=current_user, admin = admin)

@auth.route('/leveltest_result', methods=['GET', 'POST'])
@login_required
def leveltest_result(result):
  if request.method == 'POST':
      note = request.form.get('note')

      if len(note) < 1:
          flash('Note is too short!', category='error')
      else:
          new_note = Note(data=note, user_id=current_user.id)
          db.session.add(new_note)
          db.session.commit()
          flash('Note added!', category='success')

  return render_template("leveltest_result.html", user=current_user, admin = admin)



@auth.route('/members', methods=['GET', 'POST'])
@login_required
def members():
  users = User.query.all()
  if request.method == 'POST':
      note = request.form.get('note')

      if len(note) < 1:
          flash('Note is too short!', category='error')
      else:
          new_note = Note(data=note, user_id=current_user.id)
          db.session.add(new_note)
          db.session.commit()
          flash('Note added!', category='success')
  
  return render_template("members.html", user=current_user, users = users, admin = admin)

@auth.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
  users = User.query.all()
  if request.method == 'POST':
      note = request.form.get('note')

      if len(note) < 1:
          flash('Note is too short!', category='error')
      else:
          new_note = Note(data=note, user_id=current_user.id)
          db.session.add(new_note)
          db.session.commit()
          flash('Note added!', category='success')
  
  return render_template("notes.html", user=current_user, users = users, admin = admin)

@auth.route('/calendar', methods=['GET', 'POST'])
@login_required
def calendar():
  users = User.query.all()

  
  return render_template("calendar.html", user=current_user, users = users, admin = admin)






  



  

  

  
  
