import requests
import mysql.connector as mariadb
import datetime
import os
import keyring
from dotenv import load_dotenv

load_dotenv()

cred = keyring.get_credential("MySQL", "root")
user = cred.username
password = cred.password

def refresh_access_token(refresh_token):
    url = "https://bankaccountdata.gocardless.com/api/v2/token/refresh/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = {"refresh": refresh_token}

    response = requests.request("POST", url, headers=headers, json=data)
    response_json = response.json()
    new_access_token = response_json["access"]
    return new_access_token


# NEW: get accounts from requisition
def get_account_ids(access_token, requisition_id):
    url = f"https://bankaccountdata.gocardless.com/api/v2/requisitions/{requisition_id}/"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)
    response_json = response.json()
    return response_json.get("accounts", [])


def get_transactions(access_token, account_id):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)

    date_from = yesterday.strftime('%Y-%m-%d')
    date_to = yesterday.strftime('%Y-%m-%d')

    url = f"https://bankaccountdata.gocardless.com/api/v2/accounts/{account_id}/transactions/?date_from={date_from}&date_to={date_to}"

    headers = {
        "Accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {access_token}"
    }

    response = requests.request("GET", url, headers=headers)
    response_json = response.json()

    transactions = response_json.get("transactions", {}).get("booked", [])
    return transactions



def insert_transaction(transactions):
    connection = None
    cursor = None

    insert_query = """
      insert ignore into bills (transactionID, entryReference, bookingDate, valueDate, amount, currency,
                                debtorName, creditorName, remittanceInformationUnstructured,
                                proprietaryBankTransactionCode, internalTransactionId)
      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
      """
    try:

        connection = mariadb.connect(host=os.environ["HOST"], user=user, password=password, database=os.environ["DATABASE"])
        cursor = connection.cursor()
        connection.autocommit = False

        for transaction in transactions:
            transactionId = transaction.get("transactionId")
            entryReference = transaction.get("entryReference", None)
            bookingDate = transaction.get("bookingDate")
            valueDate = transaction.get("valueDate")
            amount = transaction.get("transactionAmount", {}).get("amount")
            currency = transaction.get("transactionAmount", {}).get("currency")
            creditorName = transaction.get("creditorName")
            debtorName = transaction.get("debtorName")
            remittanceInformationUnstructured = transaction.get("remittanceInformationUnstructured", None)
            proprietaryBankTransactionCode = transaction.get("proprietaryBankTransactionCode", None)
            internalTransactionId = transaction.get("internalTransactionId", None)

            data = (transactionId, entryReference, bookingDate, valueDate, amount, currency,
                    debtorName, creditorName, remittanceInformationUnstructured,
                    proprietaryBankTransactionCode, internalTransactionId)

            cursor.execute(insert_query, data)
        #-- commit outside the loop to avoid partial loads
        connection.commit()
    except Exception as e:
        raise e
    finally:
        try:
            cursor.close()
            connection.close()
        except Exception as e:
            print(e)

def main():
    refresh_token = keyring.get_password('refresh_token', 'refresh_token')

    access_token = refresh_access_token(refresh_token)
    account_ids = get_account_ids(access_token, os.environ["44063370-fb4a-4c29-bb88-41b489683583"])

    # EXACT SAME ONE-LINE CALL YOU USED — now loops accounts
    for account_id in account_ids:
        insert_transaction(get_transactions(access_token, account_id))
if __name__ == "__main__":
    main()
