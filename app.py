from flask import Flask, render_template, request, redirect, url_for
import datetime as d
app = Flask(__name__)
atm_data = {
    "account_number": "123",
    "pin": "123",
    "balance": 100000000000
}
transaction=[]
@app.route('/')
def home():
    return render_template("login.html")

@app.route('/login', methods=['POST'])
def login():
    acc_no = request.form['account_number']
    pin = request.form['pin']
    if acc_no == atm_data["account_number"] and pin == atm_data["pin"]:
        return redirect(url_for('dashboard'))
    else:
        return render_template("login.html",error='invalid credentials')
    
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    
    if request.method == 'POST':
        
        amount = int(request.form['withdraw'])
        if amount<=atm_data['balance']:
            atm_data['balance']-=amount
            transaction.append({"type": "Withdraw","amount": amount,"time": d.datetime.now().strftime("%d-%m-%Y %H:%M:%S")})
            print(atm_data['balance'])
            return redirect(url_for('dashboard'))
        else:
            return render_template("withdraw.html",error="Insufficient Balance")

            #     return f"""
    #     <h1>{atm_data["balance"]-amount}</h1>
    # """
        
    return render_template("withdraw.html")

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    
    if request.method == 'POST':
        amount = int(request.form['deposit'])
        atm_data['balance']+=amount
        transaction.append({
    "type": "Deposit",
    "amount": amount,
    "time": d.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
})
        return redirect(url_for('dashboard'))
    return render_template("deposit.html")
@app.route('/check_balance')
def check_balance():
    # if request.method=='POST':
    return render_template("check_balance.html",bal=atm_data['balance'])

@app.route('/statment')
def statment():
    # print(transaction)
    return render_template('statment.html',transaction=transaction[::-1])

@app.route('/pin_change', methods=['GET', 'POST'] )
def pin_change():
    if request.method=='POST':
        new_pin=request.form['new_pin']
        old_pin=request.form['old_pin']
        if old_pin==atm_data['pin']:
            # atm_data['pin']=new_pin
            return render_template('dashboard.html')
        else:
            return render_template('pin_change.html',error="wrong pin")
    return render_template('pin_change.html')



if __name__ == '__main__':
    app.run(debug=True)