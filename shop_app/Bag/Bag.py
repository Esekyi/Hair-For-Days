from typing import Dict
from shop_app.items.routes import vehiclePart
from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop_app import db, app
from shop_app.items.models import AddItem
import simplejson
from shop_app.items.routes import brands, categorys


def MergeDicts(dict1, dict2):
    if isinstance(dict, list) and isinstance(dict1, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/AddtoBag', methods=['POST'])
def AddtoBag():
    try:
        item_id = request.form.get('item_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        sizes = request.form.get('sizes')
        wigItem = AddItem.query.filter_by(id=item_id).first()
        if item_id and colors and quantity and sizes and request.method == "POST":
            DictItems = {
                item_id: {'name': wigItem.name, 'price': wigItem.price,
                          'discount': wigItem.discount, 'color': colors, 'size': sizes,
                          'quantity': quantity, 'image': wigItem.image_1, 'colors': wigItem.colors, 'sizes': wigItem.sizes
                          }
            }

            if 'ShoppingBag' in session:
                print(session['ShoppingBag'])
                if item_id in session['ShoppingBag']:
                    for key, item in session['ShoppingBag'].items():
                        if int(key) == int(item_id):
                            session.modified = True
                            item['quantity'] += 1
                else:
                    session['ShoppingBag'] = MergeDicts(
                        session['ShoppingBag'], DictItems)
                    return redirect(request.referrer)

            else:
                session['ShoppingBag'] = DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@app.route('/bagItems')
def getBag():
    if 'ShoppingBag' not in session or len(session['ShoppingBag']) <= 0:
        return redirect(url_for('home'))
    total = 0
    grandTotal = 0
    for key, item in session['ShoppingBag'].items():
        discount = (item['discount']/100) * float(item['price'])
        total += float(item['price']) * int(item['quantity'])
        total -= discount
        tax = ("%.2f" % (.06 * float(total)))
        grandTotal = float("%.2f" % (1.06 * total))
    return render_template('items/bag.html', tax=tax, grandTotal=grandTotal, brands=brands(), categorys=categorys())


@app.route('/updatebag/<int:code>', methods=['POST'])
def updatebag(code):
    if 'ShoppingBag' not in session or len(session['ShoppingBag']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        color = request.form.get('color')
        try:
            session.modified = True
            for key, item in session['ShoppingBag'].items():
                if int(key) == code:
                    item['quantity'] = quantity
                    item['color'] = color
                    flash('Item has been Updated!')
                    return redirect(url_for('getBag'))
        except Exception as e:
            print(e)
            return redirect(url_for('getBag'))


@app.route('/removeitem/<int:id>')
def removeitem(id):
    if 'ShoppingBag' not in session or len(session['ShoppingBag']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['ShoppingBag'].items():
            if int(key) == id:
                session['ShoppingBag'].pop(key, None)
                flash('The Item was removed from your bag')
                return redirect(url_for('getBag'))
    except Exception as e:
        print(e)
        return redirect(url_for('getBag'))


@app.route('/emptyBag')
def emptyBag():
    try:
        session.pop('ShoppingBag', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)
