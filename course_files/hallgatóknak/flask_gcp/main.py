# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import psycopg2
from psycopg2 import Error
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/')
@app.route('/order_form', methods=['POST', 'GET']) 
def order_form():
    try:
        # product combo feltöltése
        cursor.execute("""select productid, productname from products order by productname;""")
        product_rows = cursor.fetchall()
        product_list = []
        for row in product_rows:  
            product_list.append({'productid': row[0], 'productname': row[1]})
        # customer combo feltöltése
        cursor.execute("""select customerid, companyname from customers order by companyname;""")
        cust_rows = cursor.fetchall()
        cust_list = []
        for row in cust_rows:  
            cust_list.append({'customerid': row[0], 'companyname': row[1]})
        return render_template('order_form.html', product_records=product_list, cust_records=cust_list)
    except (Exception, Error) as error:
        print("Lekérdezési hiba", error)

@app.route('/order_proc', methods=['POST', 'GET']) 
def order_proc():  # felvétel futtatása
    try:
        if request.method == 'POST': # ha űrlapról hívták, felvesszük az új rendelést
            sql = """select new_order(%s, %s, %s);"""
            with connection: # ha nem with: blokkban van, akkor nem autocommit a tranzakció, nem csinál semmit https://www.psycopg.org/docs/connection.html
                with connection.cursor() as c:
                    c.execute(sql, (request.form['product'], request.form['qt'], request.form['customer'],))
                    row = c.fetchone() # ha row[0] == 0, akkor sikeres
                    # siker esetén utána megnyitjuk a rendelés-listázást    
                    return render_template('order_list.html', success=row[0], order_records=list_orders())
        else:
            return render_template('order_list.html', order_records=list_orders())
    except (Exception, Error) as error:
        print("Lekérdezési vagy rendelés-felvételi hiba: ", error)

def list_orders():
    try:
        cursor.execute("""select * from last_orders;""") # ez egy view
        order_rows = cursor.fetchall()
        order_list = []
        for row in order_rows:  
            order_list.append({'date': row[0], 'companyname': row[1], 'country': row[2], 'balance': row[3], 'productname': row[4], 'quantity': row[5], 'value': row[6], 'unitsinstock': row[7]})        
        return order_list   
    except (Exception, Error) as error:
        print("Connect Error", error)

try:
    connection = psycopg2.connect(user="postgres", password="my_pass", host="my_GCP_IP", port="5432", database="postgres")
    cursor = connection.cursor()
    if (connection):
        logging.info("...app indul...")
        app.run(debug=True)
except (Exception, Error) as error:
    print("Connect Error: ", error)

