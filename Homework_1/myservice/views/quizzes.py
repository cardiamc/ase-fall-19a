from flakon import JsonBlueprint
import json
from flask import request, jsonify, abort
from myservice.classes.quiz import Quiz, Question, Answer, \
    NonExistingAnswerError, LostQuizError, CompletedQuizError

quizzes = JsonBlueprint('quizzes', __name__)

_LOADED_QUIZZES = {}  # list of available quizzes
_QUIZNUMBER = 0  # index of the last created quizzes
_NUMBER_ANSWERS = []  # list containing the nbs of answers given for a quiz


'''
    /quizzes endpoint.
    It allows either to create a new quiz or retrieve all loaded quizzes.
'''
@quizzes.route("/quizzes", methods=['GET', 'POST'])
def all_quizzes():
    if 'POST' == request.method:
        # Create new quiz
        content = json.loads(str(request.data, 'utf8'))
        result = create_quiz(jsonify(content))
        _NUMBER_ANSWERS.append(int(0))  # inizialise the number of answer given
    elif 'GET' == request.method:
        # Retrieve all loaded quizzes
        result = get_all_quizzes(request)
    return result


'''
    /quizzes/loaded endpoint.
    Returns the number of quizzes loaded
'''
@quizzes.route("/quizzes/loaded", methods=['GET'])
def loaded_quizzes():  # returns the number of quizzes loaded in the system
    global _LOADED_QUIZZES
    n_quizzes = 0
    for e in _LOADED_QUIZZES.values():
        n_quizzes += 1
    return jsonify({'loaded_quizzes': n_quizzes})


'''
    /quiz/<id> endpoint.
    A GET request returns the quiz with id <id>
    A DELETE request deletes the quiz with id <id> and returns the number
    of questions of the quiz and the number of answered questions
'''
@quizzes.route("/quiz/<id>", methods=['GET', 'DELETE'])
def single_quiz(id):
    global _LOADED_QUIZZES, _NUMBER_ANSWERS
    result = ""

    # check if the quiz is an existing one
    exists_quiz(id)

    if 'GET' == request.method:
        # retrieve a quiz <id>
        result = _LOADED_QUIZZES[id].serialize()

    elif 'DELETE' == request.method:
        # delete a quiz and get back number of answered questions
        # and total number of questions

        n_questions = len(_LOADED_QUIZZES[id].serialize()['questions'])
        del _LOADED_QUIZZES[id]

        result = jsonify({
                'answered_questions': _NUMBER_ANSWERS[int(id)],
                'total_questions': n_questions
            }
        )

    return result


'''
    /quiz/<id>/question endpoint
    It returns the next question in the quiz with id <id>
    In case of either completed quiz or a wrong answer,
    it returns a determined message.
'''
@quizzes.route("/quiz/<id>/question", methods=['GET'])
def play_quiz(id):
    global _LOADED_QUIZZES
    result = ""

    # check if the quiz is an existing one
    exists_quiz(id)

    if 'GET' == request.method:
        # retrieve next question in a quiz, handle exceptions
        try:
            result = _LOADED_QUIZZES[id].getQuestion()
        except CompletedQuizError:
            result = jsonify({'msg': "completed quiz"})
        except LostQuizError:
            result = ({'msg': "you lost!"})

    return result


'''
    /quiz/<id>/question/<answer> endpoint
    It is used to answer to a question belonging to the quiz
    with id <id>. It returns wether or not you answer correctly
'''
@quizzes.route("/quiz/<id>/question/<answer>", methods=['PUT'])
def answer_question(id, answer):
    global _LOADED_QUIZZES
    result = ""

    # check if the quiz is an existing one
    exists_quiz(id)

    if 'PUT' == request.method:
        quiz = _LOADED_QUIZZES[id]
        try:  # check if quiz is lost or completed and act consequently

            # increment the number of answers given
            _NUMBER_ANSWERS[int(id)] += 1
            quiz.isOpen()

            try:  # Check answers and handle exceptions
                result = quiz.checkAnswer(answer)

            except NonExistingAnswerError:
                # The answer doesn't exist, it shouldn't be counted
                result = "non-existing answer!"
                _NUMBER_ANSWERS[int(id)] -= 1
            except CompletedQuizError:
                result = "you won 1 million clams!"
            except LostQuizError:
                result = "you lost!"

        except CompletedQuizError:
            result = "completed quiz"
        except LostQuizError:
            result = "you lost!"

        return jsonify({'msg': result})


############################################
# USEFUL FUNCTIONS BELOW (use them, don't change them)
############################################

def create_quiz(request):
    global _LOADED_QUIZZES, _QUIZNUMBER

    json_data = request.get_json()
    qs = json_data['questions']
    questions = []
    for q in qs:
        question = q['question']
        answers = []
        for a in q['answers']:
            answers.append(Answer(a['answer'], a['correct']))
        question = Question(question, answers)
        questions.append(question)

    _LOADED_QUIZZES[str(_QUIZNUMBER)] = Quiz(_QUIZNUMBER, questions)
    _QUIZNUMBER += 1

    return jsonify({'quiznumber': _QUIZNUMBER - 1})


def get_all_quizzes(request):
    global _LOADED_QUIZZES

    return jsonify(
        loadedquizzes=[e.serialize() for e in _LOADED_QUIZZES.values()]
    )


def exists_quiz(id):
    if int(id) > _QUIZNUMBER:
        # error 404: Not Found, i.e. wrong URL, resource does not exist
        abort(404)
    elif not(id in _LOADED_QUIZZES):
        # error 410: Gone, i.e. it existed but it's not there anymore
        abort(410)
