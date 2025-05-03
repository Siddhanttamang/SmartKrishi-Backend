from flask import Blueprint, request, jsonify
from flask_restful import Resource, reqparse, fields, marshal_with, Api, abort
from app.models.result_set import ResultSetModel
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

# Blueprint setup
resultset_bp = Blueprint('resultset_bp', __name__)
api = Api(resultset_bp)

# Request parser
report_args = reqparse.RequestParser()
report_args.add_argument('class_name', type=str, required=True, help="Class name is required")
report_args.add_argument('report', type=str, required=True, help="Report is required")

# Response fields (no image_path)
report_fields = {
    'id': fields.Integer,
    'class_name': fields.String,
    'report': fields.String,
    'user_id': fields.Integer
}

class ReportListResource(Resource):
    @jwt_required()
    @marshal_with(report_fields)
    def get(self):
        user_id = int(get_jwt_identity())
        return ResultSetModel.query.filter_by(user_id=user_id).all()

    @jwt_required()
    @marshal_with(report_fields)
    def post(self):
        user_id = int(get_jwt_identity())
        args = report_args.parse_args()

        new_report = ResultSetModel(
            class_name=args['class_name'],
            report=args['report'],
            user_id=user_id
        )
        db.session.add(new_report)
        db.session.commit()
        return new_report, 201

class ReportResource(Resource):
    @jwt_required()
    @marshal_with(report_fields)
    def get(self, id):
        user_id = int(get_jwt_identity())
        report = ResultSetModel.query.filter_by(id=id, user_id=user_id).first()
        if not report:
            abort(404, message="Report not found")
        return report

# Register routes
api.add_resource(ReportListResource, '/report')
api.add_resource(ReportResource, '/report/<int:id>')

