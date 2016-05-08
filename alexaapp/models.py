from alexaapp.database import db
from sqlalchemy_utils import EncryptedType, ChoiceType

class User(db.Model):
    """A user capable of listening to voicemails"""
    __tablename__ = 'user'

    email = db.Column(db.String, primary_key=True)
    session_token = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
