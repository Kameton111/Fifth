from random import shuffle
from turtle import right
from flask import Flask, session, request, redirect, url_for, render_template
from db_scripts import get_question_after, get_quises, check_answer
import os


def start_quis(quiz_id):
    session['quiz'] = quiz_id
    session['last_question'] = 0
    session['answers'] = 0
    session['total'] = 0
 
def end_quiz():
    session.clear()

def quiz_form():
    html_beg = '''<html><body><h2>Выберите викторину:</h2><form method="post" action="index"><select name="quiz">'''
    frm_submit = '''<p><input type="submit" value="Выбрать"> </p>'''
 
    html_end = '''</select>''' + frm_submit + '''</form></body></html>'''
    options = ''' '''
    q_list = get_quises()
    for id, name in q_list:
        option_line = ('''<option value="''' +
                        str(id) + '''">''' +
                        str(name) + '''</option>
                      ''')
        options = options + option_line
    return html_beg + options + html_end
       
def index():
    if request.method == 'GET':
        start_quis(-1)
        return quiz_form()
    else:
        quest_id = request.form.get('quiz')
        start_quis(quest_id)
        return redirect(url_for('test'))


def question_form(question):
    answers_list = [
        question[2], question[3], question[4], question[5]
    ]
    shuffle(answers_list)
    return render_template('test.html', question=question[1], quest_id=question[0], answers_list=answers_list   )

def save_answers():
    '''получает данные из формы, проверяет, верен ли ответ, записывает итоги в сессию'''
    answer = request.form.get('ans_text')
    quest_id = request.form.get('q_id')
    # этот вопрос уже задан:
    session['last_question'] = quest_id
    # увеличиваем счетчик вопросов:
    session['total'] += 1
    # проверить, совпадает ли ответ с верным для этого id
    if check_answer(quest_id, answer):
        session['answers'] += 1

def test():
    if not ('quiz' in session) or int(session['quiz']) < 0:
        return redirect(url_for('index'))
    else:
        if request.method == 'POST':
            save_answers()
        next_question = get_question_after(session['last_question'], session['quiz'])
        if next_question is None or len(next_question) == 0:
            return redirect(url_for('result'))
        else:
            return question_form(next_question)
 
def result():
    html = render_template('result.html', right=session['answers'], total=session['total'])
    end_quiz()
    return html

folder = os.getcwd()

app = Flask(__name__, template_folder=folder, static_folder=folder)  
app.add_url_rule('/', 'index', index)
app.add_url_rule('/index', 'index', index, methods=['post', 'get'])
app.add_url_rule('/test', 'test', test, methods=['post', 'get'])
app.add_url_rule('/result', 'result', result)

app.config['SECRET_KEY'] = 'ThisIsSecretSecretSecretLife'
 
if __name__ == "__main__":
    app.run()
