from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Skill, Bookmark
from forms import SkillForm
import sqlalchemy
from sqlalchemy import func

skills_bp = Blueprint('skills', __name__)


@skills_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    skill_type = request.args.get('type', '')
    search = request.args.get('q', '')
    
    query = Skill.query.filter_by(is_approved=True)
    
    # Case-insensitive category filter
    if category:
        query = query.filter(sqlalchemy.func.lower(Skill.category) == category.lower())
    
    if skill_type:
        query = query.filter_by(skill_type=skill_type)
    
    if search:
        query = query.filter(
            (Skill.title.ilike(f'%{search}%')) | 
            (Skill.description.ilike(f'%{search}%'))
        )
    
    skills = query.order_by(Skill.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    
    # Get counts for tabs
    teaching_count = Skill.query.filter_by(skill_type='offered', is_approved=True).count()
    learning_count = Skill.query.filter_by(skill_type='wanted', is_approved=True).count()
    
    # Get category counts - dynamically calculated from database
    category_counts_raw = db.session.query(
        func.lower(Skill.category).label('category'), 
        func.count(Skill.id).label('count')
    ).filter(
        Skill.is_approved == True
    ).group_by(
        func.lower(Skill.category)
    ).all()
    
    # Convert to dictionary with proper case mapping
    category_counts = {}
    total_all = 0
    for cat, count in category_counts_raw:
        # Store with capitalized category name for display
        category_counts[cat.capitalize()] = count
        total_all += count
    
    # Add total count for "All" category
    category_counts['All'] = total_all
    
    return render_template('skills/skills.html', skills=skills, teaching_count=teaching_count, learning_count=learning_count, category_counts=category_counts)


@skills_bp.route('/<int:skill_id>')
def detail(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    
    if not skill.is_approved:
        flash('This skill is not available.', 'warning')
        return redirect(url_for('skills.index'))
    
    # Check if current user has bookmarked this skill
    is_bookmarked = False
    if current_user.is_authenticated:
        bookmark = Bookmark.query.filter_by(user_id=current_user.id, skill_id=skill_id).first()
        is_bookmarked = bookmark is not None
    
    # Get related skills (same category)
    related_skills = Skill.query.filter(
        Skill.id != skill_id,
        Skill.category == skill.category,
        Skill.is_approved == True
    ).limit(4).all()
    
    return render_template('skills/skill_detail.html', 
                           skill=skill, 
                           is_bookmarked=is_bookmarked,
                           related_skills=related_skills)


@skills_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = SkillForm()
    
    if form.validate_on_submit():
        skill = Skill(
            user_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            category=form.category.data,
            skill_type=form.skill_type.data
        )
        
        db.session.add(skill)
        db.session.commit()
        
        flash('Skill added successfully!', 'success')
        return redirect(url_for('main.profile'))
    
    return render_template('skills/add_skill.html', form=form)


@skills_bp.route('/edit/<int:skill_id>', methods=['GET', 'POST'])
@login_required
def edit(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    
    # Only owner can edit
    if skill.user_id != current_user.id and not current_user.is_admin:
        flash('You can only edit your own skills.', 'danger')
        return redirect(url_for('skills.index'))
    
    form = SkillForm()
    
    if form.validate_on_submit():
        skill.title = form.title.data
        skill.description = form.description.data
        skill.category = form.category.data
        skill.skill_type = form.skill_type.data
        
        db.session.commit()
        
        flash('Skill updated successfully!', 'success')
        return redirect(url_for('skills.detail', skill_id=skill.id))
    
    # Pre-populate form
    if request.method == 'GET':
        form.title.data = skill.title
        form.description.data = skill.description
        form.category.data = skill.category
        form.skill_type.data = skill.skill_type
    
    return render_template('skills/edit_skill.html', form=form, skill=skill)


@skills_bp.route('/delete/<int:skill_id>', methods=['POST'])
@login_required
def delete(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    
    # Only owner can delete
    if skill.user_id != current_user.id and not current_user.is_admin:
        flash('You can only delete your own skills.', 'danger')
        return redirect(url_for('skills.index'))
    
    # Delete bookmarks first
    Bookmark.query.filter_by(skill_id=skill_id).delete()
    
    db.session.delete(skill)
    db.session.commit()
    
    flash('Skill deleted successfully!', 'success')
    return redirect(url_for('main.profile'))


@skills_bp.route('/my-skills')
@login_required
def my_skills():
    offered = Skill.query.filter_by(user_id=current_user.id, skill_type='offered').all()
    wanted = Skill.query.filter_by(user_id=current_user.id, skill_type='wanted').all()
    
    return render_template('skills/my_skills.html', offered=offered, wanted=wanted)

