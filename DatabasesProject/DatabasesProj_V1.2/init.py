#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import hashlib
import random
from datetime import date, datetime, timedelta

#Initialize the app from Flask
app = Flask(__name__)

# Activate VENV
#source .venv/bin/activate 
#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port= 8889,
                       user='root',
                       password='root',
                       db='proj',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')
#Define a route to flight function
@app.route('/flights')
def flights():
	return render_template('flights.html')

#Define route for staff
@app.route('/login/customer')
def login_customer():
	return render_template('login-cus.html')

#Define route for staff login
@app.route('/login/staff')
def login_staff():
	return render_template('login-staff.html')

#Define route for register
@app.route('/register/customer')
def register_customer():
	return render_template('register-cus.html')

@app.route('/register/staff')
def register_staff():
	cursor = conn.cursor()
	query = 'SELECT airline_name FROM airline'
	cursor.execute(query)
	data = cursor.fetchall()
	cursor.close()
	return render_template('register-staff.html', airline=data)

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuthCus():
	#cursor used to send queries
	cursor = conn.cursor()
	#grabs information from the forms
	email = request.form['email']
	password = request.form['password'] #userinput 
	hash_pass = hashlib.md5(password.encode()).hexdigest()
	
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s and pass_w = %s' 
	cursor.execute(query, (email, hash_pass))
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None

	if(data):
		#creates a session for the the user
		#session is a built in 
		print("hash pass")
		session['email'] = email
		#return redirect(url_for('hello'))
		return redirect('/customer/home') 
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login-cus.html', error=error)

#Authenticates the login
@app.route('/loginAuthStaff', methods=['GET', 'POST'])
def loginAuthStaff():
	#cursor used to send queries
	cursor = conn.cursor()
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password'] #userinput 
	hash_pass = hashlib.md5(password.encode()).hexdigest()
	
	#executes query
	query = 'SELECT * FROM air_staff WHERE username = %s and pass_word = %s' 
	cursor.execute(query, (username, hash_pass))
	#stores the results in a variable
	data = cursor.fetchall()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	cursor.close()
	if(data):
		#creates a session for the the user
		#session is a built in 
		#print("hash pass")
		session['username'] = username
		return redirect('/staff/home')
		#return render_template('loggedin-staff.html') 
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login-staff.html', error=error)

@app.route('/customer/home')
def customerhome():
	cus = cus_check_session()
	if (cus):
		return render_template('loggedin-cus.html', customer=cus)
	else:
		return redirect('/login/customer')

@app.route('/staff/home')
def staffhome():
	if (staff_check_session):
		staff = session['username']
		cursor = conn.cursor()
		query = "SELECT first_name FROM air_staff WHERE username = %s"
		cursor.execute(query, (staff))
		data = cursor.fetchall()
		cursor.close()
		return render_template('loggedin-staff.html',  data1= data)
	return redirect('/login/staff')


#Authenticates the register
@app.route('/registerAuth/customer', methods=['GET', 'POST'])
def registerAuthCus():
	#grabs information from the forms
	name = request.form['name']
	email = request.form['email']
	password = request.form['password']
	phonenum = request.form['phoneNum']
	buildnum = request.form['buildingNum']
	street = request.form['street']
	city = request.form['city']
	state = request.form['state']
	passnum = request.form['passportNumber']
	passcountry = request.form['passportCountry']
	passexp = request.form['passportExp']
	dob = request.form['dob']

	#Hashes Users Password
	hash_pass = hashlib.md5(password.encode()).hexdigest()

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM customer WHERE email = %s'
	cursor.execute(query, (email))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register-cus.html', error = error)
	else:
		ins = 'INSERT INTO customer(`name`, `phone_num`, `email`, `pass_w`,`building_num`, `street`, `city`, `state`, `passport_num`, `passport_country`, `passport_exp`, `date_of_birth`) VALUES( %s, %s, %s, %s,%s, %s,%s, %s,%s, %s,%s, %s)'
		cursor.execute(ins, (
			name,
			phonenum,
			email, 
			hash_pass,
			buildnum,
			street,
			city,
			state,
			passnum,
			passcountry,
			passexp,
			dob
			))
		conn.commit()

		cursor.close()
		return render_template('index.html')

@app.route('/registerAuth/staff',methods=['GET', 'POST'] )
def registerAuthStaff():
	#grab the info from the form
	fname = request.form['fname']
	lname = request.form['lname']
	username = request.form['username']
	phoneNum = request.form['phoneNum']
	email = request.form['email']
	pass_w = request.form['password']
	airline = request.form['airline']
	dob = request.form['dob']

	#Hashes Users Password
	hash_pass = hashlib.md5(pass_w.encode()).hexdigest()


	cursor = conn.cursor()
	query = 'Select * FROM air_staff WHERE username = %s'
	cursor.execute(query, (username))
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register-staff.html', error = error)
	else:
		ins = 'INSERT INTO `air_staff`(`username`, `pass_word`, `first_name`, `last_name`, `date_of_birth`, `email`, `airline_name`) VALUES (%s,%s,%s,%s,%s,%s,%s)'
		cursor.execute(ins, (
			username,
			hash_pass,
			fname,
			lname,
			dob,
			email,
			airline
		))
		ins_phone = 'INSERT INTO `air_staff_phone_number`(`username`, `phone_number`) VALUES (%s,%s)'
		cursor.execute(ins_phone, (
			username,
			phoneNum
		))
		conn.commit()
		cursor.close()
		return render_template('index.html')


@app.route('/purchaseTicket', methods=['GET', 'POST'])
def purchaseTicket():
	return render_template('purchase-ticket.html')

@app.route('/purchaseTicketsAuth', methods=['GET', 'POST'])
def purchaseTicketAuth(): 
	cursor = conn.cursor()
	cus_email = request.form['cus_email']
	cus_ticket_id = request.form['cus_ticket_id']
	deptdate = request.form['deptdate']
	depttime = request.form['depttime']
	flightnum = request.form['flightnum']
	price = request.form['price']
	cardtype = request.form['cardtype']
	cardnumber = request.form['cardnumber']
	nameoncard = request.form['nameoncard']
	expmonth = request.form['expmonth']
	expyear = request.form['expyear']
	ins = 'INSERT INTO buys(`email`, `ticket_id`, `dept_date`, `dept_time`, `flight_num`, `sold_price`, `card_type`, `card_num`, `name_on_card`, `exp_month`, `exp_year`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
	cursor.execute(ins, (
		cus_email,
		cus_ticket_id,
		deptdate,
		depttime,
		flightnum,
		price,
		cardtype,
		cardnumber,
		nameoncard,
		expmonth,
		expyear
		))
	conn.commit()
	data = cursor.fetchall()    
	cursor.close()
	return render_template('flights.html',buys = data) 

@app.route('/customerFlight', methods=['GET', 'POST'])
def customerFlight():
	return render_template('flights.html')



@app.route('/customer/view/myflights')
def customerViewmyFlights():
	customer = cus_check_session()
	if customer:
		cursor = conn.cursor()
		query = 'SELECT * FROM Flight, buys WHERE buys.flight_num = flight.flight_num and buys.email = %s'
		cursor.execute(query, (customer[0]['email']))
		data = cursor.fetchall()
		cursor.close()
		return render_template('cus-view-flight.html',data=data)
	return redirect('/login/customer')


@app.route('/searchFlights', methods=['GET', 'POST'])
def flightSearch():
	deptairport = request.form['deptairport']
	arrairport = request.form['arrairport']
	deptdate = request.form['deptdate']
	current_date = get_format_date()
	cursor = conn.cursor()	
		
	query = 'SELECT  f.stats, f.flight_num, f.dept_airport, f.arr_airport, f.dept_date, f.arr_date FROM flight as f, manage as m WHERE (f.dept_date = %s OR f.dept_date >= %s) and f.dept_date >= %s and f.dept_airport = (SELECT name_airport FROM airport WHERE city = %s or name_airport = %s) and f.arr_airport = (SELECT name_airport FROM airport WHERE city = %s or name_airport=%s) and m.flight_num = f.flight_num and ((m.max_seats - m.total_seats) > 0)'
	cursor.execute(query, (
		deptdate,
		deptdate,
		current_date,
		deptairport,
		deptairport,
		arrairport,
		arrairport
	))
	flight = cursor.fetchall()
	cursor.close()
	return render_template('flights.html', flight=flight)


@app.route('/cusCancelFlight', methods=['GET', 'POST'])
def cusCancelFlight():
	customer = cus_check_session()
	if customer:
		flightnum = request.form['flight_num']
		cur = conn.cursor()
		query = 'SELECT ticket_id, dept_date, dept_time FROM buys WHERE flight_num = %s and email = %s'
		cur.execute(query, (
			flightnum,
			customer[0]['email']
		))
		data = cur.fetchall()
		ticketid = data[0]['ticket_id']

		delete = 'DELETE FROM buys WHERE ticket_id = %s and dept_date = %s and dept_time = %s'
		cur.execute(delete, (
			ticketid,
			data[0]['dept_date'],
			data[0]['dept_time']
		))

		del_ticket = 'DELETE FROM ticket WHERE ID = %s and dept_date = %s and dept_time = %s and flight_num = %s' 
		cur.execute(del_ticket, (
			ticketid,
			data[0]['dept_date'],
			data[0]['dept_time'],
			flightnum

		))
		month= data[0]['dept_date'].month
		day = data[0]['dept_date'].day
		year = data[0]['dept_date'].year
		currentDate = get_format_date().strip('-')

		seat = 'UPDATE `manage` SET `total_seats`= total_seats - 1 WHERE total_seats >=1'
		cur.execute(seat)
		conn.commit()
		cur.close()
		return redirect('/customer/view/myflights')
	return redirect('/login/customer')



@app.route('/staff/searchflights/date', methods=['GET', 'POST'])
def staffSearchFlights():
	air_data = staff_check_session()
	if (air_data):
		cursor = conn.cursor()
		#deptairport = request.form['deptairport']
		#arrairport = request.form['arrairport'] 
		deptdate = request.form['deptdate']
		arrdate = request.form['arrdate']
		query = 'SELECT f.dept_date, f.dept_time, f.flight_num, f.arr_time, f.arr_airport, f.arr_date, f.base_price, f.id_airplane, f.dept_airport, f.stats FROM flight as f, manage as m, air_staff as s WHERE (f.dept_date >= %s and f.arr_date < %s) AND m.flight_num = f.flight_num and m.airline_name = s.airline_name'
		cursor.execute(query, (
			deptdate,
			arrdate
		))
		data = cursor.fetchall()
		cursor.close()
		return render_template('staff-view-flights.html', flight = data, airline_name=air_data)
	return redirect('/login/staff')

@app.route('/staff/searchFlight/view', methods=['GET', 'POST'])
def staffViewSpecificFlgiht():
	airline = staff_check_session()
	if airline:
		flightnum = request.form['flight_num']
		cursor = conn.cursor()
		query = 'SELECT DISTINCT name, c.email FROM customer as c, buys as b WHERE b.flight_num = %s and b.email = c.email'
		cursor.execute(query, flightnum)
		data = cursor.fetchall()
		cursor.close()
		return render_template('customer-on-flight.html', data=data, airline=airline[0]['airline_name'], flight=flightnum)
	return redirect('/login/staff')


@app.route('/addFlight', methods=['GET', 'POST'])
def CreateNewFlights():
	airline = staff_check_session()
	if (airline):
		cursor = conn.cursor()
		query = 'SELECT id_airplane FROM airplane WHERE airline_name = %s'
		airport = 'SELECT name_airport FROM airport'
		cursor.execute(query, airline[0]['airline_name'])
		data = cursor.fetchall()
		cursor.execute(airport)
		air = cursor.fetchall()
		cursor.close()
		return render_template('addFlight.html', airplane = data, airport = air)
	return redirect('/login/staff')



@app.route('/addFlightAuth', methods=['GET', 'POST'])
def CreateNewFlighAtuth():
	staff = staff_check_session()
	if staff:
		deptdate = request.form['deptdate']
		depttime = request.form['depttime']
		flightnum = request.form['flightnum']
		arrtime = request.form['arrtime']
		arrairport = request.form['arrairport']
		arrdate = request.form['arrdate']
		baseprice = request.form['baseprice']
		idairplane = request.form['idairplane']
		deptairport = request.form['deptairport']
		states = request.form['states']
		cursor = conn.cursor()
		check = 'SELECT * FROM flight WHERE flight_num = %s'
		cursor.execute(check, flightnum)
		if (cursor.fetchall()):
			error = 'Flight Number Already in use'
			cursor.close()
			return render_template('staff-errorpage.html', error=error)

		ins = 'INSERT INTO flight(`dept_date`, `dept_time`, `flight_num`, `arr_time`,`arr_airport`, `arr_date`, `base_price`, `id_airplane`, `dept_airport`, `stats`) VALUES( %s, %s, %s, %s,%s, %s,%s, %s,%s, %s)'
		cursor.execute(ins, (
			deptdate, 
			depttime, 
			flightnum, 
			arrtime,
			arrairport,
			arrdate, 
			baseprice, 
			idairplane, 
			deptairport, 
			states
			))
		conn.commit()
		cur = conn.cursor()
		
		data = flight_helper(idairplane)
		tracks = 'INSERT INTO manage(`airline_name`, `dept_date`, `dept_time`, `flight_num`, `total_seats`, `max_seats`) VALUES (%s,%s,%s,%s, %s, %s)'
		cur.execute(tracks,(
			staff[0]['airline_name'],
			deptdate,
			depttime,
			flightnum,
			0,
			data[0]['num_of_seats'],
			
		))
		conn.commit()
		cur.close()
		cursor.close()
		return redirect('/staff/home')
	return redirect('/login/staff')

def flight_helper(id):
	cur = conn.cursor()
	seats = 'SELECT num_of_seats FROM airplane WHERE id_airplane = %s'
	cur.execute(seats, id)
	data = cur.fetchall()
	cur.close()
	return data
@app.route('/changeStatus', methods=['GET', 'POST'])
def changeFlightStatus():
	airline = staff_check_session()
	if airline:
		cursor = conn.cursor()
		query = 'SELECT m.flight_num FROM manage as m, flight as f WHERE f.flight_num = m.flight_num and m.airline_name = %s'
		cursor.execute(query, airline[0]['airline_name'])
		data = cursor.fetchall()
		cursor.close()
		return render_template('changeFlightStatus.html', flight = data)
	return redirect('/staff/home')

@app.route('/changeStatusAuth', methods=['GET', 'POST'])
def changeFlightStatusAuth():
	if (staff_check_session):
		flightnum = request.form['flightNum']
	#airplaneid = request.form['airplaneid']
		status = request.form['status']
		cursor = conn.cursor()
		ins = 'UPDATE flight SET stats = %s WHERE flight_num = %s'# and id_airplane = %s'
		cursor.execute(ins, (
			status,
			flightnum,
		#airplaneid
			))
		conn.commit()

		cursor.close()
		return redirect('/staff/home')
	return redirect('/login/staff')

@app.route('/customer/viewflights')
def customerViewFlights():
	customer = cus_check_session()
	if customer:
		return render_template('cus-search-flights.html')

	return redirect('/login/customer')

@app.route('/customer/search/flights', methods=['GET', 'POST'])
def customerFlightAuth(): 
	customer = cus_check_session()
	if customer:
		deptairport = request.form['deptairport']
		arrairport = request.form['arrairport']
		deptdate = request.form['deptdate']
		current_date = get_format_date()
		cursor = conn.cursor()	
		
		query = 'SELECT f.flight_num, f.dept_airport, f.arr_airport, f.dept_date, f.arr_date FROM flight as f, manage as m WHERE (f.dept_date = %s OR f.dept_date >= %s) and f.dept_date >= %s and f.dept_airport = (SELECT name_airport FROM airport WHERE city = %s or name_airport = %s) and f.arr_airport = (SELECT name_airport FROM airport WHERE city = %s or name_airport=%s) and m.flight_num = f.flight_num and ((m.max_seats - m.total_seats) > 0)'
		cursor.execute(query, (
			deptdate,
			deptdate,
			current_date,
			deptairport,
			deptairport,
			arrairport,
			arrairport
		))
		flight = cursor.fetchall()
		cursor.close()
		return render_template('cus-search-flights.html',flight=flight)
	return redirect('/login/customer')


@app.route('/customer/buy/flight',  methods=['GET', 'POST'])
def customerbuyflight():
	customer = cus_check_session()
	if customer:
		flightnum = request.form['flightnum']
		cur = conn.cursor()
		query = 'SELECT airline_name, base_price, max_seats, total_seats FROM flight, manage WHERE flight.flight_num = %s and manage.flight_num = %s'
		cur.execute(query, (
			flightnum,
			flightnum
		))
		data = cur.fetchall()
		baseprice = float(data[0]['base_price'])
		max_seats = float(data[0]['max_seats'])
		remain_seats = float(data[0]['max_seats']) - float(data[0]['total_seats'])
		if 0.6 * max_seats >= remain_seats:
			baseprice = baseprice + (baseprice * 0.25)
		return render_template('cus-buy-flight.html', price=baseprice, flight = flightnum, airline=data[0]['airline_name'])
	return redirect('/login/customer')

@app.route('/customer/buyAuth', methods=['GET', 'POST'])
def confirmCustomerBuy():
	customer = cus_check_session()
	if customer:
		print(get_date())
		price = request.form['price']
		name = request.form['name']
		ctype = request.form['type']
		cnum = request.form['cardnumber']
		expm = request.form['month']
		expy = request.form['year']
		flightnum = request.form['flightnum']
		cur = conn.cursor()
		num = generateTicketID()
		timestamp = get_timestamp()
		flight_info = get_flight_info(flightnum)
		ins = 'INSERT INTO `ticket`(`ID`, `dept_date`, `dept_time`, `flight_num`) VALUES (%s,%s,%s,%s)'
		cur.execute(ins, (
			num,
			flight_info[0]['dept_date'],
			flight_info[0]['dept_time'],
			flightnum
		))
		ins_buy = 'INSERT INTO `buys`(`email`, `ticket_id`, `dept_date`, `dept_time`, `flight_num`, `purchase_timestamp`, `sold_price`, `card_type`, `card_num`, `name_on_card`, `exp_month`, `exp_year`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		cur.execute(ins_buy, (
			customer[0]['email'],
			num,
			flight_info[0]['dept_date'],
			flight_info[0]['dept_time'],
			flightnum,
			timestamp,
			price,
			ctype,
			cnum,
			name,
			expm,
			expy
		))
		seat = 'UPDATE `manage` SET `total_seats`= total_seats + 1'
		cur.execute(seat)
		conn.commit()
		cur.close()
		return redirect('/customer/view/myflights')
	return redirect('/login/customer')

def get_flight_info(num):
	cur = conn.cursor()
	query = 'SELECT dept_date, dept_time FROM flight WHERE flight_num = %s'
	cur.execute(query, num)
	data = cur.fetchall()
	cur.close()
	return data

def generateTicketID():
	cur = conn.cursor()
	check = True
	number = random.randint(1, 99999)
	while(check):
		query = 'SELECT * FROM ticket WHERE ID = %s'
		cur.execute(query, number)
		if(cur.fetchall()):
			number = random.randint(1,99999)
		else:
			check = False
	cur.close()
	return number
		
@app.route('/staff/viewflights')
def staffViewFlights():
	air_data = staff_check_session()
	if (air_data):
		cursor = conn.cursor()
		query = 'SELECT f.dept_date, f.dept_time, f.flight_num, f.arr_time, f.arr_airport, f.arr_date, f.base_price, f.id_airplane, f.dept_airport, f.stats FROM flight as f, manage as m, air_staff as s WHERE m.airline_name = s.airline_name AND m.flight_num = f.flight_num'	
		cursor.execute(query)
		data = cursor.fetchall()
		cursor.close()
		return render_template('staff-view-flights.html', flight = data, airline_name=air_data)



@app.route('/staff/reports')
def viewReports():
	airline = staff_check_session()
	if (airline):
		cursor = conn.cursor()
		query = 'SELECT DISTINCT count(b.ticket_id) as total, MONTH(b.purchase_timestamp) as m, YEAR(b.purchase_timestamp) as y, b.flight_num FROM buys as b, manage as m WHERE b.flight_num = m.flight_num and m.airline_name = %s group by b.flight_num, m, y'
		cursor.execute(query, airline[0]['airline_name'])
		data = cursor.fetchall()
		cursor.close()
		labels = [ 'Flight #' + str(line['flight_num']) + ': ' + (str(line['m']) + '/'+ str(line['y'])) for line in data]
		values = [int(line['total']) for line in data]
		values.append(0)		

		return render_template('staff-reports.html', data =data, labels=labels, values=values)
	return redirect('/login/staff')

@app.route('/staff/reports/search', methods=['GET', 'POST'])
def searchReports():
	air_data = staff_check_session()
	if (air_data):
		startDate = request.form['startDate']
		endDate = request.form['endDate']
		cursor = conn.cursor()
		query = 'SELECT count(b.ticket_id) as total,  MONTH(b.purchase_timestamp) as m, YEAR(b.purchase_timestamp) as y, b.flight_num FROM buys as b, manage as m WHERE %s <= b.purchase_timestamp and b.purchase_timestamp < %s and b.flight_num = m.flight_num and m.airline_name = %s group by b.flight_num, m,y'
		cursor.execute(query, (
			startDate+ "00:00:00",
			endDate+ "00:00:00",
			air_data[0]['airline_name']
		))
		data = cursor.fetchall()
		cursor.close()
		labels = ['Flight #' + str(line['flight_num']) + ': ' + (str(line['m']) + '/'+ str(line['y'])) for line in data]
		values = [int(line['total']) for line in data]
		values.append(0)		

		return render_template('staff-reports.html', data =data, labels=labels, values=values)
	return redirect('/login/staff')

@app.route('/staff/view/customers')
def viewCustomers():
	airline = staff_check_session()
	if (airline):
		cursor = conn.cursor()
		query = 'SELECT distinct c.name, c.email FROM customer as c, buys as b, manage as m  WHERE c.email = b.email and b.flight_num = m.flight_num and m.airline_name = %s and YEAR(b.purchase_timestamp) = %s'
		cursor.execute(query, (
			airline[0]['airline_name'],
			date.today().strftime("%Y")
			))
		data = cursor.fetchall() 

		return render_template('staff-view-customer.html', airline= airline[0]['airline_name'], customer = data, date =date.today().strftime("%Y") )
	return redirect('/login/staff')

@app.route('/staff/view/specfic/customer',  methods=['GET', 'POST'])
def viewSpecficCustomer():
	airline = staff_check_session()
	if (airline):
		customer_email = request.form['email']
		cursor = conn.cursor()
		query = 'SELECT DISTINCT c.name, f.flight_num, f.dept_date, f.arr_date, f.dept_airport, f.arr_airport, f.id_airplane FROM flight as f, buys as b, manage as m, customer as c WHERE  b.email = c.email and b.email = %s and b.flight_num = f.flight_num and f.flight_num = m.flight_num and m.airline_name = %s'
		cursor.execute(query,(
			customer_email,
			airline[0]['airline_name']
		))
		data = cursor.fetchall()
		cursor.close()
		return render_template('staff-specific-cus.html', details=data)
	return redirect('/login/staff')

@app.route('/viewAirplane')
def viewAirplane():
	airline = staff_check_session()
	if (airline):
		cursor = conn.cursor()
		query = 'SELECT * FROM airplane WHERE airline_name = %s'
		cursor.execute(query, airline[0]['airline_name'])
		data = cursor.fetchall()
		cursor.close()
		return render_template('view-airplane.html', data=data)
	return redirect('login/staff')


@app.route('/addAirplane', methods=['GET', 'POST'])
def addAirplane():
	if (staff_check_session):
		return render_template('addAirplane.html')
	return redirect('/login/staff')

@app.route('/addAirplaneAuth', methods=['GET', 'POST'])
def addAirplaneAuth():
	airline = staff_check_session()
	if (airline):
		ID = request.form['idAirplane']
		numSeats = request.form['numSeats']
		manufact = request.form['manuCompany']
		age = request.form['age']
		cursor = conn.cursor()
		check = 'SELECT * FROM airplane WHERE id_airplane = %s'
		cursor.execute(check, ID)
		if cursor.fetchall():
			error = "Airplane Already Exists"
			cursor.close()
			return render_template('staff-errorpage.html', error=error)

		query = 'INSERT INTO `airplane`(`id_airplane`, `airline_name`, `num_of_seats`, `manufacturing_company`, `age`) VALUES (%s,%s,%s,%s,%s)'
		cursor.execute(query, (
			ID,
			airline[0]['airline_name'],
			numSeats,
			manufact,
			age
		))
		conn.commit()
		cursor.close()
		return redirect('/viewAirplane')
	return redirect('/login/staff')

@app.route('/addAirport', methods=['GET', 'POST'])
def addAirport():
	if (staff_check_session):
		return render_template('addAirport.html')
	return redirect('/login/staff')

@app.route('/addAirportAuth', methods=['GET', 'POST'])
def addAirportAuth():
	airplane = staff_check_session()
	if (airplane):
		airportName = request.form['airportName']
		city = request.form['city']
		country = request.form['country']
		airport_type = 	request.form['airportType']
		cursor = conn.cursor()
		check = 'SELECT * FROM airport WHERE name_airport = %s'
		cursor.execute(check, airportName)
		data = cursor.fetchall()
		query = 'INSERT INTO `airport`(`name_airport`, `city`, `country`, `airport_type`) VALUES (%s,%s,%s,%s)'
		error = None
		if (data):
			error = "Airport already exists"
			return render_template('addAirport.html', error=error)
		else:
			cursor.execute(query, (
				airportName,
				city,
				country,
				airport_type
			))
			conn.commit()
			cursor.close()
			return redirect('/staff/home')
	return redirect('/login/staff')

@app.route('/customer/review')
def reviews():
	name = cus_check_session()
	date = get_format_date()
	print(date)
	if (name):
		cursor = conn.cursor()
		query = 'SELECT flight_num, ticket_id, dept_date FROM buys where dept_date <= %s and email = %s'
		cursor.execute(query, (
			date,
			name[0]['email']
		))
		data = cursor.fetchall()
		cursor.close()
		return render_template('cus-review.html', data=data)
	return redirect('/login/customer')
@app.route('/customer/addReview',methods=['GET', 'POST'])
def addReview():
	customer = cus_check_session()
	if (customer):
		ticket = request.form['ticket_id']
		rating = request.form['rating']
		comment = request.form['comment']
		cursor = conn.cursor()
		query = 'UPDATE buys set ratings=%s, comments=%s WHERE ticket_id =%s and email = %s'
		cursor.execute(query, (
			rating,
			comment,
			ticket,
			customer[0]['email']
		)) 
		conn.commit()
		cursor.close()
		return redirect('/customer/home')
	return redirect('/login/customer')

@app.route('/customer/spending')
def viewSpending():
	customer = cus_check_session()
	if (customer):
		cursor = conn.cursor()
		query = 'SELECT sum(sold_price) as total, MONTH(purchase_timestamp) as m, YEAR(purchase_timestamp) as y FROM `buys` WHERE email = %s GROUP BY m,y'
		cursor.execute(query, customer[0]['email'])
		data = cursor.fetchall()
	
		labels = [(str(line['m']) + '/'+ str(line['y'])) for line in data]
		values = [float(line['total']) for line in data]
		values.append(0)		
		cursor.close()
		return render_template('cus-track-spending.html', total=data, labels = labels, values=values)
	return redirect('/login/customer')
@app.route('/customer/spending/search', methods=['GET', 'POST'])
def searchSpending():
	customer = cus_check_session()
	if customer:
		startMonth = request.form['startMonth']
		startYear = request.form['startYear']
		endMonth = request.form['endMonth']
		endYear = request.form['endYear']
		cursor = conn.cursor()
		query = 'SELECT sum(sold_price) as total, MONTH(purchase_timestamp) as m, YEAR(purchase_timestamp) as y FROM `buys` WHERE email = %s and (MONTH(purchase_timestamp) >= %s and YEAR(purchase_timestamp) >= %s) and ((MONTH(purchase_timestamp)>= %s and YEAR(purchase_timestamp)<=%s) OR (MONTH(purchase_timestamp)<=%s and YEAR(purchase_timestamp)<=%s))GROUP BY m,y'
		cursor.execute(query, (
			customer[0]['email'],
			startMonth,
			startYear,
			endMonth,
			endYear,
			endMonth,
			endYear
		))
		data = cursor.fetchall()
		labels = [(str(line['m']) + '/'+ str(line['y'])) for line in data]
		values = [float(line['total']) for line in data]
		values.append(0)		
		cursor.close()
		return render_template('cus-track-spending.html', total=data, labels = labels, values=values)
	return redirect('/login/customer')


@app.route('/viewPreviousFlights')
def viewPreviousFlights():
	if (staff_check_session):
		return render_template('pastFlights.html')
	return redirect('/login/staff')

@app.route('/viewPreviousFlightsAuth')
def viewPreviousFlightsAuth():
	air_data = staff_check_session()
	
	#print(air_data[0][])
	if (air_data):
		error= None
		air_name = air_data[0]['airline_name']
		cursor = conn.cursor()
		query = 'SELECT distinct m.flight_num FROM manage as m, buys as b WHERE m.airline_name = %s and m.flight_num = b.flight_num and b.ratings IS NOT NULL and b.comments is NOT NULL'
		#query = 'SELECT distinct b.flight_num, avg(b.ratings) as avg_rating, b.comments FROM buys as b, manage as m WHERE m.airline_name = %s and m.flight_num = b.flight_num GROUP BY b.flight_num ,b.comments'
		cursor.execute(query, (air_name))
		data = cursor.fetchall()
		
		cursor.close()
		return render_template('pastFlights.html', flight = data, airline_name = air_name)#, average = average)

	return redirect('/login/staff')

@app.route('/viewPreviousFlightsAuth2', methods=['GET', 'POST'])
def viewPreviousFlightsAuth2():
	air_data = staff_check_session()
	if (air_data):
		air_name = air_data[0]['airline_name']
		flight_num = request.form['flight_num']
		cursor = conn.cursor()
		query = 'SELECT distinct b.flight_num, b.ratings, b.comments FROM buys as b, manage as m WHERE m.airline_name = %s and m.flight_num = b.flight_num and b.flight_num = %s and (b.ratings IS NOT NULL and b.comments IS NOT NULL)'
		cursor.execute(query, (air_name, flight_num))
		data = cursor.fetchall()
		print('DATA: ', data)
		
		values = [int(line['ratings']) for line in data]  
		sumvalues = sum(values)
		count_values = len(values)
		if count_values == 0:
			average = "No Average Rating"
		else:
			average = sumvalues/count_values
		
		cursor.close()
		return render_template('FlightStats.html', flight = data, airline_name = air_name, average = average, flight_num = flight_num)
	

	return redirect('/login/staff')

@app.route('/logout/customer') 
def logout_customer():
	session.pop('email')
	return redirect('/')

@app.route('/logout/staff')
def logout_staff():
	session.pop('username')
	return redirect('/')

def staff_check_session():
	data = None
	try:
		staff = session['username']
		air_cur = conn.cursor()
		airline_name = 'SELECT airline_name FROM air_staff where username = %s'
		air_cur.execute(airline_name, staff)
		data =air_cur.fetchall()
		air_cur.close()
	finally:
		return data
def cus_check_session():
	data = None
	try:
		user = session['email']
		cursor = conn.cursor()
		query = 'SELECT * FROM customer WHERE email =%s'
		cursor.execute(query,user)
		data =cursor.fetchall()
		cursor.close()

	finally:
		return data
def get_format_date():
	today = date.today()	  
	return today.strftime('%Y-%m-%d')
	
def get_date():
	today = date.today()	  
	# return datetime.today().strftime('%Y-%m-%d')  
	now = datetime.now() 
	#dd/mm/YY H:M:S
	dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
	print("date and time =", dt_string)	
	return dt_string
def get_timestamp():
	today = date.today()	  
	# return datetime.today().strftime('%Y-%m-%d')  
	now = datetime.now() 
	#dd/mm/YY H:M:S
	dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
	print("date and time =", dt_string)	
	return dt_string

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION

if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)

