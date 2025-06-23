from flask import Blueprint, request, jsonify
from flask_restful import Resource, reqparse, fields, marshal_with, Api, abort
from app.models.report import ReportModel
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask import current_app
from uuid import uuid4

# Blueprint setup
report_bp = Blueprint('report_bp', __name__)
api = Api(report_bp)

# Request parser
report_args = reqparse.RequestParser()

report_args.add_argument('crop', type=str, required=True, help="Crop is required")
report_args.add_argument('disease', type=str, required=True, help="Disease is required")
report_args.add_argument('recommendation', type=str, required=True, help="Recommendation is required")
report_args.add_argument('image_url', type=str, help="Image URL or base64 string")
report_args.add_argument('user_id', type=int, help="Optional: will be overridden by JWT")

report_fields = {
    'id': fields.Integer,
    'crop_name': fields.String,
    'disease': fields.String,
    'recommendation': fields.String,
    'image_url': fields.String(attribute=lambda x: request.host_url.rstrip('/') + x.image_url if x.image_url else None),
    'user_id': fields.Integer,
    'created_at': fields.String
}
class ReportListResource(Resource):
    @jwt_required()
    @marshal_with(report_fields)
    def get(self):
        user_id = int(get_jwt_identity())
        report = ReportModel.query.filter_by(user_id=user_id).all()
        if not report:
            abort(404, message="Report not found")
        return report
    @jwt_required()
    def delete(self, id):
        user_id = int(get_jwt_identity())
        report = ReportModel.query.filter_by(id=id, user_id=user_id).first()
        if not report:
            abort(404, message="Report not found")

        db.session.delete(report)
        db.session.commit()
        return {'message': 'Report deleted successfully'}, 200

    @jwt_required()
    @marshal_with(report_fields)
    def post(self):
        user_id = int(get_jwt_identity())

        # Expect multipart/form-data
        crop = request.form.get('crop')
        disease = request.form.get('disease')
        recommendation = request.form.get('recommendation')
        image = request.files.get('image')

        if not all([crop, disease, recommendation, image]):
            return {'message': 'All fields including image are required'}, 400

        # Generate unique filename to avoid conflicts
        ext = os.path.splitext(secure_filename(image.filename))[1]
        unique_filename = f"{uuid4().hex}{ext}"

        # Save image
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        image.save(filepath)

        image_url = f"/uploads/{unique_filename}"

        # Save report
        new_report = ReportModel(
            crop_name=crop,
            disease=disease,
            recommendation=recommendation,
            image_url=image_url,
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
        report = ReportModel.query.filter_by(id=id, user_id=user_id).first()
        if not report:
            abort(404, message="Report not found")
        return report

# Register routes
api.add_resource(ReportListResource, '/report')
api.add_resource(ReportResource, '/report/<int:id>')

