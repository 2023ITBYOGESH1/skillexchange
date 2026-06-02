from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from models import db, User, Skill, ExchangeRequest, Bookmark, Review
from forms import ProfileForm, SearchForm
from werkzeug.utils import secure_filename
import os

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    # Get featured skills (latest approved skills)
    skills = Skill.query.filter_by(is_approved=True).order_by(Skill.created_at.desc()).limit(8).all()
    
    # Get top users by rating
    top_users = User.query.filter_by(is_banned=False).order_by(User.rating.desc()).limit(6).all()
    
    # Get statistics
    stats = {
        'total_users': User.query.filter_by(is_banned=False).count(),
        'total_skills': Skill.query.filter_by(is_approved=True).count(),
        'active_exchanges': ExchangeRequest.query.filter_by(status='completed').count()
    }
    
    return render_template('index.html', skills=skills, top_users=top_users, stats=stats)


@main_bp.route('/profile')
@login_required
def profile():
    # Get user's skills
    skills_offered = Skill.query.filter_by(user_id=current_user.id, skill_type='offered').all()
    skills_wanted = Skill.query.filter_by(user_id=current_user.id, skill_type='wanted').all()
    
    # Get user's reviews
    reviews = Review.query.filter_by(reviewed_id=current_user.id).order_by(Review.created_at.desc()).all()
    
    # Get exchange statistics
    pending_requests = ExchangeRequest.query.filter_by(receiver_id=current_user.id, status='pending').count()
    completed_exchanges = ExchangeRequest.query.filter(
        (ExchangeRequest.sender_id == current_user.id) | (ExchangeRequest.receiver_id == current_user.id),
        ExchangeRequest.status == 'completed'
    ).count()
    
    return render_template('profile/profile.html',
                           skills_offered=skills_offered,
                           skills_wanted=skills_wanted,
                           reviews=reviews,
                           pending_requests=pending_requests,
                           completed_exchanges=completed_exchanges)


@main_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm()
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        
        # Handle profile picture upload
        if form.profile_picture.data:
            filename = secure_filename(form.profile_picture.data.filename)
            # Delete old profile picture if exists and not default
            if current_user.profile_picture != 'default.png':
                old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.profile_picture)
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            # Save new profile picture
            form.profile_picture.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            current_user.profile_picture = filename
        
        # Handle signature upload
        if form.signature.data:
            filename = secure_filename(form.signature.data.filename)
            # Delete old signature if exists
            if current_user.signature_image:
                old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], current_user.signature_image)
                if os.path.exists(old_path):
                    os.remove(old_path)
            
            # Save new signature with unique name to avoid conflicts
            import uuid
            ext = os.path.splitext(filename)[1].lower()
            filename = f"signature_{current_user.id}_{uuid.uuid4().hex[:8]}{ext}"
            form.signature.data.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            current_user.signature_image = filename
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    # Pre-populate form with current data
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.location.data = current_user.location
    
    return render_template('profile/edit_profile.html', form=form)


@main_bp.route('/user/<int:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.is_banned:
        flash('This user has been banned.', 'danger')
        return redirect(url_for('main.index'))
    
    skills_offered = Skill.query.filter_by(user_id=user.id, skill_type='offered', is_approved=True).all()
    skills_wanted = Skill.query.filter_by(user_id=user.id, skill_type='wanted', is_approved=True).all()
    reviews = Review.query.filter_by(reviewed_id=user.id).order_by(Review.created_at.desc()).all()
    
    # Check if current user has bookmarked any of this user's skills
    bookmarks = []
    if current_user.is_authenticated:
        bookmarks = [b.skill_id for b in current_user.bookmarks.all()]
    
    return render_template('profile/user_detail.html',
                           user=user,
                           skills_offered=skills_offered,
                           skills_wanted=skills_wanted,
                           reviews=reviews,
                           bookmarks=bookmarks)


@main_bp.route('/search')
def search():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    skill_type = request.args.get('type', '')
    
    # Build query
    skills_query = Skill.query.filter_by(is_approved=True)
    
    if query:
        skills_query = skills_query.filter(
            (Skill.title.ilike(f'%{query}%')) | 
            (Skill.description.ilike(f'%{query}%'))
        )
    
    if category:
        skills_query = skills_query.filter_by(category=category)
    
    if skill_type:
        skills_query = skills_query.filter_by(skill_type=skill_type)
    
    skills = skills_query.order_by(Skill.created_at.desc()).paginate(
        page=1, per_page=12, error_out=False
    )
    
    # Also search users
    users = []
    if query:
        users = User.query.filter(
            User.is_banned == False,
            (User.username.ilike(f'%{query}%')) | 
            (User.bio.ilike(f'%{query}%'))
        ).limit(10).all()
    
    form = SearchForm()
    
    return render_template('search.html', 
                           skills=skills, 
                           users=users,
                           query=query,
                           category=category,
                           skill_type=skill_type,
                           form=form)


@main_bp.route('/bookmarks')
@login_required
def bookmarks():
    bookmarks_list = Bookmark.query.filter_by(user_id=current_user.id).order_by(Bookmark.created_at.desc()).all()
    return render_template('profile/bookmarks.html', bookmarks=bookmarks_list)


@main_bp.route('/bookmarks/add/<int:skill_id>', methods=['POST'])
@login_required
def add_bookmark(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    
    # Check if already bookmarked
    existing = Bookmark.query.filter_by(user_id=current_user.id, skill_id=skill_id).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        flash('Bookmark removed.', 'info')
    else:
        bookmark = Bookmark(user_id=current_user.id, skill_id=skill_id)
        db.session.add(bookmark)
        db.session.commit()
        flash('Skill bookmarked!', 'success')
    
    return redirect(request.referrer or url_for('main.index'))


@main_bp.route('/about')
def about():
    return render_template('about.html')


@main_bp.route('/contact')
def contact():
    return render_template('contact.html')


@main_bp.route('/reviews/<int:user_id>')
def user_reviews(user_id):
    user = User.query.get_or_404(user_id)
    reviews = Review.query.filter_by(reviewed_id=user_id).order_by(Review.created_at.desc()).all()
    from forms import ReviewForm
    form = ReviewForm()
    return render_template('profile/reviews.html', user=user, reviews=reviews, form=form)


@main_bp.route('/reviews/add/<int:user_id>', methods=['GET', 'POST'])
@login_required
def add_review(user_id):
    user = User.query.get_or_404(user_id)
    
    # Can't review yourself
    if user.id == current_user.id:
        flash('You cannot review yourself.', 'danger')
        return redirect(url_for('main.user_profile', user_id=user.id))
    
    from forms import ReviewForm
    form = ReviewForm()
    
    if form.validate_on_submit():
        # Check if already reviewed
        existing = Review.query.filter_by(reviewer_id=current_user.id, reviewed_id=user_id).first()
        if existing:
            flash('You have already reviewed this user.', 'warning')
            return redirect(url_for('main.user_reviews', user_id=user_id))
        
        review = Review(
            reviewer_id=current_user.id,
            reviewed_id=user_id,
            rating=form.rating.data,
            comment=form.comment.data
        )
        
        db.session.add(review)
        
        # Update user's rating
        user.update_rating()
        
        db.session.commit()
        flash('Review added successfully!', 'success')
        return redirect(url_for('main.user_reviews', user_id=user_id))
    
    reviews = Review.query.filter_by(reviewed_id=user_id).order_by(Review.created_at.desc()).all()
    return render_template('profile/reviews.html', user=user, reviews=reviews, form=form)


@main_bp.route('/report/<int:user_id>', methods=['GET', 'POST'])
@login_required
def report_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Can't report yourself
    if user.id == current_user.id:
        flash('You cannot report yourself.', 'danger')
        return redirect(url_for('main.user_profile', user_id=user.id))
    
    from forms import ReportForm
    form = ReportForm()
    
    if form.validate_on_submit():
        report = Report(
            reporter_id=current_user.id,
            reported_id=user_id,
            reason=form.reason.data
        )
        
        db.session.add(report)
        db.session.commit()
        
        flash('Report submitted. Thank you for helping keep our community safe!', 'success')
        return redirect(url_for('main.user_profile', user_id=user_id))
    
    return render_template('profile/report.html', user=user, form=form)


@main_bp.route('/signature-demo')
def signature_demo():
    """Demo page for signature template"""
    return render_template('signature_demo.html')

