from flask import request
from flask_smorest import abort, Blueprint
from flask.views import MethodView

from db import db
from models.store import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

import uuid

from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")


@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store
        # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(404, message="Store not found.")

    def delete(self, store_id):
        store=StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return{"message": "Item deleted."}
        # try:
        #     del stores[store_id]
        #     return {"message": "Store deleted."}
        # except KeyError:
        #     abort(404, message="Store not found.")

@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store=StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists")
        except SQLAlchemyError:
            abort(500, message="An error occured creating the store.")
        # for store in stores.values():
        #     if (store_data["name"] == store["name"]):
        #         abort(400, message="Store already exists.")
                
        # store_id = uuid.uuid4().hex
        # store = {**store_data, "id": store_id}
        # stores[store_id] = store

        return store