import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
import pprint
from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

    '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
    # register a function to run after each request,
    # and function must take one parameter.
    # and return a new response object
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,POST,PATCH,PUT,DELETE')
        # response.headers.add('Access-Control-Allow-Credentials', 'true')
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        return response

    '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
    @app.route("/categories_questions", methods=['GET'])
    @cross_origin()
    def get_categories():
        try:
            categories = [cat.format() for cat in Category.query.all()]
            questions = [question.format()
                         for question in Question.query.all()]
            print(categories, questions)
        except Exception as e:
            flash(f"Error... when getting categories.questions data")
            print(e)
        return jsonify({
            "categories": categories,
            "questions": questions
        })

    '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    @app.route("/questions", methods=["GET"])
    @cross_origin()
    def get_questions():
        search = request.args.get("page", None)
        questions = [question.format() for question in Question.query.all()]

        if search:
            searchPage = int(search)
            if searchPage == 1:
                pageQuestions = questions[0:10]
            else:
                index = (searchPage - 1) * 10
                pageQuestions = questions[index:searchPage * 10]
            total_questions = len(pageQuestions)
            categoriesIDs = list(set([question["category"]
                                      for question in pageQuestions]))
            print(categoriesIDs)
            typesNames = []
            for id in categoriesIDs:
                typeName = Category.query.get(id)
                typesNames.append({id: typeName.type})

            print(typesNames)
            return jsonify({
                "questions": pageQuestions,
                "total_questions": total_questions,
                "categories": typesNames,
                "current_category": None
            })
        else:
            categoriesIDs = list(set([question["category"]
                                      for question in questions]))
            typesNames = []
            for id in categoriesIDs:
                typeName = Category.query.get(id)
                typesNames.append({id: typeName.type})

            return jsonify({
                "questions": questions,
                "total_questions": len(questions),
                "categories": typesNames,
                "current_category": None
            })
    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
    

    '''
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    @app.route("/questions/add", methods = ["POST"])
    @cross_origin(
      origin='http://localhost:3000', 
      methods = 'POST', 
      allow_headers = '*', 
      supports_credentials = True)
    
    def create_new_question():
      post_data = request.get_json()
      #pprint.pprint(post_data)
      categoryId = [data.id for data in Category.query.filter_by(type = post_data["category"]).all()][0]
      print(categoryId)
      error = False
      try:
        newRow = Question(
          question = post_data["question"],
          answer = post_data["answer"],
          difficulty = post_data["difficulty"],
          category = categoryId
        )
        Question.insert(newRow)
        # db.session.add(newRow)
        # db.session.commit()
      except Exception as e:
        error = True
        db.session.rollback()
        print(e)
      finally:
        if error:
          flash("data failed to insert")
        
      return jsonify({
        "success": error,
        "data": post_data
      })

  

    '''
  @DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    @app.route("/questions/search", methods=["POST"])
    @cross_origin(origin='http://localhost:3000', methods = 'POST', allow_headers = '*', supports_credentials = True)
    def search_questions():
        try:
            searchTerm = "%{}%".format(request.args.get("searchterm"))
        except Exception as e:
            flash(f"Error...cannot target the search term...")
            print(e)
            return "error"
        if searchTerm:
            filteredSearch = Question.query.filter(
                Question.question.like(searchTerm)
            ).all()
            questions = [question.format() for question in filteredSearch]
            current_category = [question["category"] for question in questions]
        return jsonify({
          "questions": questions,
          "total_questions": len(questions),
          "current_category": list(set(current_category))
        })
        
    '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route("/categories/<int:id>/questions")
    @cross_origin()
    def get_questions_by_category(id):
        questions = [question.format()
                     for question in Question.query.filter_by(category=id).all()]
        current_category = list(
            set([question["category"] for question in questions]))
        return jsonify({
            "questions": questions,
            "total_questions": len(questions),
            "current_category": current_category
        })
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

    '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

    return app
