from flask import Flask, render_template, request, redirect, send_file
import smtplib
from email.message import EmailMessage
from twilio.rest import Client

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/<string:page_name>')
def pages(page_name):
    return render_template(page_name)

def write_database(data):
	with open('database.txt', mode='a') as database:
		phone = data["phone"]
		file = database.write(f'\n{phone}')

def write_mdatabase(data):
	with open('mdatabase.txt', mode='a') as database:
		matrix = data["matrix"]
		file = database.write(f'{matrix}')

def last_line(file):
	with open(file, 'r') as txt:
		for last in txt:
			pass
		return last

def mail_grade(grade):
	email = EmailMessage()
	email['from'] = 'My Project'
	email['to'] = 'mohammad.ahmadi1379@gmail.com'
	email['subject'] = 'Your Grade'
	email.set_content(f'Your Grade is {grade}')

	with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.login('project6152020@gmail.com', 'todayis6152020')
		smtp.send_message(email)

def sms_teacher(phone):
	account_sid = 'ACab0af4b77bf5d37725f6bad55ac5966a' 
	auth_token = '776d12bc41c0e5a06c942a1138e6a7e5' 
	client = Client(account_sid, auth_token) 
 
	message = client.messages.create( 
                              from_='+14256156467',  
                              body='Thanks For Using My Project',      
                              to=f'{phone}' 
                          ) 
 
	print(message.sid)

def write_grade(data):
	with open('grade.txt', mode='a') as grades_data:
		grade = data["grade"]
		message = data["message"]
		file = grades_data.write(f'\n{grade}, {message}')

def add(data):
	with open('pdatabase.txt', mode='a') as database:
		nc = data["nc"]
		name = data['name']
		lastname = data['lastname']
		file = database.write(f'\n{nc}, {name}, {lastname}')

def search_nc(data):
    pass
    
def update_nc(data):
	pass

@app.route('/submit', methods=['POST', 'GET'])
def submit():
	if request.method == 'POST':
		data = request.form.to_dict()
		write_database(data)
		write_grade(data)
		mail_grade(last_line(grade.txt))
		sms_teacher(last_line(database.txt))
		return redirect('/thanks.html')
	else:
		return redirect('/error.html')

@app.route('/done', methods=['POST','GET'])
def done():
	if request.method == 'POST':
		data = request.form.to_dict()
		add(data)
		return redirect('/homework2.html')

@app.route('/showall', methods=['POST','GET'])
def showall():
	if request.method == 'POST':
		path = "C:/Users/mohammad/Desktop/CPP/pdatabase.txt"
		return send_file(path, as_attachment=True)

#line.split
#for line in database
@app.route('/get_matrix', methods=['POST','GET'])
def get_matrix():
	if request.method == 'POST':
		data = request.form.to_dict()
		write_mdatabase(data)
	with open('mdatabase.txt', 'r') as data:
		matrix = [[int(num) for num in line.split(',')] for line in data]
	rows = len(matrix)
	columns = len(matrix[0])  
	sum_list= []
	avr_list= []
	failed= []
	for i in range(0, rows):  
		summ = 0
		for j in range(0, columns):  
			summ = summ + matrix[i][j]  
			sum_list.append((summ,'Student' + str(i+1)))
			avr_list.append((summ/columns,'Student' + str(i+1)))
			if summ/columns < 10:
				failed.append((summ/columns,'Student' + str(i+1)))

	best = avr_list[:3]
	with open('mdatabase.txt', mode='a') as database:
		database.write(f"\n{sum_list} \n{avr_list} \nbest : {best} \nfailed: {failed}")
	path = "C:/Users/mohammad/Desktop/CPP/mdatabase.txt"
	return send_file(path, as_attachment=True)