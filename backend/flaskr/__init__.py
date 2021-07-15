#-------------------------------------------------------------------------------#
# Imports.
#-------------------------------------------------------------------------------#
import os
from flask import Flask, json, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

#-------------------------------------------------------------------------------#
# Paginate question.
#-------------------------------------------------------------------------------#
QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in questions]
    current_question = questions[start:end]

    return current_question

#-------------------------------------------------------------------------------#
# Create and configure app.
#-------------------------------------------------------------------------------#


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={'/': {'origins': '*'}})

    #-------------------------------------------------------------------------------#
    # after_request.
    #-------------------------------------------------------------------------------#
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PUT, POST, DELETE, OPTIONS')

        return response

    #-------------------------------------------------------------------------------#
    # Categories.
    #-------------------------------------------------------------------------------#
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        current_category = paginate_questions(request, categories)
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        if len(current_category) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories_dict
        })

    #-------------------------------------------------------------------------------#
    # Questions.
    #-------------------------------------------------------------------------------#
    @app.route('/questions')
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        current_question = paginate_questions(request, questions)
        categories = Category.query.order_by(Category.id).all()
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type

        if len(current_question) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_question,
            'total_questions': len(questions),
            'categories': categories_dict,
        })

    #-------------------------------------------------------------------------------#
    # Delete question.
    #-------------------------------------------------------------------------------#
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        if question is None:
            abort(404)

        question.delete()
        return jsonify({
            'success': True,
            'deleted': question_id
        })

    #-------------------------------------------------------------------------------#
    # Create and search question.
    #-------------------------------------------------------------------------------#
    @app.route('/questions', methods=['POST'])
    def create_and_search_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)
        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search))
                ).all()
                current_questions = paginate_questions(request, selection)
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all()),
                })
            else:
                question = Question(
                    new_question,
                    new_answer,
                    new_category,
                    new_difficulty
                )
                question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)
                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                })
        except BaseException:
            abort(422)

    #-------------------------------------------------------------------------------#
    # Questions in category.
    #-------------------------------------------------------------------------------#

    @app.route('/categories/<int:category_id>/questions')
    def questions_in_category(category_id):
        questions = Question.query.filter(
            Question.category == category_id).all()
        current_question = paginate_questions(request, questions)

        if len(current_question) == 0:
            abort(404)

        return jsonify({
            'questions': current_question,
            'total_questions': len(questions),
            'current_category': category_id
        })

    #-------------------------------------------------------------------------------#
    # Play game.
    #-------------------------------------------------------------------------------#
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()
        previous_questions = body['previous_questions']
        category_id = body['quiz_category']['id']
        questions = None

        if category_id != 0:
            questions = Question.query.filter_by(category=str(category_id))
        else:
            questions = Question.query.all()

        current_question = ''

        for question in questions:
            if question.id not in previous_questions:
                current_question = question.format()
                break

        return jsonify({
            'success': True,
            'question': current_question,
        })

    #-------------------------------------------------------------------------------#
    # Errors.
    #-------------------------------------------------------------------------------#
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': "bad request"
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "questions not found"
        }), 404

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': "unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': "enternal server error"
        })

    return app
