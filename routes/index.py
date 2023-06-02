from helpers import (
    sqlite3,
    render_template,
    Blueprint,
)

indexBlueprint = Blueprint("index", __name__)


@indexBlueprint.route("/")
def index():
    connection = sqlite3.connect("db/posts.db")
    cursor = connection.cursor()
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    cursor.execute('''CREATE TABLE IF NOT EXISTS blog_data (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          title TEXT,
                          paragraph TEXT,
                          show_AIBLOG BOOLEAN
                      )''')
    cursor.execute("SELECT * FROM blog_data")
    blog_data = cursor.fetchall()
    connection.close()
    return render_template("index.html", posts=posts, blog_data=blog_data)

    