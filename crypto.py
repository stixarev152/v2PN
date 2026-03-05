import requests
from config import CRYPTO_TOKEN

API = "https://pay.crypt.bot/api"


def create_invoice(amount):

    headers = {
        "Crypto-Pay-API-Token": CRYPTO_TOKEN
    }

    data = {
        "asset":"USDT",
        "amount":amount
    }

    r = requests.post(API+"/createInvoice",headers=headers,json=data).json()

    return r["result"]["pay_url"], r["result"]["invoice_id"]


def check_invoice(invoice_id):

    headers = {
        "Crypto-Pay-API-Token": CRYPTO_TOKEN
    }

    r = requests.get(API+"/getInvoices",headers=headers).json()

    for i in r["result"]["items"]:
        if i["invoice_id"] == invoice_id:
            return i["status"]

    return "active"
