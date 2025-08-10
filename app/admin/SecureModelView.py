from flask_admin.contrib.sqla import ModelView
from flask_admin.actions import action
from flask_login import current_user
from flask import redirect, url_for, flash

class SecureModelView(ModelView):

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('admin_auth.login'))

    # Remove the default delete bulk action if you want
    def get_actions(self):
        actions = super().get_actions()
        if 'delete' in actions:
            del actions['delete']
        return actions

    # Add your custom bulk action here
    @action('my_action', 'Do Something', 'Are you sure you want to do this action?')
    def action_my_action(self, ids):
        # `ids` is a list of primary keys of selected records
        # Example: just flash the count
        flash(f"Custom action executed on {len(ids)} records.", "success")

        # Here you can add your logic, e.g. update or delete rows by IDs
        # For example:
        # query = self.session.query(self.model).filter(self.model.id.in_(ids))
        # query.update({self.model.status: 'processed'}, synchronize_session='fetch')
        # self.session.commit()
