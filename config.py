from __future__ import annotations

import pathlib

import connexion
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


class _AppConfig:

    _app_config: _AppConfig

    def __init__(self) -> None:
        basedir: pathlib.Path = pathlib.Path(__file__).parent.resolve()
        self._connex_app: connexion.FlaskApp = connexion.App(
            __name__, specification_dir=basedir)

        self._setup_flask_variables(basedir)

        self.db = SQLAlchemy(self._connex_app.app)
        self.ma = Marshmallow(self._connex_app.app)

    def _setup_flask_variables(self, basedir: pathlib.Path) -> None:
        _app = self._connex_app.app
        _app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir / 'todo.db'}"
        _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        _app.secret_key = "asdsdfsdfs13sdf_df%&"

    @property
    def app(self) -> connexion.FlaskApp:
        return self._connex_app

    # Singleton Pattern
    @classmethod
    def get_app_config(cls) -> _AppConfig:
        if not hasattr(cls, "_app_config"):
            cls._app_config = cls()

        return cls._app_config


def get_app_config() -> _AppConfig:
    return _AppConfig.get_app_config()
