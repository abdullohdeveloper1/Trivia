# Full Stack API Final Project
## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter) and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.
>Once you're ready, you can submit your project on the last page.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

# Backend
The [./backend](https://github.com/udacity/FSND/blob/master/projects/02_trivia_api/starter/backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:
1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*

#### Pre-requisites
* Developers using this project should already have Python3, pip and node installed on their local machines.
#### Install requirements
To install all reuirements, navigate to the `/backend` folder and run the folllowing command:
```bash
    pip install -r requirements.txt
```
requirements.txt is a file which includes all required modules and packages for API

Then to run application run the following commands:
```bash
    export FLASK_APP=flaskr
    export FLASK_ENV=development
    flask run
```
These commands put the application in development and directs our application to use `__init__.py` file in our flaskr folder. Wroking in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.
If you use Window, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The applcation by default runs on `http://127.0.0.1:5000/`.


# Frontend
From the `frontend` folder, run the following commands to start the client:
```
    npm install // install all requirements
    npm start
```
By default, the frontend will run on localhost:3000.

## Tests
In order to run tests, navigate to the `/backend` folder and run the following commands: 
```bash
psql -U postgres
dropdb trivia_test
createdb trivia_test
\q
psql trivia_test < trivia.psql
python test_flaskr.py
```


# API Reference

## Getting Started
* Base URL: At present this app can be run locally and it hosted by default. Default local url: ` http://127.0.0.1:5000 `
* Authentication: This version of API does not require :D

## Error Handling
Errors are returned as JSON objects in folloving format:
```json
    {
        "error": <error_code>,
        "message": <error_message>,
        "success": false
    }
```

### The API will return three types of errors: <br>
* 400: Bad request 
* 404: Resource not found 
* 405: Method now allowed 

## Endpoints

## `GET /categories`
    ```
        {
            "categories": 
                {
                    '1' : "Science",
                    '2' : "Art",
                    '3' : "Geography",
                    '4' : "History",
                    '5' : "Entertainment",
                    '6' : "Sports" 
                },
            "success": true,
        }
    ```
<br>

## `GET /questions`
* ### Example
    * Requests: ` https://127.0.0.1:/5000/questions ` - return an all questions
    * Response:
        ```
            {
                'question': [
                  {
                    "id" : 1,
                    "question" : "This is a question",
                    "answer" : "This is an answer",
                    "difficulty" : 5,
                    "category" : 2
                  },
                ],
                "totalQuestions" : 100,
                "categories" : {
                  "1" : "Science",
                  "2" : "Art",
                  "3" : "Geography",
                  "4" : "History",
                  "5" : "Entertainment",
                  "6" : "Sports"
                },
                "current_category" : "History"
            }
            
* ### ⚠️ Warning
    * If  in your request give a questions page which does not exists in database, API returns error with message "questions not found"
    * Example:
        * Request: ` http://127.0.0.1:5000/questions?page=12515 `
        * Response:
        ```
            {
                "message": "questions not found",
                "success": false
            }
        ```
## POST /questions
* ### General:
    * Search questions via question name. This endopint return all defined questions as searching resulsts
    * You should request to this endpoint with `POST` method. ⚠️ Request  should include JSON data which includes 'search' key and it value
* ### Example:
    * Request: ` POST/ 127.0.0.1:5000/questions `
        * Request body:
        ``` json
            {
                'searchTerm': 'which'
            }
        ```
        * Response:
        ``` json
            {
                'questions': [
                    {
                        'id': 1,
                        'question': 'This is a question',
                        'answer': 'This is an answer', 
                        'difficulty': 5,
                        'category': 5
                    },
                ],
                'totalQuestions': 100,
                'currentCategory': 'Entertainment'
            }
        ```
* ### ⚠️ Warning
    * If you send empty request or request which not includes important value, API returns "400" error with message "bad request"
    * Example:
        * Request: ` POST/ http://127.0.0.1:5000/questions `
            * Request body:
            ```json
                {
                    "uncorrect_key": "uncorrect_value"
                }
            ```
            or empty request body:
            ```json
                {}
            ```
            * Response:
            ```json
                {
                    "error": 400,
                    "message": "bad request",
                    "success": false
                }
            ```      
      
## POST /questions
* ### General:
    * Create a new questions
    * You should send request with `POST` method. Your request should include JSON data about new question


    * JSON data should include:
    ```
        "question" - new question
        "answer" - new answer
        "category" - new category
        "difficulty" - new difficulty
    ```
    * Then API reutrns data which includes:
    ```
        "questions" - all questions list,
        "created" - id of new question,
        "success" - True,
        "total_books" - number of all books
    ```

## DELETE /books/{book_id}
* ### General:
    * Delete a question:
    ```
        "id" - the id of deleted question
        "success" - True 
    ```
* ### Example:
    * Delete question
        * Request: ` DELETE http://127.0.0.1:5000/questions/2 `
        * Response:
        ```json
            {
                "success": true,
                "deleted" : 2
            }    
        ```
