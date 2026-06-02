from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, Message, User
from forms import MessageForm
from sqlalchemy import or_

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/')
@login_required
def index():
    # Get all conversations
    messages = Message.query.filter(
        or_(
            Message.sender_id == current_user.id,
            Message.receiver_id == current_user.id
        )
    ).order_by(Message.created_at.desc()).all()
    
    # Group by user
    conversations = {}
    for msg in messages:
        other_id = msg.receiver_id if msg.sender_id == current_user.id else msg.sender_id
        if other_id not in conversations:
            other_user = User.query.get(other_id)
            last_msg = Message.query.filter(
                or_(
                    (Message.sender_id == current_user.id) & (Message.receiver_id == other_id),
                    (Message.sender_id == other_id) & (Message.receiver_id == current_user.id)
                )
            ).order_by(Message.created_at.desc()).first()
            
            unread_count = Message.query.filter(
                Message.sender_id == other_id,
                Message.receiver_id == current_user.id,
                Message.is_read == False
            ).count()
            
            conversations[other_id] = {
                'user': other_user,
                'last_message': last_msg,
                'unread_count': unread_count
            }
    
    return render_template('chat/chat.html', conversations=conversations)


@chat_bp.route('/<int:user_id>', methods=['GET', 'POST'])
@login_required
def conversation(user_id):
    other_user = User.query.get_or_404(user_id)
    
    if other_user.is_banned:
        flash('This user has been banned.', 'danger')
        return redirect(url_for('chat.index'))
    
    form = MessageForm()
    
    if form.validate_on_submit():
        message = Message(
            sender_id=current_user.id,
            receiver_id=user_id,
            content=form.content.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Message sent!', 'success')
        return redirect(url_for('chat.conversation', user_id=user_id))
    
    # Get messages between users
    messages = Message.query.filter(
        or_(
            (Message.sender_id == current_user.id) & (Message.receiver_id == user_id),
            (Message.sender_id == user_id) & (Message.receiver_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).all()
    
    # Mark messages as read
    Message.query.filter(
        Message.sender_id == user_id,
        Message.receiver_id == current_user.id,
        Message.is_read == False
    ).update({'is_read': True})
    db.session.commit()
    
    return render_template('chat/conversation.html', 
                           other_user=other_user, 
                           messages=messages,
                           form=form)


@chat_bp.route('/api/messages/<int:user_id>')
@login_required
def get_messages(user_id):
    messages = Message.query.filter(
        or_(
            (Message.sender_id == current_user.id) & (Message.receiver_id == user_id),
            (Message.sender_id == user_id) & (Message.receiver_id == current_user.id)
        )
    ).order_by(Message.created_at.asc()).all()
    
    return jsonify([{
        'id': m.id,
        'sender_id': m.sender_id,
        'receiver_id': m.receiver_id,
        'content': m.content,
        'created_at': m.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'is_read': m.is_read
    } for m in messages])


@chat_bp.route('/api/send', methods=['POST'])
@login_required
def send_message():
    data = request.get_json()
    receiver_id = data.get('receiver_id')
    content = data.get('content')
    
    if not receiver_id or not content:
        return jsonify({'error': 'Missing data'}), 400
    
    message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content
    )
    db.session.add(message)
    db.session.commit()
    
    return jsonify({
        'id': message.id,
        'sender_id': message.sender_id,
        'receiver_id': message.receiver_id,
        'content': message.content,
        'created_at': message.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })


@chat_bp.route('/api/unread')
@login_required
def unread_count():
    count = Message.query.filter(
        Message.receiver_id == current_user.id,
        Message.is_read == False
    ).count()
    
    return jsonify({'unread': count})

