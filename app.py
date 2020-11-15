import os
import datetime


from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

db = SQLAlchemy(app)


class Products(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(400), nullable=False)
    price = db.Column(db.INTEGER, nullable=False)
    image = db.Column(db.String(400), nullable=True)
    timestamp = db.Column(db.DATETIME, default=datetime.datetime.now())

    def __repr__(self):
        return self.title


@app.route('/')
def index():
    products = Products.query.filter_by(type='bed').order_by(Products.id).all()
    last = Products.query.filter_by(type='bed').order_by(db.desc(Products.id)).limit(4).all()
    return render_template('indextemp.html', products=products, lastAdd=last, hero=True)


@app.route('/beds')
def beds():
    products = Products.query.filter_by(type='bed').order_by(Products.id).all()
    return render_template('bedstemp.html', products=products, hero=True)


@app.route('/cases')
def cases():
    products = Products.query.filter_by(type='bed').order_by(Products.id).all()
    items = Products.query.filter_by(type='case').order_by(Products.id).all()
    return render_template('casestemp.html', products=products, cases=items, hero=True)


@app.route('/poufs')
def poufs():
    products = Products.query.filter_by(type='bed').order_by(Products.id).all()
    items = Products.query.filter_by(type='pouf').order_by(Products.id).all()
    return render_template('poufstemp.html', products=products, poufs=items, hero=True)


@app.route('/card/<int:id>')
def card(id):
    product = Products.query.get(id)
    products = Products.query.filter_by(type='bed').order_by(Products.id).all()
    return render_template('bedcardtemp.html', product=product, products=products, hero=False)


@app.route('/about')
def about():
    products = Products.query.filter_by(type='bed').order_by(Products.id).all()
    return render_template('abouttemp.html', products=products, hero=True)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        target = os.path.join(APP_ROOT, 'static/')
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)
            print('create image dir')

        for file in request.files.getlist("file"):
            print(file)
            filename = file.filename
            destination = "".join([target, filename])
            print(destination)
            file.save(destination)

        title = request.form['title']
        pt = request.form['type']
        description = request.form['description']
        price = request.form['price']
        image = filename

        product = Products(title=title, description=description, image=image, type=pt, price=price)

        try:
            db.session.add(product)
            db.session.commit()
            return redirect(url_for('index'), 200)
        except:
            return 'Ошибка'
    else:
        return render_template('create.html')


@app.errorhandler(404)
def pageNot(error):
        return ('Cраница не найдена 404', 404)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)