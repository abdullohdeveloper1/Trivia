import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres', '12', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "How are you?",
            "answer": "I am fine",
            "category": "Art",
            "difficulty": 5
        }

        self.another_question = {
            "question": "Hello",
            "difficulty": 1,
            "category": "Art"
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()
    
    def tearDown(self):
        pass

    #-------------------------------------------------------------------------------#
    # Get categories.
    #-------------------------------------------------------------------------------#
    def test_for_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['categories'])

    #-------------------------------------------------------------------------------#
    # Get categories. (error)
    #-------------------------------------------------------------------------------#
    def test_for_404_error(self):
        response = self.client().get('/categories/lorem')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'questions not found')
    
    #-------------------------------------------------------------------------------#
    # Get question.
    #-------------------------------------------------------------------------------#
    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    #-------------------------------------------------------------------------------#
    # Get question. (error)
    #-------------------------------------------------------------------------------#
    def test_get_questions_failed(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertTrue(data['message'], "resource not found")


    #-------------------------------------------------------------------------------#
    # Search question.
    #-------------------------------------------------------------------------------#
    def test_search_question(self):
        response = self.client().post('/question', json={'searchTerm': 'Which'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    #-------------------------------------------------------------------------------#
    # Search question. (error)
    #-------------------------------------------------------------------------------#
    def test_search_question_failed(self):
        response = self.client().post('/question')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'questions not found')

    #-------------------------------------------------------------------------------#
    # Delete question.
    #-------------------------------------------------------------------------------#
    def test_delete_question(self):
        last = Question.query.all()[-1].id
        response = self.client().delete(f'/question/{last}')

        data = json.loads(response.data)

        question = Question.query.filter(Question.id == last).one_or_none()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['deleted'], last)
        self.assertIsNone(question)

    #-------------------------------------------------------------------------------#
    # Delete question. (error)
    #-------------------------------------------------------------------------------#
    def test_delete_question_failed(self):
        response = self.client().delete(f'question/122222')
        data = json.loads(response.data)

        question = Question.query.filter(Question.id == 122222).one_or_none()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'questions not found')
        self.assertIsNone(question)

    #-------------------------------------------------------------------------------#
    # Create question.
    #-------------------------------------------------------------------------------#
    def test_create_question(self):
        response = self.client().post('/question', json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(question.difficulty)

    #-------------------------------------------------------------------------------#
    # Create question (error).
    #-------------------------------------------------------------------------------#
    def test_create_question_for_method_not_allowed(self):
        response = self.client().post('/question/1', json=self.another_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'questions not found')

if __name__ == "__main__":
    unittest.main()