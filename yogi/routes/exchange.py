from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Skill, ExchangeRequest, User
from forms import ExchangeRequestForm
from datetime import datetime

exchange_bp = Blueprint('exchange', __name__)


@exchange_bp.route('/requests')
@login_required
def requests():
    sent = ExchangeRequest.query.filter_by(sender_id=current_user.id).order_by(ExchangeRequest.created_at.desc()).all()
    received = ExchangeRequest.query.filter_by(receiver_id=current_user.id).order_by(ExchangeRequest.created_at.desc()).all()
    
    return render_template('exchange/requests.html', sent=sent, received=received)


@exchange_bp.route('/request/<int:request_id>')
@login_required
def request_detail(request_id):
    exchange = ExchangeRequest.query.get_or_404(request_id)
    
    if exchange.sender_id != current_user.id and exchange.receiver_id != current_user.id:
        if not current_user.is_admin:
            flash('You can only view your own exchange requests.', 'danger')
            return redirect(url_for('exchange.requests'))
    
    return render_template('exchange/request_detail.html', exchange=exchange)


@exchange_bp.route('/create/<int:receiver_id>/<int:receiver_skill_id>', methods=['GET', 'POST'])
@login_required
def create(receiver_id, receiver_skill_id):
    receiver = User.query.get_or_404(receiver_id)
    receiver_skill = Skill.query.get_or_404(receiver_skill_id)
    
    my_skills = Skill.query.filter_by(user_id=current_user.id, skill_type='offered', is_approved=True).all()
    
    if not my_skills:
        flash('You need to add a skill you can offer first!', 'warning')
        return redirect(url_for('skills.add'))
    
    form = ExchangeRequestForm()
    sender_skill_id = request.args.get('sender_skill_id', type=int)
    
    if form.validate_on_submit():
        sender_skill_id = request.form.get('sender_skill_id', type=int)
        
        if not sender_skill_id:
            flash('Please select a skill to offer.', 'danger')
            return render_template('exchange/create.html', 
                                   form=form, 
                                   receiver=receiver,
                                   receiver_skill=receiver_skill,
                                   my_skills=my_skills)
        
        existing = ExchangeRequest.query.filter_by(
            sender_id=current_user.id,
            receiver_id=receiver_id,
            sender_skill_id=sender_skill_id,
            receiver_skill_id=receiver_skill_id,
            status='pending'
        ).first()
        
        if existing:
            flash('You already have a pending request for this exchange!', 'warning')
            return redirect(url_for('exchange.requests'))
        
        exchange = ExchangeRequest(
            sender_id=current_user.id,
            receiver_id=receiver_id,
            sender_skill_id=sender_skill_id,
            receiver_skill_id=receiver_skill_id,
            message=form.message.data
        )
        
        db.session.add(exchange)
        db.session.commit()
        
        flash('Exchange request sent!', 'success')
        return redirect(url_for('exchange.requests'))
    
    return render_template('exchange/create.html', 
                           form=form, 
                           receiver=receiver,
                           receiver_skill=receiver_skill,
                           my_skills=my_skills,
                           selected_skill=sender_skill_id)


@exchange_bp.route('/accept/<int:request_id>', methods=['POST'])
@login_required
def accept(request_id):
    exchange = ExchangeRequest.query.get_or_404(request_id)
    
    if exchange.receiver_id != current_user.id:
        flash('You can only accept requests sent to you.', 'danger')
        return redirect(url_for('exchange.requests'))
    
    if exchange.status != 'pending':
        flash('This request has already been processed.', 'warning')
        return redirect(url_for('exchange.requests'))
    
    exchange.status = 'accepted'
    exchange.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Exchange request accepted!', 'success')
    return redirect(url_for('exchange.request_detail', request_id=exchange.id))


@exchange_bp.route('/reject/<int:request_id>', methods=['POST'])
@login_required
def reject(request_id):
    exchange = ExchangeRequest.query.get_or_404(request_id)
    
    if exchange.receiver_id != current_user.id:
        flash('You can only reject requests sent to you.', 'danger')
        return redirect(url_for('exchange.requests'))
    
    if exchange.status != 'pending':
        flash('This request has already been processed.', 'warning')
        return redirect(url_for('exchange.requests'))
    
    exchange.status = 'rejected'
    exchange.updated_at = datetime.utcnow()
    db.session.commit()
    
    flash('Exchange request rejected.', 'info')
    return redirect(url_for('exchange.request_detail', request_id=exchange.id))


@exchange_bp.route('/complete/<int:request_id>', methods=['POST'])
@login_required
def complete(request_id):
    from models import Certificate
    import random
    import string
    
    exchange = ExchangeRequest.query.get_or_404(request_id)
    
    if exchange.sender_id != current_user.id and exchange.receiver_id != current_user.id:
        flash('You are not part of this exchange.', 'danger')
        return redirect(url_for('exchange.requests'))
    
    if exchange.status != 'accepted':
        flash('This request must be accepted first.', 'warning')
        return redirect(url_for('exchange.requests'))
    
    exchange.status = 'completed'
    exchange.updated_at = datetime.utcnow()
    
    # Auto-generate certificate for the learner (sender)
    # Check if certificate already exists
    existing_cert = Certificate.query.filter_by(exchange_id=exchange.id).first()
    if not existing_cert:
        # Determine learner and instructor
        learner = exchange.sender
        instructor = exchange.receiver
        skill = exchange.receiver_skill  # The skill being learned
        
        # Generate unique certificate number
        timestamp = datetime.now().strftime('%Y%m%d')
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        certificate_number = f"SES-{timestamp}-{random_suffix}"
        
        # Create certificate
        certificate = Certificate(
            user_id=learner.id,
            exchange_id=exchange.id,
            skill_name=skill.title,
            instructor_name=instructor.username,
            completion_date=exchange.updated_at,
            certificate_number=certificate_number
        )
        db.session.add(certificate)
        flash('Exchange marked as completed! A certificate has been generated.', 'success')
    else:
        flash('Exchange marked as completed!', 'success')
    
    db.session.commit()
    return redirect(url_for('exchange.request_detail', request_id=exchange.id))


@exchange_bp.route('/cancel/<int:request_id>', methods=['POST'])
@login_required
def cancel(request_id):
    exchange = ExchangeRequest.query.get_or_404(request_id)
    
    if exchange.sender_id != current_user.id:
        flash('You can only cancel your own requests.', 'danger')
        return redirect(url_for('exchange.requests'))
    
    if exchange.status != 'pending':
        flash('Only pending requests can be cancelled.', 'warning')
        return redirect(url_for('exchange.requests'))
    
    db.session.delete(exchange)
    db.session.commit()
    
    flash('Request cancelled.', 'info')
    return redirect(url_for('exchange.requests'))


@exchange_bp.route('/my-exchanges')
@login_required
def my_exchanges():
    exchanges = ExchangeRequest.query.filter(
        (ExchangeRequest.sender_id == current_user.id) | 
        (ExchangeRequest.receiver_id == current_user.id)
    ).order_by(ExchangeRequest.updated_at.desc()).all()
    
    active_count = ExchangeRequest.query.filter(
        ((ExchangeRequest.sender_id == current_user.id) | 
         (ExchangeRequest.receiver_id == current_user.id)),
        ExchangeRequest.status == 'accepted'
    ).count()
    
    return render_template('exchange/my_exchanges.html', 
                           exchanges=exchanges, 
                           active_count=active_count)

