from config import get_app_config
from flask import abort, make_response, session
from flask_sqlalchemy import SQLAlchemy
from models import Chore, User, chore_schema, chores_schema


class _ChoresDBOperations:
    db: SQLAlchemy

    def __init__(self):
        self.db = get_app_config().db

    def read_all(self, user_id):
        chores = Chore.query.filter_by(user_id=user_id).all()
        return chores_schema.dump(chores)

    def create(self, chore):

        title = chore.get("title")
        user_id = User.query.filter_by(
            username=session['username']).first().id
        user = User.query.get(user_id)
        existing_chore = Chore.query.filter_by(title=title, user=user).first()

        if existing_chore is None:
            new_chore = chore_schema.load(chore, session=self.db.session)
            user.chores.append(new_chore)
            self.db.session.commit()

            return chore_schema.dump(new_chore), 201
        else:
            abort(
                409,
                f"Chore with title {title} already exists"
            )

    def updateCompletedField(self, chore_id, chore):
        existing_chore = Chore.query.filter_by(id=chore_id).first()
        if existing_chore is not None:
            chore["id"] = chore_id
            chore["due_date"] = str(existing_chore.due_date)
            chore["description"] = existing_chore.description
            chore["title"] = existing_chore.title
            update_chore = chore_schema.load(chore, session=self.db.session)
            self.db.session.merge(update_chore)
            self.db.session.commit()
            return chore_schema.dump(update_chore), 201
        else:
            abort(
                404,
                f"Chore with id {chore_id} not found"
            )

    def delete(self, chore_id):
        existing_chore = Chore.query.filter_by(id=chore_id).first()
        if existing_chore is not None:
            self.db.session.delete(existing_chore)
            self.db.session.commit()
            return make_response(f"{chore_id} successfully deleted", 204)
        else:
            abort(
                404,
                f"Chore with id {chore_id} not found"
            )


chores = _ChoresDBOperations()
