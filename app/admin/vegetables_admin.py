from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup

class VegetableAdmin(ModelView):
    can_delete = True
    can_edit = True
    column_searchable_list = ['name']

    column_sortable_list = ['name', 'price']
    column_list = ['name', 'quantity', 'price', 'seller_name', 'image']

    column_labels = {
        'seller_name': 'Seller',
        'image': 'Image',
        'name': 'Vegetable Name',
    }

    def _format_image(self, context, model, name):
        if model.image_url:
            return Markup(
                f'<a href="{model.image_url}" target="_blank">'
                f'<img src="{model.image_url}" style="height: 60px;"></a>'
            )
        return 'No Image'

    def _format_seller_name(self, context, model, name):
        return model.user.name if model.user else 'Unknown'

    column_formatters = {
        'image': _format_image,
        'seller_name': _format_seller_name,
    }
