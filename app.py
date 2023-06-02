import socket
from helpers import (
    secrets,
    session,
    message,
    render_template,
    getProfilePicture,
    Flask,
    ai_text,
    get_trending_title,
)

import sqlite3
from flask import redirect, jsonify
from flask_apscheduler import APScheduler
from routes.post import postBlueprint
from routes.user import userBlueprint
from routes.index import indexBlueprint
from routes.login import loginBlueprint
from routes.signup import signUpBlueprint
from routes.logout import logoutBlueprint
from routes.search import searchBlueprint
from routes.searchBar import searchBarBlueprint
from routes.editPost import editPostBlueprint
from routes.dashboard import dashboardBlueprint
from routes.adminPanel import adminPanelBlueprint
from routes.deleteUser import deleteUserBlueprint
from routes.deletePost import deletePostBlueprint
from routes.createPost import createPostBlueprint
from routes.setUserRole import setUserRoleBlueprint
from routes.deleteComment import deleteCommentBlueprint
from routes.changeUserName import changeUserNameBlueprint
from routes.changePassword import changePasswordBlueprint
from routes.adminPanelUsers import adminPanelUsersBlueprint
from routes.adminPanelPosts import adminPanelPostsBlueprint
from routes.accountSettings import accountSettingsBlueprint
from routes.adminPanelComments import adminPanelCommentsBlueprint
from dbChecker import dbFolder, usersTable, postsTable, commentsTable 


dbFolder()
usersTable()
postsTable()
commentsTable()

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)
app.config["SESSION_PERMANENT"] = True

scheduler = APScheduler()

@app.context_processor
def utility_processor():
    getProfilePicture
    return dict(getProfilePicture=getProfilePicture)

@app.errorhandler(404)
def notFound(e):
    message("1", "404")
    return render_template("404.html"), 404


def auto_blog():
    title = get_trending_title()  # Fetch title
    blog_para = ai_text(title)  # Generate AI-generated paragraphs
    save_to_database(title, blog_para)  # Save to database
    return title, blog_para

def save_to_database(title, blog_para):
    # Establish a database connection
    conn = sqlite3.connect('db/posts.db')
    cursor = conn.cursor()
    defalt_show_aiblog = False
    cursor.execute('CREATE TABLE IF NOT EXISTS blog_data (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, paragraph TEXT, show_AIBLOG BOOLEAN)')
    cursor.execute('INSERT INTO blog_data (title, paragraph, show_AIBLOG) VALUES (?, ?, ?)', (title, blog_para, defalt_show_aiblog))

    conn.commit()

    cursor.execute('SELECT * FROM blog_data')
    data = cursor.fetchall()

    conn.close()
    return data


@app.route("/deletepost/<int:postID>")
def delete_post(postID):
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    cursor.execute("DELETE FROM blog_data WHERE id = ?", (postID,))
    connection.commit()
    connection.close()
    return jsonify({"success": True})

def addPoints():
    pass

@app.route("/publishpost/<int:postID>", methods=["GET"])
def publish_post(postID):
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    print(cursor, postID)
    cursor.execute("UPDATE blog_data SET show_AIBLOG = TRUE WHERE id = ?", (postID,))
    connection.commit()
    connection.close()
    # Assuming you have the published post content in the `published_post_content` variable
    return redirect(f'/user/{session["userName"].lower()}')


app.register_blueprint(postBlueprint)
app.register_blueprint(userBlueprint)
app.register_blueprint(indexBlueprint)
app.register_blueprint(loginBlueprint)
app.register_blueprint(signUpBlueprint)
app.register_blueprint(logoutBlueprint)
app.register_blueprint(searchBlueprint)
app.register_blueprint(editPostBlueprint)
app.register_blueprint(dashboardBlueprint)
app.register_blueprint(searchBarBlueprint)
app.register_blueprint(adminPanelBlueprint)
app.register_blueprint(deleteUserBlueprint)
app.register_blueprint(deletePostBlueprint)
app.register_blueprint(createPostBlueprint)
app.register_blueprint(setUserRoleBlueprint)
app.register_blueprint(deleteCommentBlueprint)
app.register_blueprint(changeUserNameBlueprint)
app.register_blueprint(changePasswordBlueprint)
app.register_blueprint(adminPanelUsersBlueprint)
app.register_blueprint(adminPanelPostsBlueprint)
app.register_blueprint(accountSettingsBlueprint)
app.register_blueprint(adminPanelCommentsBlueprint) 


match __name__:
    case "__main__":
        scheduler.add_job(id='shedule task', func=auto_blog, trigger="interval", minutes=60)
        scheduler.start() 
        app.run(debug=True, host=socket.gethostbyname(socket.gethostname())) 
