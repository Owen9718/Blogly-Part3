"""Blogly application."""

from crypt import methods
from flask import Flask,redirect,render_template,request,flash
from models import PostTag, Tag, db, connect_db,User,Post,Tag


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

connect_db(app)
db.create_all()

@app.route('/')
def root():
    """Show recent list of posts, most-recent first."""

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)


@app.route('/users')
def list_users():
    users = User.query.order_by(User.last_name,User.first_name).all()
    return render_template('users.html',users = users)


@app.route('/users/new')
def create_user():

    return render_template('home.html',tags=tags)


@app.route('/users/new', methods= ['POST'])
def add_user():
    image_url = request.form['url'] if request.form['url']!= "" else None
    new_user = User(first_name = request.form['first'],last_name = request.form['last'],image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')


@app.route(f'/users/<int:user_id>')
def user_info(user_id):
    user = User.query.get_or_404(user_id)
    print('THIS IS IMAGE', user.image_url)
    return render_template('user_info.html', user= user)


@app.route(f'/users/<int:user_id>/edit')
def edit_temp(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html',user = user)


@app.route(f'/users/<int:user_id>/edit', methods =["POST"])
def save_user_edit(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    user.image_url = request.form['image']

    db.session.add(user)
    db.session.commit()
    return redirect('/users')


@app.route(f'/users/<int:user_id>/delete', methods =["POST"])
def delete(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route(f'/users/<int:user_id>/posts/new')
def post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('post_form.html',user=user,tags=tags)

@app.route(f'/users/<int:user_id>/posts/new', methods = ['POST'])
def post_create(user_id):
    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)
    post = Post(title = title,content = content, user_id = user.id)
    form_tags = request.form.getlist('selected')
    post.tags = Tag.query.filter(Tag.name.in_(form_tags)).all()
    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' added.")
    return redirect(f'/users/{user_id}')


@app.route(f'/posts/<int:post_id>')
def post_details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post_info.html', post = post)

@app.route(f'/posts/<int:post_id>/edit')
def show_edit(post_id):
    tag = Tag.query.all()
    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html',post=post,tags=tag)

@app.route(f'/posts/<int:post_id>/edit', methods=['POST'])
def save_post_edit(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    form_tags = request.form.getlist('selected')
    post.tags = Tag.query.filter(Tag.name.in_(form_tags)).all()
    

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' saved.")
    return redirect(f'/posts/{post.id}')


@app.route(f'/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted.")
    return redirect(f'/users/{post.user_id}')



@app.route('/tags')
def list_tags():
    tags = Tag.query.all()
    return render_template("tags.html",tags=tags)

@app.route('/tags/<int:tag_id>')
def tag_info(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tag_posts.html",tag=tag)



@app.route('/tags/new')
def add_tag():

    return render_template("make_tag.html")



@app.route('/tags/new',methods=["POST"])
def return_tag_list():
    name = request.form['tag_name']
    tag = Tag(name = name)
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')




@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html',tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def save_edit(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    name = request.form['tag_name']
    tag.name = name
    db.session.add(tag)
    db.session.commit()
    return redirect(f'/tags/{tag.id}')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')