from flask import render_template,redirect,session,request,flash
from flask_app import app
from flask_app.models.bike import Bike
from flask_app.models.user import User

@app.route('/new/bike')
def new_bike():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_bike.html',users=User.get_by_id(data))

@app.route('/create/bike',methods=['POST'])
def create_bike():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Bike.validate_bike(request.form):
        return redirect('/new/bike')
    print(request.form)
    data = {
        "biketype": request.form['biketype'],
        "description": request.form['description'],
        "bikepic": request.form['bikepic'],
        "user_id": session["user_id"]
    }
    Bike.save(data)
    return redirect('/dashboard')

@app.route('/edit/bike/<int:id>')
def edit_bike(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id 
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_bike.html",edit=Bike.get_one(data),users=User.get_by_id(user_data))

@app.route('/update/bike', methods=['POST'])
def update_bike():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Bike.validate_bike(request.form):
        return redirect('new/bike')
    data = {
        "biketype": request.form['biketype'],
        "description": request.form['description'],
        "bikepic": request.form['bikepic'],
        "id": request.form['id']
    }
    Bike.update(data)
    return redirect('/dashboard')

@app.route('/bike/<int:id>')
def show_bike(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id 
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_bike.html", bike=Bike.get_one(data), users=User.get_by_id(user_data))

@app.route('/destroy/bike/<int:id>')
def destroy_bike(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id 
    }
    Bike.destroy(data)
    return redirect('/dashboard')

