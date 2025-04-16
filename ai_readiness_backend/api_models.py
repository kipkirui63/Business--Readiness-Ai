from flask_restx import fields
from extensions import api

user_model = api.model('User', {
    'username': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(required=False)
})

login_model = api.model('Login', {
    'email': fields.String(required=True),
    'password': fields.String(required=True)
})

data_readiness_model = api.model('DataReadiness', {
    'data_source': fields.String(required=True),
    'status': fields.String(required=True),
    'last_checked': fields.DateTime(required=True)
})

technical_infra_model = api.model('TechnicalInfrastructure', {
    'infrastructure_name': fields.String(required=True),
    'status': fields.String(required=True),
    'last_checked': fields.DateTime(required=True)
})

team_readiness_model = api.model('TeamReadiness', {
    'team_member_name': fields.String(required=True),
    'role': fields.String(required=True),
    'availability': fields.String(required=True)
})
