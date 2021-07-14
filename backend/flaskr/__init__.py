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
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')

    return response

  #-------------------------------------------------------------------------------#
  # Categories.
  #-------------------------------------------------------------------------------#
  @app.route('/categories')
  def get_categories():
    categories = Category.query.order_by(Category.id).all()
    current_category = paginate_questions(request, categories)

    if len(categories) == 0:
      abort(404)

    return jsonify({
      'success': True,
      'categories': current_category
    })

  #-------------------------------------------------------------------------------#
  # Questions.
  #-------------------------------------------------------------------------------#
  @app.route('/questions')
  def get_questions():
    questions = Question.query.order_by(Question.id).all()
    current_question = paginate_questions(request, questions)
    categories = Category.query.order_by(Category.id).all()
    current_category = paginate_questions(request, categories)


    if len(questions) == 0:
      abort(404)
    
    return jsonify({
      'success': True,
      'questions': current_question,
      'totalQuestions': len(questions),
      'categories': current_category,
    })

  #-------------------------------------------------------------------------------#
  # Delete question.
  #-------------------------------------------------------------------------------#
  @app.route('/question/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.filter(Question.id == question_id).one_or_none()

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
        selection = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search))).all()
        current_questions = paginate_questions(request, selection)
        current_category = Category.query.filter(Category.id == category_id).one()

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(Question.query.all()),
          'current_category': current_category.type
        })
      else:
        question = Question(
          question = new_question,
          answer = new_answer,
          category = new_category,
          difficulty = new_difficulty
        )
        question.insert()

        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        return jsonify({
          'success': True,
          'created': question.id,
          'books': current_questions,
          'total_books': len(Question.query.all())
        })
    except:
      abort(422)

  #-------------------------------------------------------------------------------#
  # Questions in category.
  #-------------------------------------------------------------------------------#
  @app.route('/categories/<int:category_id>/questions')
  def questions_in_category(category_id):
    questions = Question.query.filter(Question.category == category_id).all()
    current_question = paginate_questions(request, questions)
    current_category = Category.query.filter(Category.id == category_id).one()

    if len(current_question) == 0:
      abort(404)

    return jsonify({
      'questions': current_question,
      'total_questions': len(questions),
      'current_category': current_category.type
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route('/quizzes')
  def play_quiz():
    print()

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
      'message': "resource not found"
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