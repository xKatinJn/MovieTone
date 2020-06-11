import os
from app import app, db
from app.forms import RegistrationForm, LoginForm, EditProfileForm, CreatePostForm
from app.models import User, UserStatuses, Post, PostChecked

from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from werkzeug.exceptions import RequestEntityTooLarge


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.htm', title='Главная')


@app.route('/sign', methods=['GET', 'POST'])
def sign():
    if current_user.is_authenticated:
        return redirect('index')

    reg_form = RegistrationForm()
    log_form = LoginForm()

    if reg_form.reg_submit.data and reg_form.validate():
        email = reg_form.email.data
        password = reg_form.password.data

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        user_status = UserStatuses(status_id=1, user_id=User.query.filter_by(email=email).first().id)
        db.session.add(user_status)
        db.session.commit()
        login_user(user)
        user = User.query.filter_by(id=current_user.id).first()
        user.nickname = 'User_'+str(user.id)
        db.session.commit()
        return redirect(url_for('edit_profile'))
    if log_form.log_submit.data and log_form.validate():
        email = log_form.email.data
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(log_form.password.data):
            return render_template('registr-exit.htm', title='Авторизация', log_form=log_form, reg_form=reg_form,
                                   log_error=True)
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('registr-exit.htm', title='Авторизация', log_form=log_form, reg_form=reg_form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('sign')


@app.route('/about', methods=['GET'])
def about():
    return render_template('about.htm', title='О проекте')


@app.route('/vacancy', methods=['GET'])
def vacancy():
    return render_template('vacancy.htm', title='Вакансии')


@app.route('/new_weekend_posts', methods=['GET'])
def new_weekend_posts():
    return render_template('new_weekend_posts.htm', title='Новые публикации', glav_red=True)


@app.route('/user_profile', methods=['GET'])
def user_profile():
    user_id = request.args.get('user_id')
    if not user_id:
        user_id = current_user.id
    else:
        user_id = int(user_id)
    user = User.query.filter_by(id=user_id).first()
    Post.query.filter_by(has_photo_header=0).delete()
    posts = Post.query.filter_by(author=user_id).all()[::-1]
    posts_len = len(posts)
    checked_posts = len(PostChecked.query.filter_by(user_id=user_id).all())
    if user:
        return render_template('user_profile.htm', title=f'Профиль {user.nickname}',
                               user=user, posts=posts, posts_len=posts_len, checked_posts=checked_posts)
    else:
        return render_template('user_profile.htm', title=f'Профиль {user.nickname}')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    edit = {}
    for arg in request.args:
        edit[arg] = request.args.get(arg)
    if form.submit.data:
        user = current_user
        for attribute in request.args:
            if not form[attribute].data:
                return redirect('edit_profile')
            if attribute != 'birthday':
                if form[attribute].data.isspace():
                    return redirect('edit_profile')
            if attribute == 'email':
                if form.email.validate(form):
                    if User.query.filter_by(email=form.email.data).first():
                        if user.email != form.email.data:
                            return render_template('edit_profile.htm', title='Редактирование профиля', form=form,
                                                   edit=edit,
                                                   email_error=True)
                else:
                    return render_template('edit_profile.htm', title='Редактирование профиля', form=form, edit=edit)
            if attribute == 'password':
                if form.password_rep.validate(form):
                    user.set_password(form.password.data)
                else:
                    return render_template('edit_profile.htm', title='Редактирование профиля', form=form, edit=edit)
            if attribute == 'nickname':
                if User.query.filter_by(nickname=form[attribute].data).first():
                    return render_template('edit_profile.htm', title='Редактирование профиля', form=form, edit=edit,
                                           nickname_error=True)
            user.__setattr__(attribute, form[attribute].data)
        db.session.commit()
        return redirect('edit_profile')
    if form.back.data:
        return redirect('edit_profile')
    return render_template('edit_profile.htm', title='Редактирование профиля', form=form, edit=edit)


@app.route('/upload_profile_photo', methods=['POST'])
@login_required
def upload_profile_photo():
    if request.method == 'POST':
        try:
            f = request.files[f'user_profile_photo_{current_user.id}']
            f.filename = secure_filename(f.filename)
            file_ext = f.filename.split('.')[-1]
            if file_ext not in app.config['ALLOWED_EXTENSIONS']:
                return redirect(url_for('edit_profile', photo_error=1))
            f.filename = f'user_profile_photo_{current_user.id}.{file_ext}'
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
            current_user.has_photo = True
            current_user.photo_path = f'../static/img/{f.filename}'
            db.session.commit()
            return redirect('edit_profile')
        except RequestEntityTooLarge:
            return redirect(url_for('edit_profile', entity_error=1))


@app.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.submit_create.data:
        Post.query.filter_by(has_photo_header=0).delete()
        post = Post(title=form.title.data,
                    title_preview_text=form.preview_text.data,
                    text=form.text.data,
                    author=current_user.id,
                    type=int(form.type.data),
                    has_photo_preview=False,
                    has_photo_header=False)
        db.session.add(post)
        db.session.commit()
        return render_template('create_post.html', title='Создание поста', set_photo=True, post=post)
    return render_template('create_post.html', title='Создание поста', form=form)


@app.route('/upload_post_photo', methods=['POST'])
@login_required
def upload_post_photo():
    if request.method == 'POST':
        try:
            post = Post.query.filter_by(author=current_user.id).all()[-1]
            files = [request.files[f'post_preview_photo'], request.files[f'post_header_photo']]
            files_exts = [secure_filename(file.filename).split('.')[-1] for file in files]
            for file_ext in files_exts:
                if file_ext not in app.config['ALLOWED_EXTENSIONS']:
                    return redirect(url_for('create_post', ext_error=1))
            files[0].filename = f'post_preview_photo_{post.id}.{files_exts[0]}'
            files[1].filename = f'post_header_photo_{post.id}.{files_exts[1]}'
            for file in files:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                if 'preview' in file.filename.split('_'):
                    post.has_photo_preview = True
                    post.photo_preview_path = f'../static/img/{file.filename}'
                else:
                    post.has_photo_header = True
                    post.photo_header_path = f'../static/img/{file.filename}'
            Post.query.filter_by(has_photo_header=0).delete()
            db.session.commit()
            return redirect(url_for('user_profile'))
        except RequestEntityTooLarge:
            return redirect(url_for('create_post', entity_error=1))


@app.route('/post', methods=['GET', 'POST'])
def post():
    post_id = request.args.get('id')
    post_content = Post.query.filter_by(id=int(post_id)).first()
    if not post_content:
        return render_template('post.htm', error=True)
    user = User.query.filter_by(id=post_content.author).first()
    if current_user.is_authenticated:
        checked_posts = PostChecked.query.filter_by(user_id=current_user.id, post_id=int(post_id)).first()
        if not checked_posts:
            checked_post = PostChecked(user_id=current_user.id, post_id=int(post_id))
            db.session.add(checked_post)
            db.session.commit()
    return render_template('post.htm', user=user, post=post_content)


@app.route('/review', methods=['GET'])
def review():
    post_type = request.args.get('type')
    if not post_type:
        post_type = 1
    raw_posts = Post.query.filter_by(type=int(post_type)).all()
    posts = []
    for post_content in raw_posts:
        posts.append([post_content, User.query.filter_by(id=post_content.author).first()])
    posts = posts[::-1]
    return render_template('review.htm', title='Рецензии', posts=posts)