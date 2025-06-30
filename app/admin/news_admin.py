from flask_admin.contrib.sqla import ModelView
from flask import redirect, request, flash, url_for
from flask_admin import expose
from app.models.news import NewsModel
from app.utils.scraper import scrape_vegetables
from app import db

class NewsAdmin(ModelView):
    list_template = '/admin/newsmodel/list.html'
    can_create = False
    can_delete = True
    can_edit = True
    column_searchable_list = ['name']
    column_sortable_list = ['name', 'price', 'updated_at']
    column_list = ['name', 'price', 'created_at', 'updated_at']
    

    @expose('/scrape')
    def scrape_news(self):
        try:
            data = scrape_vegetables()
            for item in data:
                existing = NewsModel.query.filter_by(name=item['name']).first()
                if existing:
                    existing.price = item['price']
                else:
                    new_item = NewsModel(name=item['name'], price=item['price'])
                    db.session.add(new_item)
            db.session.commit()
            flash("News updated from external source.", "success")
        except Exception as e:
            flash(f"Scraping failed: {str(e)}", "error")

        return redirect(url_for('.index_view'))


    @expose('/')
    def index_view(self):
        if request.args.get('scrape') == 'true':
            return self.scrape_news()
        return super().index_view()
