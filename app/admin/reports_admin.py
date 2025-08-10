from app.admin.SecureModelView import SecureModelView
from wtforms.fields import TextAreaField
from wtforms.widgets import TextArea
from markupsafe import Markup

class ReportAdmin(SecureModelView):
    can_create = True
    can_edit = True
    can_delete = True

    column_list = ('user_id', 'crop_name', 'disease', 'recommendation', 'image_url', 'created_at')
    column_searchable_list = ('crop_name', 'disease')


    form_overrides = {
        'recommendation': TextAreaField
    }

    form_widget_args = {
        'recommendation': {
            'rows': 5,
            'style': 'resize: vertical'
        }
    }

    def _format_image(self, context, model, name):
        if model.image_url:
            return Markup(
                f'<a href="{model.image_url}" target="_blank">'
                f'<img src="{model.image_url}" style="height: 60px;"></a>'
            )
        return 'No Image'

    column_formatters = {
        'image_url': _format_image,
        # no formatter for user_id, will display as integer
    }

