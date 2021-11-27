from shop_app.admin.routes import category
from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop_app import db, app, photos, search
from .forms import UserRegisterationForm
import secrets
import os


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    form = UserRegisterationForm(request.form)
    return render_template('User-customer/register.html', form=form)
