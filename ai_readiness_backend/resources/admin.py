from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Organization
from resources.decorators import admin_required

admin_ns = Namespace('admin', description='Super Admin Operations')
from models import db, User



# ==== Schemas ====
org_model = admin_ns.model('Organization', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True),
    'industry': fields.String,
    'size': fields.String
})

user_model = admin_ns.model('User', {
    'id': fields.Integer(readonly=True),
    'email': fields.String(required=True),
    'full_name': fields.String,
    'role': fields.String,
    'organization_id': fields.Integer
})

# ==== ORG CRUD ====
@admin_ns.route('/orgs')
class OrgList(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        return [vars(org) for org in Organization.query.all()]

    @jwt_required()
    @admin_required
    @admin_ns.expect(org_model)
    def post(self):
        data = admin_ns.payload
        org = Organization(**data)
        db.session.add(org)
        db.session.commit()
        return vars(org), 201

@admin_ns.route('/orgs/<int:org_id>')
class OrgDetail(Resource):
    @jwt_required()
    @admin_required
    def get(self, org_id):
        org = Organization.query.get_or_404(org_id)
        return vars(org)

    @jwt_required()
    @admin_required
    @admin_ns.expect(org_model)
    def put(self, org_id):
        org = Organization.query.get_or_404(org_id)
        for key, value in admin_ns.payload.items():
            setattr(org, key, value)
        db.session.commit()
        return vars(org)

    @jwt_required()
    @admin_required
    def delete(self, org_id):
        org = Organization.query.get_or_404(org_id)
        db.session.delete(org)
        db.session.commit()
        return {'message': 'Organization deleted.'}


# ==== USER CRUD ====
@admin_ns.route('/users')
class UserList(Resource):
    @jwt_required()
    @admin_required
    def get(self):
        return [vars(user) for user in User.query.all()]

    @jwt_required()
    @admin_required
    @admin_ns.expect(user_model)
    def post(self):
        data = admin_ns.payload
        user = User(**data)
        
        db.session.add(user)
        db.session.commit()
        return vars(user), 201

@admin_ns.route('/users/<int:user_id>')
class UserDetail(Resource):
    @jwt_required()
    @admin_required
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return vars(user)

    @jwt_required()
    @admin_required
    @admin_ns.expect(user_model)
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        for key, value in admin_ns.payload.items():
            setattr(user, key, value)
        db.session.commit()
        return vars(user)

    @jwt_required()
    @admin_required
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted.'}
