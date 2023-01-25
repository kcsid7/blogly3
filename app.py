"""Blogly application."""

import datetime

from flask import Flask, redirect, render_template, request, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostsTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)

# Use once to setup the database using the models
def run_db_createall():
    with app.app_context():
        db.create_all()


app.config['SECRET_KEY'] = "Secret Secret Secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)


@app.route("/")
def root_route():
    """ Homepage"""
    return redirect("/users")

# Users Route

@app.route("/users")
def users_route():
    """  List of Users"""
    users = User.query.order_by(User.last_name).all()

    return render_template("home.html", users = users)

@app.route("/users/new", methods=["GET"])
def create_user_form():
    """ Create a new User"""

    return render_template("new_user.html")


@app.route("/users/new", methods=["POST"])
def create_user_db():
    """ Create a new User"""
    new_user = User(
        first_name = request.form['first_name'],
        last_name = request.form['last_name'],
        image_url = request.form['image_url'] or '/static/img/default.jpg')

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user_details(user_id):

    user = User.query.get_or_404(user_id)

    user_posts = Post.query.filter(Post.user_id == user.id)

    return render_template("user_detail.html", user=user, posts=user_posts)


@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_user_details_form(user_id):
    
    user = User.query.get_or_404(user_id)

    return render_template("user_detail_edit_form.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user_details(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form['image_url'] or '/static/img/default.jpg'

    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


# Posts Route

@app.route("/users/<int:user_id>/posts/new")
def new_post_show_form(user_id):
    """ Displays the form to submit a post"""
    curr_user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template("new_post_form.html", user=curr_user, tags = tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def new_post_handle(user_id):
    """ Handles the new post """

    sel_tags = [int(tag) for tag in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(sel_tags)).all()

    new_post = Post(
        title = request.form["title"],
        content = request.form["content"],
        user_id = user_id,
        tags=tags
    )

    db.session.add(new_post)
    db.session.commit()

    flash("New Post Created")
    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def get_post(post_id):
    """ Shows more details about the selected post"""

    curr_post = Post.query.get_or_404(post_id)
    post_user = User.query.get_or_404(curr_post.user_id)

    return render_template("post.html", post = curr_post, user = post_user)


@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    post_edit = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template("edit_post.html", post = post_edit, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post_submit(post_id):

    curr_post = Post.query.get_or_404(post_id)
    curr_post.title = request.form["title"]
    curr_post.content = request.form["content"]
    curr_post.created_at = datetime.datetime.now()

    tagid = [int(tag) for tag in request.form.getlist("tags")]
    curr_post.tags = Tag.query.filter(Tag.id.in_(tagid)).all()

    db.session.add(curr_post)
    db.session.commit()

    return redirect(f"/posts/{curr_post.id}")



@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):

    curr_post = Post.query.get_or_404(post_id)

    db.session.delete(curr_post)
    db.session.commit()

    flash("Post Deleted")

    return redirect(f"/users/{curr_post.user_id}")




# Tags Route

@app.route("/tags")
def show_all_tags():
    """ Shows all tags """
    
    tags = Tag.query.all()
    return render_template("tags_all.html", tags=tags)



@app.route("/tags/new")
def add_new_tag_form():
    """ Add new Tag Form """

    all_posts = Post.query.all()
    return render_template("tags_new.html", posts = all_posts)




@app.route("/tags/new", methods=["POST"])
def add_new_tag():
    """ Add new Tag """
    postid = [ int(pst) for pst in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(postid)).all()
    nTag = Tag(
        name = request.form["name"],
        posts = posts
    )

    db.session.add(nTag)
    db.session.commit()

    flash("New Tag Added!")
    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def tag_details(tag_id):
    """ Shows more details about the tag """

    curr_tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_info.html", tag = curr_tag)


@app.route("/tags/<int:tag_id>/edit")
def tag_edit_form(tag_id):
    """ Tag Edit Form"""
    curr_tag = Tag.query.get_or_404(tag_id)
    all_posts = Post.query.all()
    return render_template("tags_edit.html", tags=curr_tag, all_posts=all_posts)



@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def tag_edit_form_post(tag_id):
    """" Handle Tag Edit Form """
    curr_tag = Tag.query.get_or_404(tag_id)
    curr_tag.name = request.form["name"]
    postid = [ int(pst) for pst in request.form.getlist("posts")]
    curr_tag.posts = Post.query.filter(Post.id.in_(postid)).all()

    db.session.add(curr_tag)
    db.session.commit()

    flash("Tag Edited")
    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete")
def delete_tag(tag_id):
    """" Delete Tag """ 
    curr_tag = Tag.query.get_or_404(tag_id)

    db.session.delete(curr_tag)
    db.session.commit()

    flash("Tag Deleted")
    return redirect("/tags")
