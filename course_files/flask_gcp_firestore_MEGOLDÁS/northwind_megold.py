# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials #☻, auth
from firebase_admin import firestore
#from firebase_admin import FirebaseError
import logging
from datetime import datetime

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

@app.route('/order_proc', methods=['POST', 'GET']) 
def order_proc():  # take a new order
    try:
        if request.method == 'POST': # we take the order only if the route was called form the other form
            success=0
            # checking the stock
            doc_product = db.collection('products').document(str(request.form['product'])) # we query a single product by product ID
            stock = float(doc_product.get({'unitsinstock'}).to_dict().get('unitsinstock'))
            # alternative solution: 
            # stock_doc = doc.get({'unitsinstock'}) # the argument of doc.get() is a sequence of field paths, the returned value is a DOCUMENT
            # stock = stock_doc.get('unitsinstock')
            unitprice = int(doc_product.get({'unitprice'}).to_dict().get('unitprice')) # don't forget that money type is simulated by storing 100*real value
            if (stock < int(request.form['qt'])):
                logging.info("...order ERROR: stock too low")
                success = 1 # ERROR: stock too low
            else: 
                # checking the balance 
                doc_customer = db.collection('customers').document(request.form['customer']) # we query a single customer
                balance = int(doc_customer.get({'balance'}).to_dict().get('balance')) 
                if (balance < unitprice*float(request.form['qt'])):             
                    logging.info("...order ERROR: balance too low")
                    success = 2 # ERROR: balance too low            
            if (success==0): # we modify the db only if everything is fine
                logging.info("...updating stock...")            
                doc_product.update({'unitsinstock': stock-float(request.form['qt'])}) # doc.set() creates a new doc or completely overwrites the existing doc
                logging.info("...updating balance...")            
                doc_customer.update({'balance': balance-unitprice*float(request.form['qt'])}) 
                logging.info("...adding new order...")            
                doc = db.collection('orders').document()   # a new document is created, automatic ID is generated
                doc.set({'customerid': request.form['customer'], 'orderdate': datetime.now(), 'customer' : 'customers/'+request.form['customer']+'/'}) # the customer field is a reference type
                item = doc.collection('details').document()
                item.set({'productid': request.form['product'], 'product': 'products/'+request.form['product']+'/', 'quantity': request.form['qt']})
            return render_template('order_list.html', success=success, order_records=list_orders())
        else:
            #return render_template('order_list.html', order_records=[])
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

