# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, Blueprint, current_app, abort
from flask_login import current_user, login_required
from flask_socketio import emit

from app.extensions import socketio, db
from app.dataBase.models import Messages, Users


chat_bp = Blueprint('chat', __name__)

online_users = []


@socketio.on('new message')
def new_message(message):
    db.session.add(message)
    db.session.commit()
    emit('new message',
         {'message_html': 1234,
          'message_body': message,
          'gravatar': current_user.gravatar,
          'nickname': current_user.nickname,
          'user_id': current_user.id},
         broadcast=True)

@socketio.on('connect')
def connect():
    global online_users
    if current_user.is_authenticated and current_user.id not in online_users:
        online_users.append(current_user.id)

        msg = Messages.query.fity_by(mac_id=current_user.devicec.id).firt()
    emit('user count', {'count': len(online_users)}, broadcast=True)


@socketio.on('disconnect')
def disconnect():
    global online_users
    if current_user.is_authenticated and current_user.id in online_users:
        online_users.remove(current_user.id)
    emit('user count', {'count': len(online_users)}, broadcast=True)


@chat_bp.route('/')
def home():
    per_page = current_app.config['MESSAGE_PER_PAGE']
    messages = Messages.query.order_by(Messages.current_update_time.asc())[-per_page:]
    user_amount = Users.query.count()
    return render_template('index.html', messages=messages, user_amount=user_amount)


@chat_bp.route('/messages')
def get_messages():
    page = request.args.get('page', 1, type=int)
    pagination = Messages.query.order_by(Messages.current_update_time.desc()).paginate(
        page, per_page=current_app.config['MESSAGE_PER_PAGE'])
    messages = pagination.items
    return render_template('messages.html', messages=messages[::-1])


@chat_bp.route('/message/delete/<message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Messages.query.get_or_404(message_id)
    if current_user != message.author and not current_user.is_admin:
        abort(403)
    db.session.delete(message)
    db.session.commit()
    return '', 204
