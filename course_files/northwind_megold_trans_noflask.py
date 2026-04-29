# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials #☻, auth
from firebase_admin import firestore
#from firebase_admin import FirebaseError
import logging
from datetime import datetime
import time


logging.basicConfig(level=logging.INFO)



@firestore.transactional
def perform_transaction (transaction, doc_product, doc_customer, qt, cust_id):
    try:
        logging.info("     ...in transaction for " + cust_id)
        success=0
        # checking the stock
        doc_product_snapshot = doc_product.get(transaction=transaction)
        stock = doc_product_snapshot.get('unitsinstock')
        unitprice =  doc_product_snapshot.get('unitprice')
        productid = doc_product_snapshot.id
        if (stock < qt):
            logging.info("...order ERROR: stock too low")
            success = 1 # ERROR: stock too low
        else: 
            # checking the balance 
            doc_customer_snapshot = doc_customer.get(transaction=transaction)
            balance = doc_customer_snapshot.get('balance')
            customerid = doc_customer_snapshot.id
            if (balance < unitprice*qt):             
                logging.info("...order ERROR: balance too low")
                success = 2 # ERROR: balance too low            
            else: # we modify the db only if everything is fine                
                time.sleep(5) # 20 seconds delay for test
                logging.info("...updating stock...")            
                transaction.update(doc_product, {'unitsinstock': stock-qt}) 
                # print(1/0) # error to test atomicity -> result: the first update is NOT rolled back
                logging.info("...updating balance...")            
                transaction.update(doc_customer, {'balance': balance-unitprice*qt}) 
                logging.info("...adding new order...")            
                doc_order = db.collection('orders').document()  
                transaction.set(doc_order, {'customerid': customerid, 'orderdate': datetime.now(), 'customer' : 'customers/'+customerid+'/'}) # the customer field is a reference type
                doc_item = doc_order.collection('details').document()
                transaction.set(doc_item, {'productid': productid, 'product': 'products/'+productid+'/', 'quantity': qt})
        return success
    except Exception as error:
        print("Firestore transaction processing error: ", error)

try:
    # open Firestore connection
    cred = credentials.Certificate("token.json")
    firebase_admin.initialize_app(cred)   
    db = firestore.client()  # we connect
    transaction = db.transaction()
    logging.info("...Firebase connected...")    
    doc_product = db.collection('products').document('1')
    doc_customer = db.collection('customers').document('ALFKI')
    success = perform_transaction(transaction, doc_product, doc_customer, 3, 'ALFKI')

except Exception as error:
    print("Connect error: ", error)

