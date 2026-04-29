import firebase_admin
from firebase_admin import credentials 
from firebase_admin import firestore
import time

cred = credentials.Certificate("token.json")
firebase_admin.initialize_app(cred)   
db = firestore.client() 
transaction = db.transaction()
cust_ref = db.collection('customers').document('test2')

@firestore.transactional
def update_in_transaction(transaction, cust_ref):
    cust_ref_snapshot = cust_ref.get(transaction=transaction)
    new_balance = cust_ref_snapshot.get('balance') + 1000
    time.sleep(10)
    if (new_balance <= 100000):
        transaction.update(cust_ref, {'balance': new_balance})
        print("Balance increased")  
    else:
        print("Balance already maximal")  

update_in_transaction(transaction, cust_ref)
