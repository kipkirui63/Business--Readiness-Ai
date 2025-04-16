from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.scoring import compute_scores
from utils.pdf_report import generate_pdf
from utils.email_utils import send_pdf_email
from models import (
    db, Assessment, UseCaseEvaluation, DataReadinessEvaluation,
    TechInfraEvaluation, TeamReadinessEvaluation
)

assessment_ns = Namespace('assessment', description='AI Readiness Assessment API')

# Models
use_case_model = assessment_ns.model('UseCase', {
    'description': fields.String,
    'value': fields.Integer,
    'feasibility': fields.Integer,
    'priority': fields.Integer,
})

data_model = assessment_ns.model('DataReadiness', {
    'data_availability': fields.Integer,
    'data_quality': fields.Integer,
    'integration_level': fields.Integer,
})

infra_model = assessment_ns.model('TechInfra', {
    'cloud_ready': fields.Boolean,
    'compute_power_score': fields.Integer,
    'tools_stack_maturity': fields.Integer,
    'apis_ready': fields.Boolean,
})

team_model = assessment_ns.model('TeamReadiness', {
    'ai_skills_level': fields.Integer,
    'training_needs': fields.String,
    'leadership_support': fields.Integer,
})

assessment_model = assessment_ns.model('Assessment', {
    'organization_id': fields.Integer,
    'use_case': fields.Nested(use_case_model),
    'data_readiness': fields.Nested(data_model),
    'tech_infra': fields.Nested(infra_model),
    'team_readiness': fields.Nested(team_model),
})

# ✅ POST /create
@assessment_ns.route('/create')
class CreateAssessment(Resource):
    @jwt_required()
    @assessment_ns.expect(assessment_model)
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        assessment = Assessment(user_id=user_id, organization_id=data.get('organization_id'))
        db.session.add(assessment)
        db.session.commit()
        return {'message': 'Assessment created', 'id': assessment.id}, 201

# ✅ GET /<id>
@assessment_ns.route('/<int:id>')
class GetAssessment(Resource):
    @jwt_required()
    def get(self, id):
        assessment = Assessment.query.get(id)
        if not assessment:
            return {'message': 'Assessment not found'}, 404
        return {
            'id': assessment.id,
            'user_id': assessment.user_id,
            'organization_id': assessment.organization_id,
            'recommendation': assessment.recommendation,
        }

# ✅ GET /user/<user_id>
@assessment_ns.route('/user/<int:user_id>')
class UserAssessments(Resource):
    @jwt_required()
    def get(self, user_id):
        assessments = Assessment.query.filter_by(user_id=user_id).all()
        return [{'id': a.id, 'organization_id': a.organization_id} for a in assessments]

# ✅ POST /submit
@assessment_ns.route('/submit')
class SubmitAssessment(Resource):
    @jwt_required()
    @assessment_ns.expect(assessment_model)
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        scores = compute_scores(data)

        if scores['total'] > 75:
            recommendation = "You're AI-ready!"
        elif scores['total'] > 50:
            recommendation = "You’re on your way. Improve data and infra readiness."
        else:
            recommendation = "Start with foundational AI planning."

        assessment = Assessment(
            user_id=user_id,
            organization_id=data['organization_id'],
            recommendation=recommendation
        )
        db.session.add(assessment)
        db.session.flush()

        use_case = UseCaseEvaluation(assessment_id=assessment.id, **data['use_case'])
        data_ready = DataReadinessEvaluation(assessment_id=assessment.id, **data['data_readiness'])
        tech_infra = TechInfraEvaluation(assessment_id=assessment.id, **data['tech_infra'])
        team_ready = TeamReadinessEvaluation(assessment_id=assessment.id, **data['team_readiness'])

        db.session.add_all([use_case, data_ready, tech_infra, team_ready])
        db.session.commit()

        pdf_path = f'tmp/report_{assessment.id}.pdf'
        generate_pdf(assessment, scores, pdf_path)

        send_pdf_email(
            to_email=assessment.user.email,
            subject='Your AI Readiness Assessment Report',
            body='Hi, find attached your AI readiness report.',
            pdf_path=pdf_path
        )

        return {'message': 'Assessment submitted and emailed.'}, 201

# ✅ GET /recommendations/<assessment_id>
@assessment_ns.route('/recommendations/<int:assessment_id>')
class Recommendations(Resource):
    @jwt_required()
    def get(self, assessment_id):
        assessment = Assessment.query.get(assessment_id)
        if not assessment:
            return {'message': 'Assessment not found'}, 404
        return {'recommendation': assessment.recommendation}

# ✅ POST /use-case
@assessment_ns.route('/use-case')
class UseCase(Resource):
    @jwt_required()
    @assessment_ns.expect(use_case_model)
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        latest = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.id.desc()).first()
        if not latest:
            return {'message': 'No assessment found for user.'}, 404
        use_case = UseCaseEvaluation(assessment_id=latest.id, **data)
        db.session.add(use_case)
        db.session.commit()
        return {'message': 'Use case saved'}, 201

# ✅ POST /data-readiness
@assessment_ns.route('/data-readiness')
class DataReadiness(Resource):
    @jwt_required()
    @assessment_ns.expect(data_model)
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        latest = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.id.desc()).first()
        if not latest:
            return {'message': 'No assessment found for user.'}, 404
        entry = DataReadinessEvaluation(assessment_id=latest.id, **data)
        db.session.add(entry)
        db.session.commit()
        return {'message': 'Data readiness saved'}, 201

# ✅ POST /technical-infrastructure
@assessment_ns.route('/technical-infrastructure')
class TechInfra(Resource):
    @jwt_required()
    @assessment_ns.expect(infra_model)
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        latest = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.id.desc()).first()
        if not latest:
            return {'message': 'No assessment found for user.'}, 404
        entry = TechInfraEvaluation(assessment_id=latest.id, **data)
        db.session.add(entry)
        db.session.commit()
        return {'message': 'Technical infrastructure saved'}, 201

# ✅ POST /team-readiness
@assessment_ns.route('/team-readiness')
class TeamReadiness(Resource):
    @jwt_required()
    @assessment_ns.expect(team_model)
    def post(self):
        data = request.get_json()
        user_id = get_jwt_identity()
        latest = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.id.desc()).first()
        if not latest:
            return {'message': 'No assessment found for user.'}, 404
        entry = TeamReadinessEvaluation(assessment_id=latest.id, **data)
        db.session.add(entry)
        db.session.commit()
        return {'message': 'Team readiness saved'}, 201
