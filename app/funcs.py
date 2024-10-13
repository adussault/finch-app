# Scripts for messing around with the Finch API
import os
from finch import Finch
import requests
from flask import flash, render_template
create_sandbox_url = "https://sandbox.tryfinch.com/api/sandbox/create"

def create_sandbox_provider (provider_id, products, employee_size=10):
	valid_products = ["company", "directory", "individual", "employment"]
	invalid_products = ["payment", "pay_statement"]

	if not (type(products) == list):
		raise exception("products needs to be a list")
	if not all(p in valid_products for p in products):
		raise exception("products list must only contain the values: \n 'company', 'directory', 'individual', 'employment'")
	if any(p in invalid_products for p in products):
		raise exception("payment and pay_statement are not in scope")
	request_data = {
		"provider_id": provider_id, 
		"products":products, 
		"employee_size":employee_size
	}
	response = requests.post(create_sandbox_url, data=request_data)

	return response

def query_finch_sandbox_api(path, access_token, method='get', content_type='application/json', json=None):
	if method  in ['get', 'GET', 'Get']:
		response = requests.get("https://sandbox.tryfinch.com/api/" + path, headers={
        	'Authorization': 'Bearer ' + access_token,
        	'Content-Type': content_type 
			})
		return response
	if method in ['post', 'POST', 'Post']:
		response = requests.post("https://sandbox.tryfinch.com/api/" + path, headers={
        	'Authorization': 'Bearer ' + access_token,
        	'Content-Type': content_type 
			},
			json=json)
		return response

def get_sandbox_employee_directory(access_token):
	response = requests.get("https://sandbox.tryfinch.com/api/employer/directory", headers={
        	'Authorization': 'Bearer ' + access_token,
        	'Content-Type': 'application/json' 
			})
	#client = Finch(access_token = access_token)
	return response

def check_response_code(response):
	if response.status_code > 399:
		flash("Call to Finch Sandbox failed with the error: \n" + str(response.status_code) + " - " + str(response.json()))
		return render_template('error_page.html', error_code=response.status_code, error_message=response.json())
	if type(response.json()) == str:
		flash(response.json())
		return redirect(url_for('index'), error_code=response.status_code, message=response.json())
