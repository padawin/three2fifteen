from app.model.model import Model


class AppUserModel(Model):
    fields = ('id_user', 'username', 'password', 'date_created')
