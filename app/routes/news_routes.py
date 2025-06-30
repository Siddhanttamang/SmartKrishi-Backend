from flask import Blueprint, jsonify
from app.models.news import NewsModel

news_bp = Blueprint('news_bp', __name__)

# GET all stored news from DB (for mobile app)
@news_bp.route('/news', methods=['GET'])
def get_all_news():
    news_list = NewsModel.query.order_by(NewsModel.updated_at.desc()).all()
    return jsonify({
        "status": "success",
        "data": [item.to_dict() for item in news_list]
    }), 200
