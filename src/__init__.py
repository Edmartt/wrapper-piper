from flask import Flask
from config import config
from src.database import postgres 
from src.database import redis_mod

def create_app(config_name: str) -> Flask:

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    #app.task_queue = rq.Queue('distances', connection=app.redis)
    postgres.init_app(app)
    redis_mod.init_app(app)
    from src.calculator import calculator_blueprint as calculator_blueprint
    app.register_blueprint(calculator_blueprint)

    return app
