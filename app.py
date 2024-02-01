from flask import Flask, render_template, request, redirect 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///UserForm.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

class UserForm(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(200), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default= datetime.utcnow)
    
        
@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method=='POST':
        customer_name= request.form['customer_name']
        product_name= request.form['product_name']         
        price= request.form['price']      
        user_info=UserForm(customer_name= customer_name ,product_name= product_name,price= price)
        db.session.add(user_info)
        db.session.commit()
        
    all_user= UserForm.query.all()   
    return render_template('index.html', all_user=all_user)

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        customer_name= request.form['customer_name']
        product_name= request.form['product_name']         
        price= request.form['price'] 
        user_info = UserForm.query.filter_by(sno=sno).first()
        user_info.customer_name = customer_name
        user_info.product_name = product_name
        user_info.price = price
        db.session.add(user_info)
        db.session.commit()
        return redirect("/")
    user_info = UserForm.query.filter_by(sno=sno).first()
    return render_template('update.html', user_info=user_info)

    
    
@app.route('/delete/<int:sno>')
def delete(sno):
    user_info = UserForm.query.filter_by(sno=sno).first()
    db.session.delete(user_info)
    db.session.commit()
    return redirect("/")

                
 

if __name__ == "__main__":
    app.run(debug=True, port=5050)