from flask import Blueprint, render_template, request,redirect, url_for,flash, Flask,session,json,jsonify
from app import *
import braintree
import os
from os.path import join, dirname
from dotenv import load_dotenv
from gateway import generate_client_token, transact, find_transaction


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
app.secret_key = os.environ.get('APP_SECRET_KEY')

braintree_blueprint = Blueprint('braintree',
                            __name__,
                            template_folder='templates')


TRANSACTION_SUCCESS_STATUSES = [
    braintree.Transaction.Status.Authorized,
    braintree.Transaction.Status.Authorizing,
    braintree.Transaction.Status.Settled,
    braintree.Transaction.Status.SettlementConfirmed,
    braintree.Transaction.Status.SettlementPending,
    braintree.Transaction.Status.Settling,
    braintree.Transaction.Status.SubmittedForSettlement
]

@braintree_blueprint.route('/', methods=['GET'])
def new_checkout():
    client_token = generate_client_token()
    return jsonify(client_token=client_token)


@braintree_blueprint.route('/checkouts', methods=['POST'])
def create_checkout():
    nonce =request.json.get('payment_method_nonce')
    
    result = transact({
        'amount': 100,
        'payment_method_nonce': nonce,
        'options': {
            "submit_for_settlement": True
        }
    })
    # amount = int(request.form.get('amount'))
    # current_id= current_user.id
    # current_email = str(current_user.email)

    if result.is_success or result.transaction:
        # print(result.transaction.id[0])
        transaction = find_transaction(result.transaction.id)
        transac = {}
        transac['id'] = transaction.id
        transac['type'] = transaction.type
        transac['amount'] = str(transaction.amount)
        transac['status'] = transaction.status
        result = {}
        if transaction.status in TRANSACTION_SUCCESS_STATUSES:
            result = {
                'header': 'Sweet Success!',
                'icon': 'success',
                'message': 'Your test transaction has been successfully processed. See the Braintree API response and try again.'
            }
        else:
            result = {
                'header': 'Transaction Failed',
                'icon': 'fail',
                'message': 'Your test transaction has a status of ' + transaction.status + '. See the Braintree API response and try again.'
            }
      
        return jsonify(message=result,transac=transac)
    else:
        
        # for x in result.errors.deep_errors: flash('Error: %s: %s' % (x.code, x.message))
        # errormessage={}
        # errormessage['errormessage'] = result.errors.deep_errors
        return jsonify(error= "error")