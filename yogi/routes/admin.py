from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User, Skill, ExchangeRequest, Report, Review
from forms import AdminUserEditForm, PasswordResetForm, ReportForm
from werkzeug.security import generate_password_hash
from functools import wraps

admin_bp = Blueprint('admin', __name__)


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {
        'total_users': User.query.count(),
        'total_skills': Skill.query.count(),
        'active_exchanges': ExchangeRequest.query.filter_by(status='accepted').count(),
        'pending_requests': ExchangeRequest.query.filter_by(status='pending').count(),
        'banned_users': User.query.filter_by(is_banned=True).count(),
        'pending_reports': Report.query.filter_by(status='pending').count()
    }
    
    top_users = User.query.filter_by(is_banned=False).order_by(User.rating.desc()).limit(10).all()
    recent_skills = Skill.query.order_by(Skill.created_at.desc()).limit(5).all()
    recent_exchanges = ExchangeRequest.query.order_by(ExchangeRequest.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                           stats=stats, 
                           top_users=top_users,
                           recent_skills=recent_skills,
                           recent_exchanges=recent_exchanges)


@admin_bp.route('/users')
@admin_required
def users():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'newest')
    
    query = User.query
    
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) | 
            (User.email.ilike(f'%{search}%'))
        )
    
    if sort == 'newest':
        query = query.order_by(User.created_at.desc())
    elif sort == 'oldest':
        query = query.order_by(User.created_at.asc())
    elif sort == 'rating':
        query = query.order_by(User.rating.desc())
    elif sort == 'banned':
        query = query.filter_by(is_banned=True)
    
    users_list = query.paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/users.html', users=users_list, search=search, sort=sort)


@admin_bp.route('/users/<int:user_id>')
@admin_required
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    
    skills = Skill.query.filter_by(user_id=user_id).all()
    exchanges = ExchangeRequest.query.filter(
        (ExchangeRequest.sender_id == user_id) | 
        (ExchangeRequest.receiver_id == user_id)
    ).order_by(ExchangeRequest.created_at.desc()).limit(10).all()
    reviews = Review.query.filter_by(reviewed_id=user_id).order_by(Review.created_at.desc()).limit(10).all()
    reports = Report.query.filter_by(reported_id=user_id).order_by(Report.created_at.desc()).limit(10).all()
    
    return render_template('admin/user_detail.html', 
                           user=user, 
                           skills=skills,
                           exchanges=exchanges,
                           reviews=reviews,
                           reports=reports)


@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = AdminUserEditForm()
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.bio = form.bio.data
        user.location = form.location.data
        user.is_admin = form.is_admin.data == '1'
        user.is_banned = form.is_banned.data == '1'
        
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.user_detail', user_id=user.id))
    
    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.bio.data = user.bio
        form.location.data = user.location
        form.is_admin.data = '1' if user.is_admin else '0'
        form.is_banned.data = '1' if user.is_banned else '0'
    
    return render_template('admin/edit_user.html', form=form, user=user)


@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.is_admin and not current_user.is_admin:
        flash('You cannot delete another admin.', 'danger')
        return redirect(url_for('admin.users'))
    
    if user.id == current_user.id:
        flash('You cannot delete yourself.', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/ban/<int:user_id>')
@admin_required
def ban_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.is_admin and not current_user.is_admin:
        flash('You cannot ban an admin.', 'danger')
        return redirect(url_for('admin.users'))
    
    user.is_banned = True
    db.session.commit()
    
    flash(f'User {user.username} has been banned.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user.id))


@admin_bp.route('/users/unban/<int:user_id>')
@admin_required
def unban_user(user_id):
    user = User.query.get_or_404(user_id)
    
    user.is_banned = False
    db.session.commit()
    
    flash(f'User {user.username} has been unbanned.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user.id))


@admin_bp.route('/users/promote/<int:user_id>')
@admin_required
def promote_user(user_id):
    user = User.query.get_or_404(user_id)
    
    user.is_admin = True
    db.session.commit()
    
    flash(f'User {user.username} has been promoted to admin.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user.id))


@admin_bp.route('/users/demote/<int:user_id>')
@admin_required
def demote_user(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        flash('You cannot demote yourself.', 'danger')
        return redirect(url_for('admin.user_detail', user_id=user.id))
    
    user.is_admin = False
    db.session.commit()
    
    flash(f'User {user.username} has been demoted to normal user.', 'success')
    return redirect(url_for('admin.user_detail', user_id=user.id))


@admin_bp.route('/users/reset-password/<int:user_id>', methods=['GET', 'POST'])
@admin_required
def reset_password(user_id):
    user = User.query.get_or_404(user_id)
    form = PasswordResetForm()
    
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        
        flash('Password has been reset successfully!', 'success')
        return redirect(url_for('admin.user_detail', user_id=user.id))
    
    return render_template('admin/reset_password.html', form=form, user=user)


@admin_bp.route('/skills')
@admin_required
def skills():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'all')
    category = request.args.get('category', '')
    
    query = Skill.query
    
    if status == 'pending':
        query = query.filter_by(is_approved=False)
    elif status == 'approved':
        query = query.filter_by(is_approved=True)
    
    if category:
        query = query.filter_by(category=category)
    
    skills_list = query.order_by(Skill.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/skills_moderation.html', 
                           skills=skills_list, 
                           status=status,
                           category=category)


@admin_bp.route('/skills/approve/<int:skill_id>')
@admin_required
def approve_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    
    skill.is_approved = True
    db.session.commit()
    
    flash('Skill has been approved!', 'success')
    return redirect(url_for('admin.skills'))


@admin_bp.route('/skills/reject/<int:skill_id>')
@admin_required
def reject_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    
    skill.is_approved = False
    db.session.commit()
    
    flash('Skill has been rejected.', 'success')
    return redirect(url_for('admin.skills'))


@admin_bp.route('/skills/delete/<int:skill_id>', methods=['POST'])
@admin_required
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    
    db.session.delete(skill)
    db.session.commit()
    
    flash('Skill has been deleted.', 'success')
    return redirect(url_for('admin.skills'))


@admin_bp.route('/reports')
@admin_required
def reports():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', 'pending')
    
    query = Report.query
    
    if status != 'all':
        query = query.filter_by(status=status)
    
    reports_list = query.order_by(Report.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/reports.html', 
                           reports=reports_list, 
                           status=status)


@admin_bp.route('/reports/<int:report_id>')
@admin_required
def report_detail(report_id):
    report = Report.query.get_or_404(report_id)
    return render_template('admin/report_detail.html', report=report)


@admin_bp.route('/reports/<int:report_id>/resolve', methods=['POST'])
@admin_required
def resolve_report(report_id):
    report = Report.query.get_or_404(report_id)
    
    report.status = 'resolved'
    db.session.commit()
    
    flash('Report has been resolved.', 'success')
    return redirect(url_for('admin.reports'))


@admin_bp.route('/reports/<int:report_id>/dismiss', methods=['POST'])
@admin_required
def dismiss_report(report_id):
    report = Report.query.get_or_404(report_id)
    
    report.status = 'reviewed'
    db.session.commit()
    
    flash('Report has been dismissed.', 'info')
    return redirect(url_for('admin.reports'))


@admin_bp.route('/reports/<int:report_id>/ban-user', methods=['POST'])
@admin_required
def ban_reported_user(report_id):
    report = Report.query.get_or_404(report_id)
    reported_user = report.reported
    
    reported_user.is_banned = True
    report.status = 'resolved'
    db.session.commit()
    
    flash(f'User {reported_user.username} has been banned.', 'success')
    return redirect(url_for('admin.reports'))


@admin_bp.route('/activity')
@admin_required
def activity():
    recent_users = User.query.order_by(User.created_at.desc()).limit(20).all()
    recent_skills = Skill.query.order_by(Skill.created_at.desc()).limit(20).all()
    recent_exchanges = ExchangeRequest.query.order_by(ExchangeRequest.created_at.desc()).limit(20).all()
    
    return render_template('admin/activity.html',
                           recent_users=recent_users,
                           recent_skills=recent_skills,
                           recent_exchanges=recent_exchanges)

