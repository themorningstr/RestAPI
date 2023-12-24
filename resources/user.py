from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema, BlockListSchema
from models import UserModel, BlockListModel
from db import db

from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from blocklist import BLOCKLIST
from sqlalchemy.exc import SQLAlchemyError


blp = Blueprint("User", __name__ , description = "Operation on Users")


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):

        user = UserModel(
            username = user_data["username"],
            password = pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    @blp.arguments(BlockListSchema)
    @blp.response(201, BlockListSchema)
    def post(self):
        jti = get_jwt()["jti"]
        block_data = BlockListModel(**jti)
        try:
            db.session.add(block_data)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "An Error Occured Whilst inserting blocked auth key data into DB")

        return {"Message" : "Key has been inserted into DB."}

 
@blp.route("/user/<int:user_id>")
class User(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.add(user)
        db.session.commit()

        return {"message": "User deleted"}, 201


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200



         
     