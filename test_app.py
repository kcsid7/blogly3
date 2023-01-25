from unittest import TestCase

from app import app
from models import User, db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

# with app.app_context():
#     db.create_all()

class UserTestCase(TestCase):
    """Tests for User Model"""

    def setUp(self):
        with app.app_context():
            User.query.delete()

    def tearDown(self):
        with app.app_context():
          db.session.rollback()

    def test_new_user_redirect(self):
        """ Test add new user post redirect """
        with app.test_client() as client:
            resp = client.post("/users/new", data = {
                "first_name": "John", 
                "last_name": "Smith", 
                "image_url": "/static/img/default.jpg"
                })
            self.assertEqual(resp.status_code, 302)

    def test_user_model(self):
        """ Test add new user post redirect """
        new_user = User(first_name="John", last_name="Smith", image_url="/static/img/default.jpg")
        self.assertEquals(new_user.full_name(), "John Smith")

                

        

