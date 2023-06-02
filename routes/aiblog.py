from helpers import (
    session,
    sqlite3,
    request,
    flash,
    message,
    redirect,
    addPoints,
    currentDate,
    currentTime,
    render_template,
    Blueprint,
    createPostForm,
     ai_text,
    get_trending_title,
)

autoBlogBlueprint = Blueprint("autoBlog", __name__)

@autoBlogBlueprint.route("/auto_blog", methods=["GET", "POST"])
def createPost():
    if "userName" in session:
        form = createPostForm(request.form)
        if request.method == "POST":
            postTitle = request.form["postTitle"]
            postTags = request.form["postTags"]
            postContent = request.form["postContent"]
            if postContent == "":
                flash("Post content cannot be empty", "error")
                message("1", f'POST CONTENT NOT BE EMPTY USER: "{session["userName"]}"')
            else:
                # Generate blog paragraph
                title = get_trending_title()
                blog_para = ai_text(title)

                connection = sqlite3.connect("db/posts2.db")
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO posts(title, tags, content, author, views, date, time, lastEditDate, lastEditTime) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (postTitle, postTags, postContent, session["userName"], 0, currentDate(), currentTime(), currentDate(), currentTime())
                )
                connection.commit()
                message("2", f'POST: "{postTitle}" POSTED')
                addPoints(20, session["userName"])
                flash("You earned 20 points by posting", "success")
                return render_template("index.html", title=title, blog_para=blog_para)
        return render_template("createPost.html", form=form)
    else:
        message("1", "USER NOT LOGGED IN")
        flash("You need to log in to create a post", "error")
        return redirect("/login")
