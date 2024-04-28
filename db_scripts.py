import sqlite3
from random import *
db_name = 'quiz.sqlite'
conn = None
curor = None

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
    ''' удаляет все таблицы '''
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
    cursor.execute(''' PRAGMA FOREIGN_KEYS = on ''')
    do('''
        CREATE TABLE IF NOT EXISTS quiz
        (id INTEGER PRIMARY KEY, name VARCHAR)
        ''')
    do('''
        CREATE TABLE IF NOT EXISTS question
        (id INTEGER PRIMARY KEY, 
        question VARCHAR, 
        rigth_ans VARCHAR,
        wrong1 VARCHAR,
        wrong2 VARCHAR,
        wrong3 VARCHAR)
        ''')
    do('''
       CREATE TABLE IF NOT EXISTS quiz_content
       (id INTEGER PRIMARY KEY ,
       quiz_id INTEGER,
       question_id INTEGER,
       FOREIGN KEY (quiz_id) REFERENCES quiz(id),
       FOREIGN KEY(question_id) REFERENCES question(id)) 
        ''')
    close()
def add_quest():
    question = [
                ('Сколько месяцев в году имеют 28 дней?', 'Все', 'Один', 'Ни одного', 'Два'),
                ('Каким станет зеленый утес, если упадет в Красное море?', 'Мокрым', 'Красным', 'Не изменится', 'Фиолетовым'),
                ('Какой рукой лучше размешивать чай?', 'Ложкой', 'Правой', 'Левой', 'Любой'),
                ('Что не имеет длины, глубины, ширины, высоты, а можно измерить?', 'Время', 'Глупость', 'Море', 'Воздух'),
                ('Когда сетью можно вытянуть воду?', 'Когда вода замерзла', 'Когда нет рыбы', 'Когда уплыла золотая рыбка', 'Когда сеть порвалась'),
                ('Что больше слона и ничего не весит?', 'Тень слона', 'Воздушный шар', 'Парашют', 'Облако')
                ]
    open()
    cursor.executemany(''' 
    INSERT INTO question (question, rigth_ans, wrong1, wrong2, wrong3)
    VALUES (?,?,?,?,?)''', question)
    
    conn.commit()
    close()
def add_quiz():
    quizs = [
        ('Своя игра', ),
        ('Кто хочет стать миллионером?', ),
        ('Самый умный', )
    ]
    open()
    cursor.executemany(''' 
    INSERT INTO quiz(name)
    VALUES(?)''', quizs)
    conn.commit()
    close()
def add_links():
    open()
    cursor.execute('''PRAGMA FOREIGN_KEYS = on''')
    query = '''
    INSERT INTO quiz_content(quiz_id, question_id)
    VALUES(?,?)'''
    s = input('Добавлять связь(y/n)')
    while s != 'n':
        quiz_id = int(input('id викторины:'))
        question_id = int(input('id вопроса:'))
        cursor.execute(query, [quiz_id, question_id])
        conn.commit()
        s =  input('Добавлять связь(y/n)')
    close()
def show(table):
    query = 'SELECT * FROM ' + table
    open()
    cursor.execute(query)
    print(cursor.fetchall())
    close()

def show_tables():
    show('question')
    show('quiz')
    show('quiz_content')

def get_quest_after(quiz_id = 0, question_id = 1):  
    #question_id = 1, в запросе нужно WHERE ... == question.id
    #   ОШИБКА в запросе                                                         
    open()
    query = '''
    SELECT quiz_content.id, 
           question.question, 
           question.rigth_ans, 
           question.wrong1, 
           question.wrong2, 
           question.wrong3 
    FROM quiz_content, question
    WHERE quiz_content.question_id == question.id
    AND quiz_content.id > ?
    AND quiz_content.quiz_id == ?
    ORDER BY quiz_content.id
    '''
    cursor.execute(query, [question_id, quiz_id])
    result = cursor.fetchone()
    close()
    return result


def get_quizes():
    query = '''SELECT * FROM quiz ORDER BY id'''
    open()
    cursor.execute(query)
    result = cursor.fetchall()
    close()
    return result

def check_answers(quiz_id, ans_text):   
    #вместо question.answer нужно rigth_ans
    query = '''
    SELECT question.rigth_ans
    FROM quiz_content, question
    WHERE quiz_content.id = ?
    AND quiz_content.question_id = question.id'''
    open()
    cursor.execute(query, str(quiz_id))
    result = cursor.fetchone()
    close()
    if result is None:
        return False 
    else:
        if result[0] == ans_text:
            return True 
        else:
            return False
        
        
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
    add_quest()
    add_quiz()
    add_links()
    show_tables()

if __name__ == "__main__":
    main()
