# -*- coding: utf-8 -*-

from flask import Blueprint, abort
from flask_login import current_user

from app.extensions import db
from app.dataBase.models import Users

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/block/<int:user_id>', methods=['DELETE'])
def block_user(user_id):
    if not current_user.is_admin:
        abort(403)
    user = Users.query.get_or_404(user_id)
    if user.is_admin:
        abort(400)
    db.session.delete(user)
    db.session.commit()
    return '', 204
