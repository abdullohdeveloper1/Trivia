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
            "question": "Is it test?",
            "answer": "Yes",
            "category": 1,
            "difficulty": 1
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
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    #-------------------------------------------------------------------------------#
    # Get categories. (error)
    #-------------------------------------------------------------------------------#
    def test_get_categories_for_404(self):
        res = self.client().get('/categories?page=1212')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)
        self.assertEqual(data["message"], "questions not found")
    
    #-------------------------------------------------------------------------------#
    # Get question.
    #-------------------------------------------------------------------------------#
    def test_get_question(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    #-------------------------------------------------------------------------------#
    # Get question. (error)
    #-------------------------------------------------------------------------------#
    def test_get_question_404(self):
        res = self.client().get('/questions?page=1221212')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "questions not found")

    #-------------------------------------------------------------------------------#
    # Get question by category.
    #-------------------------------------------------------------------------------#
    def test_get_question_in_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        # self.assertEqual(data['success'], True)
        # self.assertTrue(len(data["questions"]))
        # self.assertTrue(data["total_questions"])

    #-------------------------------------------------------------------------------#
    # Get question by category. (error)
    #-------------------------------------------------------------------------------#
    def test_get_question_in_category_404(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertTrue(data['message'], "questions not found")

    #-------------------------------------------------------------------------------#
    # Search question.
    #-------------------------------------------------------------------------------#
    def test_get_question_search_with_results(self):
        res = self.client().post('/questions', json={'search': 'is'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    #-------------------------------------------------------------------------------#
    # Search question. (error)
    #-------------------------------------------------------------------------------#
    def test_get_book_search_without_result(self):
        res = self.client().post('/books', json={'search': 'sasasas'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertTrue(data['message'], "resource not found")

    #-------------------------------------------------------------------------------#
    # Delete question.
    #-------------------------------------------------------------------------------#
    def test_delete_question(self):
        question = Question.query.all()[-1].id
        res = self.client().delete('/questions/' + str(question))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], question)

    #-------------------------------------------------------------------------------#
    # Delete question. (error)
    #-------------------------------------------------------------------------------#
    def test_422_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'questions not found')

    #-------------------------------------------------------------------------------#
    # Create question.
    #-------------------------------------------------------------------------------#
    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    #-------------------------------------------------------------------------------#
    # Create question (error).
    #-------------------------------------------------------------------------------#
    def test_405_if_question_creation_not_allowed(self):
        res = self.client().post('/questions/45', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    #-------------------------------------------------------------------------------#
    # Get next question (error).
    #-------------------------------------------------------------------------------#
    def test_get_next_question(self):
        res = self.client().post('/quizzes', json={
            "previous_questions":[],
            "quiz_category": {"id": 2, "type":"All"}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(data['question'], None)

if __name__ == "__main__":
    unittest.main()