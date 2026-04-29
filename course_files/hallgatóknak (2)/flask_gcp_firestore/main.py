# -*- coding: utf-8 -*-
#from flask import Flask
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging
import psycopg2
from psycopg2 import Error
from datetime import datetime

logging.basicConfig(level=logging.INFO)
#app = Flask(__name__)

def upload_data():
    try:
    # open Firestore connection
        cred = credentials.Certificate("token.json")
        firebase_admin.initialize_app(cred)
        
        db = firestore.client()  # we connect
        logging.info("...Firebase connected...")
        # collection = db.collection('test')  
        # doc = collection.document('FIk6WMJaGa2hBbZBDYiy')  
        # res = doc.get().to_dict()
        # print(res)
    
    # open Postgres connection    
        connection = psycopg2.connect(user="postgres", password="h6twqPNO", host="127.0.0.1", port="14432", database="postgres")
        cursor = connection.cursor()
        logging.info("...Postgres connected...")
    
    # Products table -> products collection
        cursor.execute("""select productid, productname, 100*unitprice::numeric::integer, unitsinstock from products;""") 
                                # no money or decimal type supported on Firestore
                                # so we simulate the money type with 2 decimals by storint value*100 as int
                                # just don't forget do divide it by 100 every time at display
        product_rows = cursor.fetchall()
        # delete the existing content from Firestore
        # it is recomennded to keep track of the number of docs in a collection by a counter (Cloud Functions for Firebase)
        docs = db.collection('products').stream() # this returns all documents (it could also include a filter condition)
        for doc in docs:
            if doc.exists:
                #print(doc.to_dict()) 
                doc.reference.delete()
        
        for row in product_rows:  
            doc = db.collection('products').document(str(row[0]))   # the collection and the document is automatically created upon the frist reference
                                                                    # the productid is the first field, we store it as a string (doc id cannot be a number)
            doc.set({'productname':row[1], 'unitprice':row[2], 'unitsinstock':row[3]}) # we could use the merge option here if the doc already exists 
            print(doc.id)
            print(doc.get().to_dict())
    
    # Customers table -> customers collection
        cursor.execute("""select customerid, companyname, country, 100*balance::numeric::integer from customers;""") 
        customer_rows = cursor.fetchall()
        docs = db.collection('customers').stream() 
        for doc in docs:
            if doc.exists:
                doc.reference.delete()   
        for row in customer_rows:  
            doc = db.collection('customers').document(str(row[0]))   
            doc.set({'companyname':row[1], 'country':row[2], 'balance':row[3]})
    
    # Orders and orderdetails tables -> orders collection, items are a sub-collection named 'details' within each order doc 
    # a possible problem with sub-collections is that they survive in an 'orphaned' state even if the parent collection is deleted
    # however, we'll never want to delete an order
    # here we add a single order with two item for demo purposes
        logging.info("...adding a new order with two items...")
        doc = db.collection('orders').document()   # a new document, automatic ID is generated
        doc.set({'customerid': 1, 'orderdate': datetime.now(), 'customer' : 'customers/1/'}) # the customer field is a reference type
        item1 = doc.collection('details').document()
        item1.set({'productid': 3, 'product': 'products/3/', 'quantity': 8})
        item1 = doc.collection('details').document()
        item1.set({'productid': 4, 'product': 'products/4/', 'quantity': 10})
        logging.info("...new order added...")
    except (Exception, Error) as error:
        print("Error: ", error)


try:
    upload_data()
    #app.run(debug=True)
except (Exception, Error) as error:
    print("Error: ", error)
