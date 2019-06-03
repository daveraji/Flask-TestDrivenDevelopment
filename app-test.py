import unittest
import os
import tempfile
import app

class BasicTestCase(unittest.TestCase):

    def test_index(self):
        tester = app.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_database(self):
        tester = os.path.exists('flaskr.db')
        self.assertEqual(tester, True)

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        #set up a blank temporary database before each test
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.init_db()

    def tearDown(self):
        #destroys the blank database are every test
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def login(self, username, password):
        #this is the login helper function
        return self.app.post('/login', data=dict(username=username, password=password), follow_redirects=True)

    def logout(self):
        #logout helper function
        return self.app.get('/logout', follow_redirects=True)

    def test_empty_db(self):
        #makes sure that the database is blank
        rv = self.app.get('/')
        assert b'No entries yet. Add some!' in rv.data

    def test_login_logout(self):
        #test login and logout using helper funtions that you outlined earlier
        rv = self.login(app.app.config['USERNAME'], app.app.config['PASSWORD'])
        assert b'You were logged in' in rv.data
        rv = self.logout()
        assert b'You were logged out' in rv.data
        rv = self.login(app.app.config['USERNAME'] + 'blah', app.app.config['PASSWORD'])
        assert b'Invalid Username' in rv.data
        rv = self.login(app.app.config['USERNAME'], app.app.config['PASSWORD'] + 'blah')
        assert b'Invalid Password' in rv.data

    def test_messages(self):
        #make sure that a user can post test_messages
        self.login(app.app.config['USERNAME'], app.app.config['PASSWORD'])
        rv = self.app.post('/add', data=dict(title='<Hello>', text='<strong>HTML</strong> allowed here'), follow_redirects=True)
        assert b'No entries yet. Add some!' not in rv.data
        assert b'&lt;Hello&gt;' in rv.data
        assert b'<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
    unittest.main()
