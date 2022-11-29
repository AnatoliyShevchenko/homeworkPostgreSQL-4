from flask import (Flask, jsonify, request)
import names
import random
from typing import Any

from service import Connection


app = Flask(__name__)
conn: Connection = Connection()
conn.create_tables()

@app.route('/', methods=['GET'])
def main_page():
    return jsonify({
        "name" : "Toliban",
        "lastname" : "Brick"
    })

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    users = conn.get_user()
    data: list[dict] = []
    for i in users:
        data.append({
            'id' : i[0],
            'name' : i[1],
            'login' : i[2],
            'password' : i[3],
            'wallet' : i[4]
        })

    return jsonify(data)

@app.route('/api/v1/users/<int:id>', methods=['GET'])
def get_user(id):
    users = conn.get_user()
    data: list[dict] = []
    for i in users:
        data.append({
            'id' : i[0],
            'name' : i[1],
            'login' : i[2],
            'password' : i[3]
        })

    return jsonify(data[id-1])


@app.route('/gen-users', methods=['GET'])
def second_page():
    TOTAL_USERS = 200
    email_patterns = [
        'gmail.com', 'mail.com', 'yandex.com', 'kahoo.com', 'bk.ru', 'inbox.com', 'yahoo.com', 'microsoft.com', 'ok.ru'
    ]
    if len(conn.get_user()) >= TOTAL_USERS:
        return jsonify({
            'result' : 'too many users'
        })
    for i in range(TOTAL_USERS):
        name = names.get_first_name()
        conn.create_user(
            name=name, 
            login='{0}@{1}'.format(name, random.choice(email_patterns)), 
            password='qwerty',
            wallet=random.randint(60, 1000))
    return jsonify({
        'result' : 'Users is create'
    })

@app.route('/users')
def users():
    users = conn.get_user()
    data: list[dict] = []
    for i in users:
        data.append({
            'id' : i[0],
            'name' : i[1],
            'login' : i[2],
            'password' : i[3]
        })

    return jsonify(data)

@app.route('/users/<int:id>', methods=['GET'])
def user(id):
    users = conn.get_user()
    data: list[dict] = []
    for i in users:
        data.append({
            'id' : i[0],
            'name' : i[1],
            'login' : i[2],
            'password' : i[3]
        })

    return jsonify(data[id-1])

@app.route('/user/create')
def user_create():
    return ("""
    <form action="/user/create/ok" method="post">
        <input type="text" name="name" id="name" placeholder="name">
        <input type="login" name="login" id="login" placeholder="login">
        <input type="password" name="password" id="password" placeholder="password">
        <input type="submit" value="submit">
    </form>
    """)

@app.route('/user/create/ok', methods=['POST'])
def add_new_user():
    name = request.form.get('name')
    login = request.form.get('login')
    password = request.form.get('password')
    conn.create_user(name, login, password)
    return (f"Пользователь: {name} {login} {password} добавлен")


@app.route('/create-post')
def create_post():
    return ("""
        <form action="/posts" method='post'>
            <input type="text" name="title" id="title" placeholder="title">
            <input type="text" name="content" id="content" placeholder="content">
            <input type="text" name="name" id="name" placeholder="name">
            <input type="submit" value="submit">
        </form>
    """)

@app.route('/posts', methods=['POST'])
def posts():
    articles = conn.get_artile()
    title = request.form.get('title')
    content = request.form.get('content')
    name = request.form.get('name')
    users = conn.get_user()
    data: list[dict] = []
    art: list[dict] = []
    for i in users:
        data.append({
            'id' : i[0],
            'name' : i[1],
        })
        if name == i[1]:
            articles = conn.create_article(title, content, i[0])
            print(conn.get_artile())
    articles = conn.get_artile()
    for i in articles:
        art.append({
            'title' : i[1],
            'content' : i[2],
            'name' : name
        })

    return jsonify(art)

@app.route('/add-friend', methods=['GET'])
def add_friend():
    try:
        user_id: int = int(request.args.get('userid'))
        friend_id: int = int(request.args.get('friendid'))
        conn.add_friend(user_id, friend_id)
        return jsonify({'detail' : f'User {user_id} add friend {friend_id}'})
    except:
        return jsonify({'error' : "user id or friend id is invalid"})

@app.route('/user/<id>')
def get_current_user(id):
    user = conn.get_current_user(id=int(id))
    us_friends = conn.get_all_friends(id=int(id))
    cash = 0
    for money in us_friends:
        cash += money[0][4]
    data: dict = {
        'id' : user[0][0],
        'name' : user[0][1],
        'login' : user[0][2],
        'cash_of_friends' : cash,
        'friends' : []
    }
    for item in us_friends:
        data['friends'].append({
            'id' : item[0][0],
            'name' : item[0][1],
            'login' : item[0][2],
            'wallet' : item[0][4],
        })
    return jsonify(data)

@app.route('/search', methods=['GET'])
def search():
    try:
        name = request.args.get('name')
        search = conn.searching(name=str(name))
        return jsonify({'detail' : f'User {search}'})
    except:
        return jsonify({'error' : "user id or friend id is invalid"})


if __name__ == '__main__':
    app.run(port=8090, debug=True)