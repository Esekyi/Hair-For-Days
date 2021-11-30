from operator import inv
from flask import redirect, render_template, url_for, flash, request, session, current_app
from flask.json.tag import PassDict
from shop_app import db, app, photos, search, bcrypt, login_manager
from flask_login import login_required,current_user,logout_user, login_user
from .forms import UserRegisterationForm, UserLoginForm
from .models import Register, UserOrder
import secrets
import os
import stripe


publishable_key = 'pk_test_51K1bMSIiaYOuKbIdxbCz4eV199VqWnnKDo3b8V8pMitzOrNgCOctbpXzAZpuw3CquCFbnRepbGQzA1NMr9fEijix00fJiibmD9'

stripe.api_key = 'sk_test_51K1bMSIiaYOuKbIdwF1jujH005D5ufSVpAxxAfm9VPmCsbrqOisqvt4BYKOyWrFjCN1bWMOSzBWT3flNThFId8ku00pExp0qLt'


@app.route('/payment', methods = ['POST'])
@login_required
def payment():
    invoice = request.form.get('invoice')
    amount = request.form.get('amount')
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )


    charge = stripe.Charge.create(
        customer=customer.id,
        description='Hair For Days',
        amount=amount,
        currency='usd',
    )
    orders = UserOrder.query.filter_by(
        user_id = current_user.id, invoice = invoice).order_by(UserOrder.id.desc()).first()
    orders.status = 'Paid'
    db.session.commit()
    return redirect(url_for('thank_you.html'))



@app.route('/thank_you')
def thank_you():
    return render_template('User-customer/thank_you.html')




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


def update_checkoutItems():
    for _key, item in session['ShoppingBag'].items():
        session.modified = True
        # del item['image']
        del item['colors']
        del item['sizes']
    return update_checkoutItems 



@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        user_id = current_user.id
        invoice = secrets.token_hex(5)
        update_checkoutItems()
        try:
            order = UserOrder(invoice=invoice, user_id=user_id,
                              orders=session['ShoppingBag'])
            db.session.add(order)
            db.session.commit()
            session.pop('ShoppingBag')
            flash('Your order has been recieved', 'success')
            return redirect(url_for('orders', invoice = invoice))
        except Exception as e:
            print(e)
            flash('something went wrong', 'danger')
            return redirect(url_for('getBag'))


@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        total = 0
        grandTotal = 0
        user_id = current_user.id
        user= Register.query.filter_by(id = user_id).first()
        orders = UserOrder.query.filter_by(user_id = user_id, invoice = invoice ).order_by(UserOrder.id.desc()).first()
        for _key, item in orders.orders.items():
            discount = (item['discount'] / 100) * float(item['price'])
            total += float(item['price']) * int(item['quantity'])
            total -= discount
            tax = ("%.2f" % (.06 * float(total)))
            grandTotal = ("%.2f" % (1.06 * total))
    else:
        return redirect(url_for('userLogin'))
    return render_template('User-customer/user_order.html', invoice = invoice, tax = tax, grandTotal = grandTotal, user = user, total = total, orders=orders, title = 'Check Out Order | Hair For Days')
