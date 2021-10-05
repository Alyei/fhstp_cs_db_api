from flask import Flask, request
from flask_restful import Resource, Api
import db
import simplejson

app = Flask(__name__)
api = Api(app)

class getAmountOfItem(Resource):
    def get(self, itemid):
        res = db.getAmountOfItem(itemid)
        return res

class getAmountOfItems(Resource):
    def get(self):
        res = db.getAllItems()
        return res

    def post(self):
        ids = request.json['itemids']
        res = db.getItemsByID(ids)
        return res

class removeItemsFromStock(Resource):
    def post(self):
        res = db.removeItems(request.json)

        return res

api.add_resource(getAmountOfItem, "/getAmountOfItem/<string:itemid>")
api.add_resource(getAmountOfItems, "/getAmountOfItems")
api.add_resource(removeItemsFromStock, "/removeItemsFromStock")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1337)
