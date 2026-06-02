from flask import Blueprint, render_template, redirect, url_for, flash, send_file, make_response
from flask_login import login_required, current_user
from models import db, Certificate, ExchangeRequest
from datetime import datetime
import io
import random
import string

# Try to import reportlab, if not available, PDF generation will be limited
try:
    from reportlab.lib.pagesizes import landscape, A4
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

certificates_bp = Blueprint('certificates', __name__)


def generate_certificate_number():
    """Generate a unique certificate number"""
    timestamp = datetime.now().strftime('%Y%m%d')
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"SES-{timestamp}-{random_suffix}"


def create_certificate_pdf(certificate):
    """Create a professional PDF certificate"""
    if not REPORTLAB_AVAILABLE:
        return None
    
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Certificate border
    c.setStrokeColor(colors.gold)
    c.setLineWidth(3)
    c.rect(30, 30, width - 60, height - 60)
    
    # Inner border
    c.setStrokeColor(colors.darkblue)
    c.setLineWidth(1)
    c.rect(40, 40, width - 80, height - 80)
    
    # Corner decorations
    corner_size = 30
    c.setStrokeColor(colors.gold)
    c.setLineWidth(2)
    
    # Top left
    c.line(30, height - 60, 30 + corner_size, height - 60)
    c.line(30, height - 60, 30, height - 60 - corner_size)
    
    # Top right
    c.line(width - 30, height - 60, width - 30 - corner_size, height - 60)
    c.line(width - 30, height - 60, width - 30, height - 60 - corner_size)
    
    # Bottom left
    c.line(30, 60, 30 + corner_size, 60)
    c.line(30, 60, 30, 60 + corner_size)
    
    # Bottom right
    c.line(width - 30, 60, width - 30 - corner_size, 60)
    c.line(width - 30, 60, width - 30, 60 + corner_size)
    
    # Title
    c.setFont("Helvetica-Bold", 36)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - 120, "CERTIFICATE")
    
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width / 2, height - 160, "of Completion")
    
    # Subtitle
    c.setFont("Helvetica", 16)
    c.setFillColor(colors.darkgray)
    c.drawCentredString(width / 2, height - 200, "This is to certify that")
    
    # Recipient name
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(colors.gold)
    c.drawCentredString(width / 2, height - 250, certificate.user.username)
    
    # Description
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.darkgray)
    c.drawCentredString(width / 2, height - 290, "has successfully completed the skill learning session in")
    
    # Skill name
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.darkblue)
    c.drawCentredString(width / 2, height - 330, certificate.skill_name)
    
    # Instructor
    c.setFont("Helvetica", 14)
    c.setFillColor(colors.darkgray)
    c.drawCentredString(width / 2, height - 370, f"Instructed by {certificate.instructor_name}")
    
    # Platform name
    c.setFont("Helvetica-Oblique", 12)
    c.setFillColor(colors.gray)
    c.drawCentredString(width / 2, height - 410, "Skill Exchange Marketplace")
    
    # Date
    completion_date_str = certificate.completion_date.strftime('%B %d, %Y')
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.darkgray)
    c.drawCentredString(width / 2, 120, f"Date of Completion: {completion_date_str}")
    
    # Certificate number
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.gray)
    c.drawCentredString(width / 2, 90, f"Certificate Number: {certificate.certificate_number}")
    
    # Signature lines
    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    
    # Instructor signature
    c.line(width / 2 - 150, 70, width / 2 - 50, 70)
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2 - 100, 55, "Instructor Signature")
    
    # Platform signature
    c.line(width / 2 + 50, 70, width / 2 + 150, 70)
    c.drawCentredString(width / 2 + 100, 55, "Platform Signature")
    
    c.save()
    buffer.seek(0)
    return buffer


@certificates_bp.route('/')
@login_required
def my_certificates():
    """View all certificates for the current user"""
    certificates = Certificate.query.filter_by(user_id=current_user.id).order_by(
        Certificate.completion_date.desc()
    ).all()
    return render_template('certificates/my_certificates.html', certificates=certificates)


@certificates_bp.route('/<int:certificate_id>')
@login_required
def view_certificate(certificate_id):
    """View a specific certificate"""
    certificate = Certificate.query.get_or_404(certificate_id)
    
    # Only the certificate owner can view it
    if certificate.user_id != current_user.id and not current_user.is_admin:
        flash('You can only view your own certificates.', 'danger')
        return redirect(url_for('certificates.my_certificates'))
    
    return render_template('certificates/certificate.html', certificate=certificate)


@certificates_bp.route('/<int:certificate_id>/download')
@login_required
def download_certificate(certificate_id):
    """Download certificate as PDF"""
    certificate = Certificate.query.get_or_404(certificate_id)
    
    # Only the certificate owner can download it
    if certificate.user_id != current_user.id and not current_user.is_admin:
        flash('You can only download your own certificates.', 'danger')
        return redirect(url_for('certificates.my_certificates'))
    
    if not REPORTLAB_AVAILABLE:
        flash('PDF generation is not available. Please install reportlab.', 'danger')
        return redirect(url_for('certificates.view_certificate', certificate_id=certificate_id))
    
    pdf_buffer = create_certificate_pdf(certificate)
    if pdf_buffer is None:
        flash('Failed to generate PDF.', 'danger')
        return redirect(url_for('certificates.view_certificate', certificate_id=certificate_id))
    
    filename = f"Certificate_{certificate.certificate_number}.pdf"
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype='application/pdf'
    )


@certificates_bp.route('/generate/<int:exchange_id>')
@login_required
def generate_certificate(exchange_id):
    """Generate a certificate for a completed exchange"""
    exchange = ExchangeRequest.query.get_or_404(exchange_id)
    
    # Check if user is part of this exchange
    if exchange.sender_id != current_user.id and exchange.receiver_id != current_user.id:
        flash('You are not part of this exchange.', 'danger')
        return redirect(url_for('exchange.requests'))
    
    if exchange.status != 'completed':
        flash('Only completed exchanges can generate certificates.', 'warning')
        return redirect(url_for('exchange.request_detail', request_id=exchange.id))
    
    # Check if certificate already exists
    existing_cert = Certificate.query.filter_by(exchange_id=exchange.id).first()
    if existing_cert:
        flash('Certificate already exists for this exchange.', 'info')
        return redirect(url_for('certificates.view_certificate', certificate_id=existing_cert.id))
    
    # Determine learner and instructor
    # The sender is learning from the receiver
    learner = exchange.sender
    instructor = exchange.receiver
    skill = exchange.receiver_skill  # The skill being learned
    
    # Get instructor's signature (if available)
    instructor_signature = instructor.signature_image if instructor.signature_image else None
    
    # Create certificate
    certificate = Certificate(
        user_id=learner.id,
        exchange_id=exchange.id,
        skill_name=skill.title,
        instructor_name=instructor.username,
        instructor_signature=instructor_signature,
        completion_date=exchange.updated_at,
        certificate_number=generate_certificate_number()
    )
    
    db.session.add(certificate)
    db.session.commit()
    
    flash('Certificate generated successfully!', 'success')
    return redirect(url_for('certificates.view_certificate', certificate_id=certificate.id))

