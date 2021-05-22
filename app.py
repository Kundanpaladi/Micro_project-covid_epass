import requests
from flask import Flask, render_template, request
from twilio.rest import Client

account_sid = 'ACea675aa175c122d1aa7b8accf33b2757'
auth_token = 'c7566abd60b0b814e29c8153ed585126'
client = Client(account_sid, auth_token)
app = Flask(__name__, static_url_path='/static')


@app.route('/')
def registration_form():
    return render_template('user_registration.html')


@app.route('/user_status', methods=['GET', 'POST'])
def login_registration_dtls():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form['dest_state']
    destination_dt = request.form['destination']
    phoneNumber = request.form['phoneNumber']
    id_proof = request.form['idcard']
    full_name = first_name + "." + last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_data = r.json()
    cnt = json_data[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_data[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt / pop) * 100)
    if travel_pass < 10 and request.form['covid_status'] == "negative" and request.method == 'POST':
        status = 'CONFIRMED'
        client.messages.create(to="+917989445823",
                                from_="+13173155093",
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " + source_dt + " to " +
                                    destination_dt + " " + "Is " + " " + status +".")
        return render_template('user_status.html', firstname=first_name, lastname=last_name,
                           status="confirmed", email=email_id)
    else:
        status = 'DENIED'
        client.messages.create(to="+917989445823",
                               from_="+13173155093",
                               body="Hello " + " " + full_name + " " + "Your Travel From " + " " +
                                    source_dt + " to " + destination_dt + " " + "Has been" + " " + status + " " +
                                    ", Apply later")
        return render_template('user_status.html', firstname=first_name, lastname=last_name,
                               status="Denied", email=email_id)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
