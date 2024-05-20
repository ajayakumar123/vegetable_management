from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from forms import VegetableForm


app = Flask(__name__)
app.config['SECRET_KEY'] = 'vegetable management'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vegetables.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
print("111111111111",db)
print("22222222222222",app)
migrate = Migrate(app, db)

class Vegetable(db.Model):
    print("5555555")
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.Date, nullable=False)
    supplier = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Vegetable {self.name}>'




@app.route('/')
def index():
    vegetables = Vegetable.query.all()
    return render_template('index.html', vegetables=vegetables)
@app.route('/add', methods=['GET', 'POST'])
def add_vegetable():
    form = VegetableForm()
    if form.validate_on_submit():
        vegetable = Vegetable(
            name=form.name.data,
            quantity=form.quantity.data,
            expiration_date=form.expiration_date.data,
            supplier=form.supplier.data
        )
        db.session.add(vegetable)
        db.session.commit()
        flash('Vegetable added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add_vegetable.html', form=form)



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_vegetable(id):
    vegetable = Vegetable.query.get_or_404(id)
    form = VegetableForm(obj=vegetable)
    if form.validate_on_submit():
        vegetable.name = form.name.data
        vegetable.quantity = form.quantity.data
        vegetable.expiration_date = form.expiration_date.data
        vegetable.supplier = form.supplier.data
        db.session.commit()
        flash('Vegetable updated successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('edit_vegetable.html', form=form)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_vegetable(id):
    vegetable = Vegetable.query.get_or_404(id)
    db.session.delete(vegetable)
    db.session.commit()
    flash('Vegetable deleted successfully!', 'success')
    return redirect(url_for('index'))



if __name__ == '__main__':
    with app.app_context():
        print("0000000000")
        #db.init_app(app)
        try:
            # db.drop_all()
            print("333333")
            db.create_all()
            print("44444444")
        except Exception as e:
            print(e)
    app.run(debug=True)
