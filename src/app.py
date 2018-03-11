from flask import Flask
from flask import request as reqs
from flask import make_response,jsonify
import json
from weather import *
app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    req = reqs.get_json(silent=True,force=True)
    print("Request:")
    print(req,"\n\n")
    print("\n",req.get("result").get("action"))
    res = makeWebhookResult(req)
    return res

def makeWebhookResult(req):
    print("Entered")
    print("\n",req.get("result").get("action"))
    if req.get("result").get("action")== "currency.convert":
        print("Entered")
        res = currencyConvertHook(req)
        return res
    elif req.get("result").get("action")== "weather":
        print("Entered")
        res = weatherHook(req)
        return res
    else:
        return { }

def currencyConvertHook(req):
    result = req.get("result")
    parameters = result.get("parameters")
    currency_to = parameters.get("currency-to")
    currency_from = parameters.get("currency-from")
    amount = parameters.get("amount")
    speech = str(amount)+" "+currency_from + " = "+currency_to

    return jsonify(error=False, speech=speech)

def weatherHook(req):
    print('here')
    city = req.get('result').get('parameters').get('geo-city')
    res = getWeather(city)
    # res = {'done': True}
    print('weather result: ', res)
    return jsonify(res)
    # return 'working'






if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)
