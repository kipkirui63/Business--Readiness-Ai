# from flask import request
# from flask_restx import Namespace, Resource, fields
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from utils.scoring import compute_scores
# from utils.pdf_report import generate_pdf
# from utils.email_utils import send_pdf_email
# import os
# from resources.decorators import admin_required
# from models import (
#     db, Assessment, UseCaseEvaluation, DataReadinessEvaluation,
#     TechInfraEvaluation, TeamReadinessEvaluation
# )

# readiness_ns = Namespace('readiness', description='AI Readiness Assessment')

# # Define input models
# use_case_model = readiness_ns.model('UseCase', {
#     'description': fields.String,
#     'value': fields.Integer,
#     'feasibility': fields.Integer,
#     'priority': fields.Integer,
# })

# data_model = readiness_ns.model('DataReadiness', {
#     'data_availability': fields.Integer,
#     'data_quality': fields.Integer,
#     'integration_level': fields.Integer,
# })

# infra_model = readiness_ns.model('TechInfra', {
#     'cloud_ready': fields.Boolean,
#     'compute_power_score': fields.Integer,
#     'tools_stack_maturity': fields.Integer,
#     'apis_ready': fields.Boolean,
# })

# team_model = readiness_ns.model('TeamReadiness', {
#     'ai_skills_level': fields.Integer,
#     'training_needs': fields.String,
#     'leadership_support': fields.Integer,
# })

# assessment_model = readiness_ns.model('Assessment', {
#     'organization_id': fields.Integer,
#     'use_case': fields.Nested(use_case_model),
#     'data_readiness': fields.Nested(data_model),
#     'tech_infra': fields.Nested(infra_model),
#     'team_readiness': fields.Nested(team_model),
#     'recommendation': fields.String
# })


# @readiness_ns.route('/submit')
# class SubmitAssessment(Resource):
#     @jwt_required()
#     @readiness_ns.expect(assessment_model)
#     def post(self):
#         user_id = get_jwt_identity()
#         data = request.get_json()


#         scores = compute_scores(data)
#         # You can use the score to determine recommendation
#         if scores['total'] > 75:
#             recommendation = "You're AI-ready!"
#         elif scores['total'] > 50:
#             recommendation = "You’re on your way. Improve data and infra readiness."
#         else:
#             recommendation = "Start with foundational AI planning."

#         assessment.recommendation = recommendation

#         # Create assessment
#         assessment = Assessment(
#             user_id=user_id,
#             organization_id=data.get('organization_id'),
#             recommendation=data.get('recommendation')
#         )
#         db.session.add(assessment)
#         db.session.flush()  # get assessment.id

#         # Add nested evaluations
#         use_case = UseCaseEvaluation(
#             assessment_id=assessment.id, **data['use_case']
#         )
#         data_ready = DataReadinessEvaluation(
#             assessment_id=assessment.id, **data['data_readiness']
#         )
#         tech_infra = TechInfraEvaluation(
#             assessment_id=assessment.id, **data['tech_infra']
#         )
#         team_ready = TeamReadinessEvaluation(
#             assessment_id=assessment.id, **data['team_readiness']
#         )

#         db.session.add_all([use_case, data_ready, tech_infra, team_ready])
#         db.session.commit()



#         # Generate and send PDF report
#         pdf_path = f'tmp/report_{assessment.id}.pdf'
#         generate_pdf(assessment, scores, pdf_path)

#         send_pdf_email(
#             to_email=assessment.user.email,
#             subject='Your AI Readiness Assessment Report',
#             body='Hi, find attached your AI readiness report.',
#             pdf_path=pdf_path
# )

#         return {'message': 'Assessment submitted successfully.'}, 201


# @readiness_ns.route('/my')
# class MyAssessments(Resource):
#     @jwt_required()
#     def get(self):
#         user_id = get_jwt_identity()
#         assessments = Assessment.query.filter_by(user_id=user_id).all()

#         result = []
#         for a in assessments:
#             result.append({
#                 'id': a.id,
#                 'date_submitted': a.date_submitted.isoformat(),
#                 'recommendation': a.recommendation,
#                 'organization_id': a.organization_id
#             })

#         return {'assessments': result}



# @readiness_ns.route('/<int:assessment_id>')
# class GetAssessment(Resource):
#     @jwt_required()
#     def get(self, assessment_id):
#         assessment = Assessment.query.get(assessment_id)
#         if not assessment:
#             return {'message': 'Assessment not found'}, 404
        
#         result = {
#             'id': assessment.id,
#             'recommendation': assessment.recommendation,
#             'date_submitted': assessment.date_submitted.isoformat(),
#             'use_case': assessment.use_case,
#             'data_readiness': assessment.data_readiness,
#             'tech_infra': assessment.tech_infra,
#             'team_readiness': assessment.team_readiness,
#         }
#         return result

# @readiness_ns.route('/all')
# class AllAssessments(Resource):
#     @jwt_required()
#     @admin_required
#     def get(self):
#         assessments = Assessment.query.all()
#         result = []
#         for a in assessments:
#             result.append({
#                 'id': a.id,
#                 'user': {
#                     'id': a.user.id,
#                     'email': a.user.email,
#                     'name': a.user.full_name
#                 },
#                 'date_submitted': a.date_submitted.isoformat(),
#                 'recommendation': a.recommendation,
#                 'organization_id': a.organization_id
#             })
#         return {'assessments': result}


# @readiness_ns.route('/delete/<int:assessment_id>')
# class DeleteAssessment(Resource):
#     @jwt_required()
#     @admin_required
#     def delete(self, assessment_id):
#         assessment = Assessment.query.get(assessment_id)
#         if not assessment:
#             return {'message': 'Assessment not found'}, 404

#         db.session.delete(assessment)
#         db.session.commit()
#         return {'message': 'Assessment deleted.'}


from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.scoring import compute_scores
from utils.pdf_report import generate_pdf
from utils.email_utils import send_pdf_email
from resources.decorators import admin_required
from models import (
    db, Assessment, UseCaseEvaluation, DataReadinessEvaluation,
    TechInfraEvaluation, TeamReadinessEvaluation, User
)

readiness_ns = Namespace('readiness', description='AI Readiness Assessment')

# Models
use_case_model = readiness_ns.model('UseCase', {
    'description': fields.String,
    'value': fields.Integer,
    'feasibility': fields.Integer,
    'priority': fields.Integer,
})

data_model = readiness_ns.model('DataReadiness', {
    'data_availability': fields.Integer,
    'data_quality': fields.Integer,
    'integration_level': fields.Integer,
})

infra_model = readiness_ns.model('TechInfra', {
    'cloud_ready': fields.Boolean,
    'compute_power_score': fields.Integer,
    'tools_stack_maturity': fields.Integer,
    'apis_ready': fields.Boolean,
})

team_model = readiness_ns.model('TeamReadiness', {
    'ai_skills_level': fields.Integer,
    'training_needs': fields.String,
    'leadership_support': fields.Integer,
})

assessment_model = readiness_ns.model('Assessment', {
    'organization_id': fields.Integer,
    'use_case': fields.Nested(use_case_model),
    'data_readiness': fields.Nested(data_model),
    'tech_infra': fields.Nested(infra_model),
    'team_readiness': fields.Nested(team_model),
})


@readiness_ns.route('/create')
class CreateAssessment(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()
        assessment = Assessment(user_id=user_id, organization_id=data.get('organization_id'))
        db.session.add(assessment)
        db.session.commit()
        return {'id': assessment.id, 'message': 'Blank assessment created.'}, 201


@readiness_ns.route('/<int:assessment_id>')
class GetAssessmentById(Resource):
    @jwt_required()
    def get(self, assessment_id):
        assessment = Assessment.query.get_or_404(assessment_id)
        return {
            'id': assessment.id,
            'organization_id': assessment.organization_id,
            'recommendation': assessment.recommendation,
            'date_submitted': assessment.date_submitted.isoformat() if assessment.date_submitted else None
        }


@readiness_ns.route('/user/<int:user_id>')
class GetUserAssessments(Resource):
    @jwt_required()
    def get(self, user_id):
        assessments = Assessment.query.filter_by(user_id=user_id).all()
        return [{'id': a.id, 'recommendation': a.recommendation} for a in assessments]


@readiness_ns.route('/recommendations/<int:assessment_id>')
class GetRecommendations(Resource):
    @jwt_required()
    def get(self, assessment_id):
        assessment = Assessment.query.get_or_404(assessment_id)
        scores = compute_scores({
            'use_case': {
                'value': assessment.use_case.value,
                'feasibility': assessment.use_case.feasibility,
                'priority': assessment.use_case.priority
            },
            'data_readiness': {
                'data_availability': assessment.data_readiness.data_availability,
                'data_quality': assessment.data_readiness.data_quality,
                'integration_level': assessment.data_readiness.integration_level
            },
            'tech_infra': {
                'cloud_ready': assessment.tech_infra.cloud_ready,
                'compute_power_score': assessment.tech_infra.compute_power_score,
                'tools_stack_maturity': assessment.tech_infra.tools_stack_maturity,
                'apis_ready': assessment.tech_infra.apis_ready
            },
            'team_readiness': {
                'ai_skills_level': assessment.team_readiness.ai_skills_level,
                'training_needs': assessment.team_readiness.training_needs,
                'leadership_support': assessment.team_readiness.leadership_support
            }
        })

        return {'recommendation': assessment.recommendation, 'score': scores}


@readiness_ns.route('/use-case')
class SaveUseCase(Resource):
    @jwt_required()
    @readiness_ns.expect(use_case_model)
    def post(self):
        data = request.get_json()
        use_case = UseCaseEvaluation(**data)
        db.session.add(use_case)
        db.session.commit()
        return {'message': 'Use case saved successfully.'}, 201


@readiness_ns.route('/data-readiness')
class SaveDataReadiness(Resource):
    @jwt_required()
    @readiness_ns.expect(data_model)
    def post(self):
        data = request.get_json()
        data_ready = DataReadinessEvaluation(**data)
        db.session.add(data_ready)
        db.session.commit()
        return {'message': 'Data readiness saved successfully.'}, 201


@readiness_ns.route('/technical-infrastructure')
class SaveTechInfra(Resource):
    @jwt_required()
    @readiness_ns.expect(infra_model)
    def post(self):
        data = request.get_json()
        tech_infra = TechInfraEvaluation(**data)
        db.session.add(tech_infra)
        db.session.commit()
        return {'message': 'Tech infrastructure saved successfully.'}, 201


@readiness_ns.route('/team-readiness')
class SaveTeamReadiness(Resource):
    @jwt_required()
    @readiness_ns.expect(team_model)
    def post(self):
        data = request.get_json()
        team_ready = TeamReadinessEvaluation(**data)
        db.session.add(team_ready)
        db.session.commit()
        return {'message': 'Team readiness saved successfully.'}, 201


