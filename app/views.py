from flask import Flask, render_template, flash, json, jsonify, request, jsonify, redirect, url_for
from app import app, db, models
from .forms import UserForm, LoginForm, PostForm
from sqlalchemy import func
from app.models import User, Posts, Friends
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import json


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    user = User.query.filter(User.username == query).first()
    if user:
        return redirect(url_for('profile', user_username=user.username))
    else:
        return redirect(url_for('error'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = generate_password_hash(form.password.data)
        new_username = User.query.filter_by(username=username).first()
        if new_username is not None:
            flash('ERROR - Username already exist', 'login')
            return render_template('signup.html', form=form, title='Interlink')
        new_user = User(email=email, username=username, hashed_password=password)
        db.session.add(new_user)
        db.session.commit()
    return render_template('signup.html', title="Interlink", form=form)


@app.route('/user')
def user():
    user_data = models.User.query.all()
    return render_template('dump.html', user_data=user_data, title='User')


@app.route('/feed', methods=['GET', 'POST'])
@login_required
def feed():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        new_post = Posts(title=title, content=content, user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('feed'))
    post_data = models.Posts.query.all()
    return render_template('feed.html', post_data=post_data, title='Main', form=form)


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.hashed_password, password):  # hash will be use here
                login_user(user, remember=False)
                return redirect(url_for('feed'))
            else:
                flash('Wrong password', 'login')
        else:
            flash('You did not sign up', 'login')
    return render_template('login.html', title="Interlink", form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/profile/<string:user_username>/', methods=['GET', 'POST'])
@login_required
def profile(user_username):
    from app.models import User
    # Query all rows from the "income" table
    user = User.query.filter_by(username=user_username).first_or_404()
    is_user = (current_user.id == user.id)
    post_data = Posts.query.filter_by(user_id=user.id).all()

    friends = Friends.query.filter(
        ((Friends.user_id == current_user.id) & (Friends.friend_id == user.id))).first()
    friend_status = friends.status if friends else None
    return render_template('profile.html', post_data=post_data, user=user, title='Main', current_user=current_user,
                           is_user=is_user, friend_status=friend_status)


@app.route('/friends', methods=['GET'])
def display_friends():
    friends_list = Friends.query.all()
    all_users = User.query.all()
    return render_template('dump.html', friends_list=friends_list, all_users=all_users)


@app.route('/error')
def error():
    return render_template('error.html')


@app.route('/friend_request', methods=['POST'])
@login_required
def friend_request():
    try:
        if request.method == 'POST':
            data = request.get_json()
            username = data.get('username')
            if username:
                user = User.query.filter_by(username=username).first_or_404()
                user.clicked = True

                friend_request1 = Friends(user_id=current_user.id, friend_id=user.id)
                friend_request2 = Friends(user_id=user.id, friend_id=current_user.id)

                db.session.add(friend_request1)
                db.session.add(friend_request2)
                db.session.commit()

                return jsonify({'status': 'success', 'friendshipStatus': 'pending'})
    except Exception as e:
        db.session.rollback()
        print(f"Database error: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500


@app.route('/accept_friend/<int:id>', methods=['GET', 'POST'])
@login_required
def accept_friend(id):
    print(id)
    print(current_user.id)
    print(current_user.username)
    friend_request1 = Friends.query.filter_by(user_id=id, friend_id=current_user.id, status='pending').first()
    friend_request2 = Friends.query.filter_by(user_id=current_user.id, friend_id=id, status='pending').first()

    if friend_request1 or friend_request2:
        friend_request1.status = 'accepted'
        friend_request2.status = 'accepted'
        db.session.commit()
    return redirect(url_for('notifications'))


@app.route('/decline_friend/<int:id>', methods=['GET', 'POST'])
@login_required
def decline_friend(id):
    print(id)
    print(current_user.id)
    print(current_user.username)
    friend_request1 = Friends.query.filter_by(user_id=id, friend_id=current_user.id, status='pending').first()
    friend_request2 = Friends.query.filter_by(user_id=current_user.id, friend_id=id, status='pending').first()

    if friend_request1 and friend_request2:
        db.session.delete(friend_request1)
        db.session.delete(friend_request2)
        db.session.commit()

    return redirect(url_for('notifications'))


@app.route('/notifications')
@login_required
def notifications():
    friends = (
        db.session.query(Friends, User.username)
        .join(User, Friends.friend_id == User.id)
        .filter(Friends.user_id == current_user.id, Friends.status == 'pending')
        .all()
    )
    return render_template('notifications.html', friends_data=friends)


@app.route('/delete_post/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Posts.query.get(id)

    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('profile', user_username=current_user.username))
