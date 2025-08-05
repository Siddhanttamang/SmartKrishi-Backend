from app.admin.SecureModelView import SecureModelView
from wtforms.fields import TextAreaField
from wtforms.widgets import TextArea

class ReportAdmin(SecureModelView):
    can_create = True
    can_edit = True
    can_delete = True

    column_list = ('crop_name', 'disease', 'recommendation', 'image_url', 'created_at')
    column_searchable_list = ('crop_name', 'disease')
    column_filters = ('created_at',)

    form_overrides = {
        'recommendation': TextAreaField
    }

    form_widget_args = {
        'recommendation': {
            'rows': 5,
            'style': 'resize: vertical'
        }
    }
