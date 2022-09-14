import sqlite3
from random import randint
 
db_name = 'quiz.sqlite'
conn = None
cursor = None
 
def open():
    global conn, cursor
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
 
def close():
    cursor.close()
    conn.close()
 
def do(query):
    cursor.execute(query)
    conn.commit()
 
def clear_db():
    ''' убивает все таблицы '''
    open()
    query = '''DROP TABLE IF EXISTS quiz_content'''
    do(query)
    query = '''DROP TABLE IF EXISTS question'''
    do(query)
    query = '''DROP TABLE IF EXISTS quiz'''
    do(query)
    close()
 
def create():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    
    do('''CREATE TABLE IF NOT EXISTS quiz (
            id INTEGER PRIMARY KEY, 
            name VARCHAR)''' 
    )
    do('''CREATE TABLE IF NOT EXISTS question (
                id INTEGER PRIMARY KEY, 
                question VARCHAR, 
                answer VARCHAR, 
                wrong1 VARCHAR, 
                wrong2 VARCHAR, 
                wrong3 VARCHAR)'''
    )
    do('''CREATE TABLE IF NOT EXISTS quiz_content (
                id INTEGER PRIMARY KEY,
                quiz_id INTEGER,
                question_id INTEGER,
                FOREIGN KEY (quiz_id) REFERENCES quiz (id),
                FOREIGN KEY (question_id) REFERENCES question (id) )'''
    )
    close()

def check_answer(q_id, ans_text):
    query = '''
            SELECT question.answer 
            FROM quiz_content, question 
            WHERE quiz_content.id = ? 
            AND quiz_content.question_id = question.id
        '''
    open()
    cursor.execute(query, str(q_id))
    result = cursor.fetchone()
    close()    
    # print(result)
    if result is None:
        return False # не нашли
    else:
        if result[0] == ans_text:
            # print(ans_text)
            return True # ответ совпал
        else:
            return False # нашли, но ответ не совпал

def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    for line in cursor.fetchall():
        print(line)
    close()
 
def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')
 
def add_questions():
    questions = [
        ('В какой стране были проведены первые Олимпийские игры?', 'Греция', 'Италия', 'Япония', 'Франция'),
        ('Сколько игроков в бейсбольной команде?', '9', '8 ', '11', '10'),
        ('Какое стихийное бедствие измеряется по шкале Рихтера?', 'Землетрясения', 'Наводнения', 'Торнадо', 'Ураган'),
        ('Какая планета находится ближе всего к Солнцу?', 'Меркурий', 'Марс', 'Земля', 'Венера'),
        ('Из какого вещества состоят ногти?', 'Кератин', 'Меланин', 'Эпидермис', 'Серотонин'),
        ('Кто была первой женщиной, получившей Нобелевскую премию в 1903 году?', 'Мари Кюри', 'Джейн Аддамс', 'Розалинд Франклин', 'Перл Бак'),
        ('“K” - это химический символ какого элемента?', 'Калий', 'Хром', 'Титан', 'Водород'),
        ('Что является столицей Австралии?', 'Канберра', 'Аделаида', 'Сидней', 'Мельбурн'),
        ('Какая страна является самой подвержеyнной землетрясениям страной в мире?', 'Япония', 'Корея', 'Малайзия', 'Тайвань')
        
    ]
    open()
    cursor.executemany('''INSERT INTO question (question, answer, wrong1, wrong2, wrong3) VALUES (?,?,?,?,?)''', questions)
    conn.commit()
    close()
 
def add_quiz():
    quizes = [
        ('Викторина 1', ),
        ('Викторина 2', ),
        ('Викторина-непоймикакая', )
    ]
    open()
    cursor.executemany('''INSERT INTO quiz (name) VALUES (?)''', quizes)
    conn.commit()
    close()
 
def add_links():
    open()
    cursor.execute('''PRAGMA foreign_keys=on''')
    query = "INSERT INTO quiz_content (quiz_id, question_id) VALUES (?,?)"
    answer = input("Добавить связь (y / n)?")
    while answer != 'n':
        quiz_id = int(input("id викторины: "))
        question_id = int(input("id вопроса: "))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        answer = input("Добавить связь (y / n)?")
    close()
 
 
def get_question_after(last_id=0, vict_id=1):
    open()
    query = '''
    SELECT quiz_content.id, question.question, question.answer, question.wrong1, question.wrong2, question.wrong3
    FROM question, quiz_content 
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ? AND quiz_content.quiz_id == ? 
    ORDER BY quiz_content.id '''
    cursor.execute(query, [last_id, vict_id] )
 
    result = cursor.fetchone()
    close()
    return result 
 
def get_quises():
    query = 'SELECT * FROM quiz ORDER BY id'
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result
 
def get_quiz_count():
    query = 'SELECT MAX(quiz_id) FROM quiz_content'
    open()
    cursor.execute(query)
    result = cursor.fetchone()
    close()
    return result

 
def get_random_quiz_id():
    query = 'SELECT quiz_id FROM quiz_content'
    open()
    cursor.execute(query)
    ids = cursor.fetchall()
    rand_num = randint(0, len(ids) - 1)
    rand_id = ids[rand_num][0]
    close()
    return rand_id
    
 
def main():
    clear_db()
    create()
    add_questions()
    add_quiz()
    show_tables()
    add_links()
    show_tables()
    pass
    
if __name__ == "__main__":
    main()