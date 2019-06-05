import unittest
import os
import json
from app import app, db

TEST_DB = 'test.db'

class BasicTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_database(self): #check that db exists
        tester = os.path.exists('flaskr.db')
        self.assertTrue(tester)

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        #set up a blank temporary database before each test
        basedir = os.path.abspath(os.path.dirname(__file__))
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        #destroys the blank database are every test
        db.drop_all()

    def login(self, username, password):
        #this is the login helper function
        return self.app.post('/login', data=dict(username=username, password=password), follow_redirects=True)

    def logout(self):
        #logout helper function
        return self.app.get('/logout', follow_redirects=True)

    def test_empty_db(self):
        #makes sure that the database is blank
        rv = self.app.get('/')
        self.assertIn(b'No entries yet. Add some!', rv.data)

    def test_login_logout(self):
        #test login and logout using helper funtions that you outlined earlier
        rv = self.login(app.config['USERNAME'], app.config['PASSWORD'])
        self.assertIn(b'You were logged in', rv.data)
        rv = self.logout()
        self.assertIn(b'You were logged out' , rv.data)
        rv = self.login(app.config['USERNAME'] + 'blah', app.config['PASSWORD'])
        self.assertIn(b'Invalid Username' ,rv.data)
        rv = self.login(app.config['USERNAME'], app.config['PASSWORD'] + 'blah')
        self.assertIn(b'Invalid Password' , rv.data)

    def test_messages(self):
        #make sure that a user can post test_messages
        self.login(app.config['USERNAME'], app.config['PASSWORD'])
        rv = self.app.post('/add', data=dict(title='<Hello>', text='<strong>HTML</strong> allowed here'), follow_redirects=True)
        self.assertNotIn(b'No entries yet. Add some!' , rv.data)
        self.assertIn(b'&lt;Hello&gt;', rv.data)
        self.assertIn(b'<strong>HTML</strong> allowed here' , rv.data)

    def test_delete_message(self):
        #make sure messages are being Deleted
        rv = self.app.get('/delete/1')
        data = json.loads(rv.data)
        self.assertEqual(data['status'], 1)

    def test_search(self):
        self.login(app.config['USERNAME'], app.config['PASSWORD'])
        self.app.post('/add', data=dict(title='<Hello>', text='<strong>HTML</strong> allowed here'), follow_redirects=True)
        rv = self.app.get('/search/?query=Hello', follow_redirects=True)
        self.assertIn(b'<strong>HTML</strong> allowed here' , rv.data)

if __name__ == '__main__':
    unittest.main()
