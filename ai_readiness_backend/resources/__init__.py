from flask import Flask
from flask_restx import Api
from flask_jwt_extended import JWTManager
from config import Config
from extensions import db, migrate, mail
from resources.admin import admin_ns
from resources.readiness import readiness_ns
from resources.assessment import assessment_ns

from models import (
    User,
    Organization,
    Assessment,
    UseCaseEvaluation,
    DataReadinessEvaluation,
    TechInfraEvaluation,
    TeamReadinessEvaluation
)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt = JWTManager(app)

    # Initialize API and register namespaces
    api = Api(app, version='1.0', title='Business AI Readiness API')
    api.add_namespace(admin_ns, path='/admin')
    api.add_namespace(readiness_ns,path='/readiness')
    api.add_namespace(assessment_ns, path="/assessment")

    
    # api.add_namespace(assessment_ns, path='/assessment')
    # api.add_namespace(use_case_ns, path='/use-case')
    # api.add_namespace(data_readiness_ns, path='/data-readiness')
    # api.add_namespace(technical_infra_ns, path='/technical-infrastructure')
    # api.add_namespace(team_readiness_ns, path='/team-readiness')


    return app
