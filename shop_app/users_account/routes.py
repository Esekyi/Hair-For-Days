from flask import redirect, render_template, url_for, flash, request, session, current_app
from flask.json.tag import PassDict
from shop_app import db, app, photos, search, bcrypt, login_manager
from flask_login import login_required,current_user,logout_user, login_user
from .forms import UserRegisterationForm, UserLoginForm
from .models import Register, UserOrder
import secrets
import os


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    form = UserRegisterationForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        register = Register(fname=form.fname.data, lname=form.lname.data, email=form.email.data, password=hash_password, 
        country=form.country.data, state=form.state.data, city=form.city.data, zipcode=form.zipcode.data, 
        address=form.address.data, contact=form.contact.data,)
        db.session.add(register)
        flash(f'Welcome on board {form.fname.data}!, Now proceed to login', 'success')
        db.session.commit()
        return redirect(url_for('userLogin'))
    return render_template('User-customer/register.html', form=form, title='Create Account | HairForDays')



@app.route('/user/login', methods=['GET','POST'])
def userLogin():
    form = UserLoginForm()
    if form.validate_on_submit():
        user = Register.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Incorrect email or password', 'danger')
        return redirect(url_for('userLogin'))
    return render_template('User-customer/user_login.html', form = form)


@app.route('/user/logout')
def userLogOut():
    logout_user()
    return redirect(url_for('home'))





@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        user_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = UserOrder(invoice=invoice, user_id=user_id,
                              orders=session['ShoppingBag'])
            db.session.add(order)
            db.session.commit()
            session.pop('ShoppingBag')
            flash('Your order has been recieved', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            print(e)
            flash('something went wrong', 'danger')
            return redirect(url_for('getBag'))