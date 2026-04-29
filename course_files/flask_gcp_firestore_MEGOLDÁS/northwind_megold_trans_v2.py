# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials #☻, auth
from firebase_admin import firestore
#from firebase_admin import FirebaseError
import logging
from datetime import datetime
import time

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
@app.route('/order_form', methods=['POST', 'GET']) 
def order_form():
    try:
        logging.info("...listing products and customers...")
        # loading the product combo 
        docs = db.collection('products').stream() # this returns all documents 
        product_list = []
        for doc in docs:  # the dictionary returned by doc.to_dict() does not contain the doc.id, 
                        # so we must assemple the combo item manually from the doc.id and the productname field
      #      print (doc.to_dict())
            product_list.append({'productid': doc.id, 'productname': doc.get('productname')})
        # loading the customer combo 
        docs = db.collection('customers').stream()  
        cust_list = []
        for doc in docs:
            cust_list.append({'customerid': doc.id, 'companyname': doc.get('companyname')})
        return render_template('order_form.html', product_records=product_list, cust_records=cust_list)
    except Exception as error:
        print("Firestore query error: ", error)

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
                time.sleep(10) # 10 seconds delay for test
                logging.info("...updating stock...")            
                transaction.update(doc_product, {'unitsinstock': stock-qt}) 
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

@app.route('/order_proc', methods=['POST', 'GET']) 
def order_proc():  # take a new order
    try:
        if request.method == 'POST': # we take the order only if the route was called form the other form
            logging.info("...starting transaction for " + request.form['customer'])
            doc_product = db.collection('products').document(str(request.form['product'])) # we query a single product by product ID
            doc_customer = db.collection('customers').document(request.form['customer']) # we query a single customer
            transaction = db.transaction() # the transaction must be created in the HTTP request handler, not in the main app
            success = perform_transaction(transaction, doc_product, doc_customer, int(request.form['qt']), request.form['customer'])
            return render_template('order_list.html', success=success, order_records=list_orders())
        else:
            return render_template('order_list.html', order_records=list_orders())
    except Exception as error:
        print("Firestore order processing error: ", error)

def list_orders():
# This is the query that we are to implement:
# select o.orderdate::timestamp(0) without time zone AS orderdate, c.companyname, c.country, c.balance, p.productname, od.quantity, od.quantity * od.unitprice AS value, p.unitsinstock
# from products p join orderdetails od on p.productid=od.productid
# 	join orders o on o.orderid=od.orderid
# 	join customers c on c.customerid=o.customerid
# order by orderdate desc limit 5;    
    try:
        order_list = []
        doc_customers_ref = db.collection('customers')
        doc_products_ref = db.collection('products')
        doc_last_orders_ref = db.collection('orders')
        filter = doc_last_orders_ref.order_by('orderdate', direction=firestore.Query.DESCENDING).limit(5) # the last 5 orders
        doc_last_orders = filter.stream()
        for doc_order in doc_last_orders:
            odate = doc_order.get('orderdate')
            customerid = doc_order.get('customerid')
            # find company name, country and balance in the matching customer document
            this_customer = doc_customers_ref.document(customerid) # we query a single customer
            balance = int(this_customer.get({'balance'}).to_dict().get('balance')) / 100 # we stored in the db the mutiple of the real balance         
            companyname = this_customer.get({'companyname'}).to_dict().get('companyname')
            country = this_customer.get({'country'}).to_dict().get('country')
            # iterate the items
            items = db.collection('orders/'+doc_order.id+'/details').stream() # get all order items. We'll create a table row for each item
            for doc_item in items: 
                # print(doc_item.to_dict()) # debug
                quantity = int(doc_item.get('quantity'))
                # find product name and units in stock in the matching product document
                this_product = doc_products_ref.document(doc_item.get('productid')) # we query a single product. Productid is already a string.
                productname = this_product.get({'productname'}).to_dict().get('productname')
                unitsinstock = this_product.get({'unitsinstock'}).to_dict().get('unitsinstock')
                unitprice = int(this_product.get({'unitprice'}).to_dict().get('unitprice')) / 100
                order_list.append({'date': odate, 'companyname': companyname, 'country': country, 'balance': balance, 'productname': productname, 'quantity': quantity, 'value': quantity*unitprice, 'unitsinstock': unitsinstock})        
        return order_list   
    except Exception as error:
        print("Order listing error: ", error)

try:
    # open Firestore connection
    cred = credentials.Certificate("token.json")
    firebase_admin.initialize_app(cred)   
    db = firestore.client()  # we connect
    logging.info("...Firebase connected...")    
    if (db):
        if __name__ == "__main__":
            app.run(debug=True)
except Exception as error:
    print("Connect error: ", error)

