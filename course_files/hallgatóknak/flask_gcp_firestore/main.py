# -*- coding: utf-8 -*-
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging
import psycopg2
from psycopg2 import Error
from datetime import datetime

logging.basicConfig(level=logging.INFO)

try:
# Firestore kapcsolat
    cred = credentials.Certificate("firestore_service_acc_key.json")
    firebase_admin.initialize_app(cred)
    
    db = firestore.client()  # most csatlakozunk
    logging.info("...Firebase csatlakozott...")
    # collection = db.collection('test')  
    # doc = collection.document('FIk6WMJaGa2hBbZBDYiy')  
    # res = doc.get().to_dict()
    # print(res)

# Postgres kapcsolat

    connection = psycopg2.connect(user="postgres", password="your_pass", host="127.0.0.1", port="your_port", database="postgres")
    cursor = connection.cursor()
    logging.info("...Postgres csatlakozott...")

# Products tábla -> products kollekció
    cursor.execute("""select productid, productname, 100*unitprice::numeric::integer, unitsinstock from products;""") 
                            # nincs money típus FS-on, sőt decimális típus sincs (hehe)
                            # ezért a 2 tizedes money típust úgy szimuláljuk, hogy a 100-zal szorzott értéket int-ként tároljuk
                            # csak ne feledjük, hogy az eredményt majd mindig osztani kell 100-zal
    product_rows = cursor.fetchall()
    # töröljük az eddigi FS tartalmat
    # hogy hány doc van a kollekcióban, azt egy számlálóban célszerű számontartani (Cloud Functions for Firebase)
    docs = db.collection('products').stream() # ez az összes dokumentumot visszaadja, lehetne WHERE szűrő része is
    for doc in docs:
        if doc.exists:
            #print(doc.to_dict()) 
            doc.reference.delete()
    
    for row in product_rows:  
        doc = db.collection('products').document(str(row[0]))   # a kollekció és a dok az első hivatkozáskor létrejön, az id az első mező
                                                                # azért kellett átalakítani stringgé, mert a dok. id nem lehet szám (hehe)
        doc.set({'productname':row[1], 'unitprice':row[2], 'unitsinstock':row[3]}) # itt lehetne merge opció is, ha már létezik a doc 
        # print(doc.id)
        # print(doc.get().to_dict())

# Customers tábla -> customers kollekció
    cursor.execute("""select customerid, companyname, country, 100*balance::numeric::integer from customers;""") 
    customer_rows = cursor.fetchall()
    docs = db.collection('customers').stream() 
    for doc in docs:
        if doc.exists:
            doc.reference.delete()   
    for row in customer_rows:  
        doc = db.collection('customers').document(str(row[0]))   
        doc.set({'companyname':row[1], 'country':row[2], 'balance':row[3]})

# Orders és orderdetails táblák -> orders kollekció, items néven a tételek, mint al-kollekció az order dokumentumon belül
# az al-kollekciók legnagyobb veszélye, hogy ha a főkollekciót törlik, akkor is megmaradnak: 'orphaned'
# de mi nem akarunk soha rendelést törölni
# egy rendelést adjunk hozzá, két tétellel
    logging.info("...egy új, két tételes rendelés felvétele...")
    doc = db.collection('orders').document()   # automatikus ID
    doc.set({'customerid': 1, 'orderdate': datetime.now(), 'customer' : 'customers/1/'})
    item1 = doc.collection('details').document()
    item1.set({'productid': 3, 'product': 'products/3/', 'quantity': 8})
    item1 = doc.collection('details').document()
    item1.set({'productid': 4, 'product': 'products/4/', 'quantity': 10})
    logging.info("...feltöltés vége...")

except (Exception, Error) as error:
    print("Error: ", error)
