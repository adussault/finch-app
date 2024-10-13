from flask import render_template, request, flash, redirect, url_for, session

from app import app
from finch import Finch
from .forms import CreateSandbox
from .app_data import providers, products
from .funcs import create_sandbox_provider, get_sandbox_employee_directory, query_finch_sandbox_api, check_response_code

import requests

create_sandbox_url = "https://sandbox.tryfinch.com/api/sandbox/create"



@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html', app_is_authenticated=False)


@app.route('/setup', methods=['GET', 'POST'])
def setup():
	form = CreateSandbox()
	if form.validate_on_submit():
		print("FORM RECEIVED")
		print(f'Form Provider: {form.provider.data}')
		session["name"] = form.name.data
		session['provider'] = form.provider.data
		session['products'] = form.products.data
		response = create_sandbox_provider(form.provider.data, form.products.data, employee_size=20)
		

		# Check response for errors

		if (400 <= response.status_code  < 500):
			flash("Call to Finch Sandbox failed with the error: \n" + str(response.status_code) + " - " + str(response.json()))
			return render_template('400_errors.html', error=response.status_code, message=response.json())

		if response.status_code >= 500:
			flash("Call to Finch Sandbox failed with the error: \n" + str(response.status_code) + " - " + str(response.json()))
			return render_template('500_errors.html', error_json=response.json())

		if type(response.json()) == str:
			flash(response.json())
			return redirect(url_for('index'))
			
		print("Status: ")
		print(response.status_code)
		print(response.json())
		print("Access token: " + response.json().get('access_token'))
		# Load API data and token into storage
		"""
		example response headers
			{'Age': '3', 
			 'Cache-Control': 'no-cache', 
			 'Cache-Status': '"Netlify Durable"; fwd=method, 
			 "Netlify Edge"; fwd=miss', 
			 'Content-Encoding': 'gzip', 
			 'Content-Type': 'application/json; charset=utf-8', 
			 'Date': 'Wed, 
			 09 Oct 2024 07:02:37 GMT', 
			 'Etag': '"2av8izridn6k-df"', 
			 'Netlify-Vary': 'cookie=__next_preview_data:presence|__prerender_bypass:presence,query', 
			 'Server': 'Netlify', 
			 'Strict-Transport-Security': 'max-age=31536000', 
			 'Vary': 'Accept-Encoding', 
			 'X-Nf-Render-Mode': 'ssr', 
			 'X-Nf-Request-Id': '01J9R1CARVVW19M02CSBQ96XST', 
			 'Transfer-Encoding': 'chunked'}

		example response json
		{'payroll_provider_id': 'gusto',
		 'company_id': '38249979-961e-4c91-be51-0198643169f1',
		 'access_token': 'sandbox-token-27b03ba1-aed3-45e2-9b9b-e495f520347d',
		 'sandbox_time': {'unix': 1728457357253,
		  'calendar': 'Wed Oct 09 2024 07:02:37 GMT+0000'}}

		"""

		session['access_token'] = response.json().get('access_token')
		session['company_id'] = response.json().get('company_id')
		session['is_authenticated'] = True

		print ("Data loaded into session for: " + session['company_id'])
		# Redirect to Dashboard
		return redirect(url_for('employee_directory'))

	return render_template("setup.html", form=form, title="Set Up")

@app.route('/directory')
def employee_directory():
	if session["is_authenticated"] == True:
		# Check if the directory data is in the session dict and is new enough
		if not("directory_data" in session.keys()):
			response = query_finch_sandbox_api('employer/directory', session["access_token"])

			if (400 <= response.status_code  < 500):
				flash("Call to Finch Sandbox failed with the error: \n" + str(response.status_code) + " - " + str(response.json()))
				return render_template('400_errors.html', error=response.status_code, message=response.json())

			if response.status_code >= 500:
				flash("Call to Finch Sandbox failed with the error: \n" + str(response.status_code) + " - " + str(response.json()))
				return render_template('500_errors.html', error_json=response.json())

			if type(response.json()) == str:
				flash(response.json())
				return redirect(url_for('index'))
			
			# Save Data in Session:
			session["directory_data"] = response.json()
		# Otherwise pull data from session 
		data = session["directory_data"]
	else:
		return render_template("not_authenticated.html", message="Please make sure you have set up your connection.")

	return render_template("employee_directory.html", data=data)

@app.route('/company')
def company():
	if session["is_authenticated"] == True:
		# Check if the directory data is in the session dict and is new enough
		if not("company_data" in session.keys()):
			response = query_finch_sandbox_api('employer/company', session["access_token"])

			# Check Response:
			#check_response_code(response)
			if (400 <= response.status_code  < 500):
				flash("Call to Finch Sandbox failed with the error: \n" + str(response.status_code) + " - " + str(response.json()))
				return render_template('400_errors.html', error=response.status_code, message=response.json())

			if response.status_code >= 500:
				flash("Call to Finch Sandbox failed with the error: \n" + str(response.status_code) + " - " + str(response.json()))
				return render_template('500_errors.html', error_json=response.json())

			if type(response.json()) == str:
				flash(response.json())
				return redirect(url_for('index'))
			
			# Save Data in Session:
			session["company_data"] = response.json()
		# Otherwise pull data from session 
		data = session["company_data"]
	else:
		return render_template("not_authenticated.html", message="Please make sure you have set up your connection.")

	return render_template("company.html", data=data)


@app.route('/employment')
def employment():
	'''
	if type(individual_id) != str:
		flash("Individual ID must be a string.")
		return render_template("404.html")
	'''
	if not ("employment_data" in session.keys()):

		if not("directory_data" in session.keys()):
			response = query_finch_sandbox_api('employer/company', session["access_token"])

			# Check Response:
			if (400 <= response.status_code  < 500):
				flash("Call to Finch Sandbox failed with the error: \n" + str(response.status_code) + " - " + str(response.json()))
				return render_template('400_errors.html', error=response.status_code, message=response.json())

			if response.status_code >= 500:
				flash("Call to Finch Sandbox failed with the error: \n" + str(response.status_code) + " - " + str(response.json()))
				return render_template('500_errors.html', error_json=response.json())

			if type(response.json()) == str:
				flash(response.json())
				return redirect(url_for('index'))
			
			session["directory_data"] = response.json()
		
		employment_json = []

		for i in session["directory_data"]["individuals"]:
			employment_json.append({"individual_id" : i["id"]})

		employment_json = {"requests": employment_json}
		
		employment_response = query_finch_sandbox_api('employer/employment', session["access_token"], method="post", json=employment_json)
		
		if (400 <= employment_response.status_code  < 500):
			flash("Call to Finch Sandbox failed with the error: \n" + str(employment_response.status_code) + " - " + str(employment_response.json()))
			return render_template('400_errors.html', error=employment_response.status_code, message=employment_response.json())


		if employment_response.status_code >= 500:
			flash("Call to Finch Sandbox failed with the error: \n" + str(employment_response.status_code) + " - " + str(employment_response.json()))
			return render_template('500_errors.html', error_json=employment_response.json())

		if type(employment_response.json()) == str:
			flash(employment_response.json())
			return redirect(url_for('index'))
			

		session["employment_data"] = employment_response.json()

	return render_template("employment.html", data=session["employment_data"])

	if session["is_authenticated"] == True:
		# Check if the directory data is in the session dict and is new enough
		if not(("employment_data_"+individual_id) in session.keys()):


			response = query_finch_sandbox_api('employer/employment', session["access_token"])

			# Check Response:
			if (400 <= response.status_code  < 500):
				flash("Call to Finch Sandbox failed with the error: \n" + str(response.status_code) + " - " + str(response.json()))
				return render_template('400_errors.html', error=response.status_code, message=response.json())

			if response.status_code >= 500:
				flash("Call to Finch Sandbox failed with the error: \n" + str(response.status_code) + " - " + str(response.json()))
				return render_template('500_errors.html', error_json=response.json())

			if type(response.json()) == str:
				flash(response.json())
				return redirect(url_for('index'))
			
		
			# Save Data in Session:
			session["employment_data"] = response.json()
		# Otherwise pull data from session 
		data = session["employment_data"]
	else:
		return render_template("not_authenticated.html", message="Please make sure you have set up your connection.")
	





@app.route('/end_session')
def endsession():
	session.clear()
	return redirect(url_for('index'))
