from flask import render_template,redirect,url_for,request,abort,flash,Blueprint
from flask_login import current_user,login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts',__name__)


@posts.route("/post/new",methods=['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        #save the posts to our db
        post = Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been created!','success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',title='Create post',form=form,legend ='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    #post = Post.query.get(post_id)
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',title=post.title,post=post)

@posts.route("/post/<int:post_id>/update",methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    #ensure only the author of the post can update it
    if post.author != current_user:
        abort(403)
    form = PostForm()
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Your post has been updated!','success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method == 'GET':
        #pre fill the form with the post data in the database
        form.content.data = post.content
        form.title.data = post.title
    return render_template('create_post.html',title='Update post',form=form,legend ='Update Post')

@posts.route("/post/<int:post_id>/delete",methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    #ensure only the author of the post can delete it
    if post.author != current_user:
        abort(403)
    #delete post
    db.session.delete(post)
    db.session.commit()
    flash(f'Your post has been deleted!','success')
    return redirect(url_for('main.home'))