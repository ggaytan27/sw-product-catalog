from flask import Blueprint, request, flash, redirect, url_for, g, render_template
from werkzeug.utils import secure_filename
from .auth import login_required
from .models import Post
from blogr import db

bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/posts')
@login_required
def posts():
    posts = Post.query.all()
    return render_template('admin/posts.html', posts = posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        url = request.form.get('title')
        url = url.replace('', '-')
        title = request.form.get('title')
        info = request.form.get('info')
        cant = request.form.get('cant', type=int)
        precio = request.form.get('precio', type=float)
                
        post = Post(g.user.id, url, title, info, cant, precio)
        
        if request.files['photo']:
            photo = request.files['photo']
            photo.save(f'blogr/static/media/{secure_filename(photo.filename)}')
            post.photo = f'media/{secure_filename(photo.filename)}'
        
        if request.files['photo2']:
            photo2 = request.files['photo2']
            photo2.save(f'blogr/static/media/{secure_filename(photo2.filename)}')
            post.photo2 = f'media/{secure_filename(photo2.filename)}'

        if request.files['photo3']:
            photo3 = request.files['photo3']
            photo3.save(f'blogr/static/media/{secure_filename(photo3.filename)}')
            post.photo3 = f'media/{secure_filename(photo3.filename)}'


        error = None

        #Comparando url de post con los existentes
        post_url = Post.query.filter_by(url = url).first()
        if post_url == None:
            db.session.add(post)
            db.session.commit()
            flash(f'El blog {post.title} se registro correctamente')
            return redirect(url_for('post.posts'))
        else:
            error = f'El URL {url} ya esta registrado'
        flash(error)
    return render_template('admin/create.html')

@bp.route('/update/<int:id>', methods = ('GET','POST'))
@login_required
def update(id):
    post = Post.query.get_or_404(id)
    if request.method == 'POST':

        post.title = request.form.get('title')
        post.info = request.form.get('info')
        post.cant = request.form.get('cant', type=int)
        post.precio = request.form.get('precio', type=float)

        if request.files['photo']:
            photo = request.files['photo']
            photo.save(f'blogr/static/media/{secure_filename(photo.filename)}')
            post.photo = f'media/{secure_filename(photo.filename)}'
        
        if request.files['photo2']:
            photo2 = request.files['photo2']
            photo2.save(f'blogr/static/media/{secure_filename(photo2.filename)}')
            post.photo2 = f'media/{secure_filename(photo2.filename)}'

        if request.files['photo3']:
            photo3 = request.files['photo3']
            photo3.save(f'blogr/static/media/{secure_filename(photo3.filename)}')
            post.photo3 = f'media/{secure_filename(photo3.filename)}'


        db.session.commit()
        flash(f"El articulo {post.title} se actualizo correctamente")
        return redirect(url_for('post.posts'))
    
    return render_template('admin/update.html', post = post)


@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    flash(F'El blog {post.title} se elimino correctamente')

    return redirect(url_for('post.posts'))


@bp.route('/view/<string:url>')
def view_post(url):
    post = Post.query.filter_by(url=url).first_or_404()
    # Trae otros posts para el carrusel (por ejemplo los últimos 5)
    posts = Post.query.order_by(Post.id.desc()).limit(5).all()
    return render_template('blog/blog_post.html', post=post, posts=posts)
