from fastapi import FastAPI, Request, Response, status
from pymongo import ReturnDocument
from bson.objectid import ObjectId

from audittracker.tracker import Tracker
from models import customer, product
from utils import create_response_obj, check_table_tracker_existence
from config import firebaseConfig

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

Tracker.initialize_firebase_storage(firebaseConfig)
customer_tracker = Tracker(BASE_DIR, 'customer', '_id')
product_tracker = Tracker(BASE_DIR, 'product', '_id')

MODEL_TRACKER_MAPPER = {
  'customer': customer_tracker,
  'product': product_tracker
}

app = FastAPI()

""" CREATE A CUSTOMER """
@app.post('/api/customer', status_code = status.HTTP_201_CREATED)
async def create_customer(request: Request, response: Response):
  try:
    insert_data = await request.json()
    new_customer = customer.insert_one(insert_data)
    new_customer__id = new_customer.inserted_id
    
    response = customer.find_one({"_id": ObjectId(new_customer__id)})
    response['_id'] = str(new_customer__id)

    response_obj = create_response_obj(True, 201, response)
  except:
    response_obj = create_response_obj(False, 400, 'Something went wrong')
    response.status_code = status.HTTP_400_BAD_REQUEST
  return response_obj


""" UPDATE A CUSTOMER DATA """
@app.post('/api/customer/{customer_id}', status_code = status.HTTP_200_OK)
async def update_customer(customer_id: str, request: Request, response: Response):
  try:
    update_data = await request.json()

    try:
      customer_found = customer.find_one({"_id": ObjectId(customer_id)})
    except:
      response_obj = create_response_obj(False, 404, f"Customer with id '{customer_id}' not found.")
      response.status_code = status.HTTP_404_NOT_FOUND
      return response_obj
    
    customer_found__id = str(customer_found['_id'])
    customer_found['_id'] = customer_found__id
    query = {'_id': ObjectId(customer_found__id)}
    set_data = {'$set': update_data}
    updated_customer = customer.find_one_and_update(query, set_data, return_document = ReturnDocument.AFTER)
    updated_customer['_id'] = customer_found__id

    # Add customer tracker
    customer_tracker.track(customer_found, updated_customer)
    response_obj = create_response_obj(True, 200, updated_customer)
  except:
    response_obj = create_response_obj(False, 400, 'Something went wrong')
    response.status_code = status.HTTP_400_BAD_REQUEST
  return response_obj


""" CREATE A PRODUCT """
@app.post('/api/product', status_code = status.HTTP_201_CREATED)
async def create_product(request: Request, response: Response):
  try:
    insert_data = await request.json()
    new_product = product.insert_one(insert_data)
    new_product__id = new_product.inserted_id
    
    response = product.find_one({"_id": ObjectId(new_product__id)})
    response['_id'] = str(new_product__id)

    response_obj = create_response_obj(True, 201, response)
  except:
    response_obj = create_response_obj(False, 400, 'Something went wrong')
    response.status_code = status.HTTP_400_BAD_REQUEST
  return response_obj


""" UPDATE A PRODUCT DATA """
@app.post('/api/product/{product_id}', status_code = status.HTTP_200_OK)
async def update_product(product_id: str, request: Request, response: Response):
  try:
    update_data = await request.json()

    try:
      product_found = product.find_one({"_id": ObjectId(product_id)})
    except:
      response_obj = create_response_obj(False, 404, f"Product with id '{product_id}' not found.")
      response.status_code = status.HTTP_404_NOT_FOUND
      return response_obj
    
    product_found__id = str(product_found['_id'])
    product_found['_id'] = product_found__id
    query = {'_id': ObjectId(product_found__id)}
    set_data = {'$set': update_data}
    updated_product = product.find_one_and_update(query, set_data, return_document = ReturnDocument.AFTER)
    updated_product['_id'] = product_found__id

    # Add product tracker
    product_tracker.track(product_found, updated_product)
    response_obj = create_response_obj(True, 200, updated_product)
  except:
    response_obj = create_response_obj(False, 400, 'Something went wrong')
    response.status_code = status.HTTP_400_BAD_REQUEST
  return response_obj



""" FETCH AUDIT RECORD OF TABLE """
@app.get('/api/audit/{table_name}', status_code = status.HTTP_200_OK)
async def fetch_audit_of_table(table_name: str, response: Response):
  can_continue, tracker, message = check_table_tracker_existence(table_name, MODEL_TRACKER_MAPPER)

  if not can_continue:
    response_obj = create_response_obj(False, 404, message)
    response.status_code = status.HTTP_404_NOT_FOUND
    return response_obj
  
  table_audit = tracker.get_all_audits()
  response_obj = create_response_obj(True, 200, table_audit)
  return response_obj


""" FETCH AUDIT RECORD OF TABLE FOR TODAY """
@app.get('/api/audit/{table_name}/today', status_code = status.HTTP_200_OK)
async def fetch_audit_of_today(table_name: str, response: Response):
  can_continue, tracker, message = check_table_tracker_existence(table_name, MODEL_TRACKER_MAPPER)

  if not can_continue:
    response_obj = create_response_obj(False, 404, message)
    response.status_code = status.HTTP_404_NOT_FOUND
    return response_obj
  
  table_audit = tracker.audit_of_today()
  response_obj = create_response_obj(True, 200, table_audit)
  return response_obj


""" FETCH AUDIT RECORD OF TABLE (OF, FROM, BETWEEN) GIVEN DATES """
@app.get('/api/audit/{table_name}/{type}/date', status_code = status.HTTP_200_OK)
async def fetch_audit_by_dates(table_name: str, type: str, response: Response, sd: int = None, sm: int = None, sy: int = None, ed: int = None, em: int = None, ey: int = None, endpoints: bool = False):
  can_continue, tracker, message = check_table_tracker_existence(table_name, MODEL_TRACKER_MAPPER)

  if not can_continue:
    response_obj = create_response_obj(False, 404, message)
    response.status_code = status.HTTP_404_NOT_FOUND
    return response_obj
  
  dates = [sd, sm, sy]
  if type == 'of':
    exec_func = tracker.audit_of_date
  elif type == 'from':
    exec_func = tracker.audit_from_date
  elif type == 'between':
    dates.extend([ed, em, ey, endpoints])
    exec_func = tracker.audit_between_date
  else:
    response_obj = create_response_obj(False, 404, f"No functions defined for type '{type}'.")
    response.status_code = status.HTTP_404_NOT_FOUND
    return response_obj

  if None in dates:
    response_obj = create_response_obj(False, 404, 'Please provide with date, month and year in parameters')
    response.status_code = status.HTTP_404_NOT_FOUND
    return response_obj

  table_audit = exec_func(*dates)
  response_obj = create_response_obj(True, 200, table_audit)
  return response_obj



""" FETCH AUDIT RECORD OF TABLE FILTERED BY ID FIELD OR OPERATIONS FIELD """
@app.get('/api/audit/{table_name}/{type}/{value}', status_code = status.HTTP_200_OK)
async def fetch_audit_by_id_or_operation(table_name: str, type: str, value: str, response: Response, sd: int = None, sm: int = None, sy: int = None, ed: int = None, em: int = None, ey: int = None):
  can_continue, tracker, message = check_table_tracker_existence(table_name, MODEL_TRACKER_MAPPER)

  if not can_continue:
    response_obj = create_response_obj(False, 404, message)
    response.status_code = status.HTTP_404_NOT_FOUND
    return response_obj

  table_audit = None
  if type == 'id':
    exec_func = tracker.audit_by_id
  elif type == 'operation':
    exec_func = tracker.audit_by_operation
  else:
    response_obj = create_response_obj(False, 404, f"No functions defined for type '{type}'.")
    response.status_code = status.HTTP_404_NOT_FOUND
    return response_obj
  
  table_audit = exec_func(value, sd, sm, sy, ed, em, ey)
  table_audit = table_audit or 'No data found, Please check if you have enetered a valid operation.'
  response_obj = create_response_obj(True, 200, table_audit)
  return response_obj