"""
Seed script to add sample skills to the Skill Exchange Marketplace database.
Run this script to populate the database with sample skills for each category.
"""

import os
import sys

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from models import Skill, User


def seed_skills():
    """Add sample skills to the database."""
    
    app = create_app('development')
    
    with app.app_context():
        # Get admin user (or first available user)
        admin = User.query.filter_by(email='admin@skillswap.com').first()
        
        if not admin:
            # Create admin if not exists
            admin = User(
                username='admin',
                email='admin@skillswap.com',
                is_admin=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
        
        # Define skills for each category
        skills_data = {
            "Technology": [
                "Python Programming",
                "Web Development (HTML/CSS/JS)",
                "Mobile App Development",
                "Data Analysis with Excel",
                "Basic Computer Maintenance",
                "Video Editing",
                "Graphic Design Basics",
                "Social Media Management",
                "Cybersecurity Fundamentals",
                "Cloud Computing Basics"
            ],
            "Languages": [
                "English Conversation",
                "Spanish for Beginners",
                "French Language Basics",
                "Mandarin Chinese",
                "Japanese Writing System",
                "German Grammar",
                "Italian Conversation",
                "Korean Speaking",
                "Portuguese Basics",
                "Hindi Writing"
            ],
            "Music": [
                "Guitar Playing",
                "Piano Basics",
                "Violin Lessons",
                "Singing for Beginners",
                "Music Theory",
                "Drum Playing",
                "Songwriting",
                "Music Production",
                "DJ Mixing",
                "Harmonica"
            ],
            "Art & Design": [
                "Watercolor Painting",
                "Digital Illustration",
                "Photography Basics",
                "Fashion Sketching",
                "Interior Design Principles",
                "Calligraphy",
                "Cartoon Drawing",
                "Sculpture Basics",
                "Textile Design",
                "UI/UX Design"
            ],
            "Business": [
                "Public Speaking",
                "Time Management",
                "Financial Planning",
                "Marketing Basics",
                "Project Management",
                "Resume Writing",
                "Negotiation Skills",
                "Customer Service",
                "Leadership Basics",
                "Entrepreneurship 101"
            ],
            "Health": [
                "Yoga Practice",
                "Meditation Techniques",
                "Fitness Training",
                "Nutrition Basics",
                "Stress Management",
                "First Aid",
                "Home Remedies",
                "Sleep Hygiene",
                "Posture Correction",
                "Mental Health Awareness"
            ],
            "Cooking": [
                "Sourdough Baking",
                "Italian Cuisine",
                "Healthy Meal Prep",
                "Baking Desserts",
                "Asian Cooking",
                "BBQ Techniques",
                "Vegetarian Cooking",
                "Knife Skills",
                "Food Photography",
                "Coffee Brewing"
            ],
            "Crafts": [
                "Knitting",
                "Pottery",
                "Candle Making",
                "Jewelry Making",
                "Woodworking",
                "Origami",
                "Sewing",
                "Soap Making",
                "Paper Crafts",
                "Leatherwork"
            ],
            "Sports": [
                "Swimming",
                "Basketball",
                "Soccer",
                "Tennis",
                "Cycling",
                "Hiking",
                "Rock Climbing",
                "Boxing",
                "Golf Basics",
                "Yoga for Athletes"
            ],
            "Academic": [
                "Essay Writing",
                "Mathematics Tutoring",
                "Science Concepts",
                "History Basics",
                "Study Skills",
                "Research Methods",
                "Critical Thinking",
                "SAT/ACT Prep",
                "Language Learning Methods",
                "Online Learning Tools"
            ],
            "Other": [
                "Personal Finance",
                "Event Planning",
                "Travel Planning",
                "Pet Care",
                "Home Organization",
                "Car Maintenance",
                "Gardening",
                "Puzzle Solving",
                "Magic Tricks",
                "Wine Tasting"
            ]
        }
        
        # Add skills to database
        skills_added = 0
        for category, skills in skills_data.items():
            for skill_title in skills:
                # Check if skill already exists
                existing = Skill.query.filter_by(title=skill_title, category=category).first()
                
                if not existing:
                    skill = Skill(
                        user_id=admin.id,
                        title=skill_title,
                        description=f"Learn {skill_title} from experienced mentors in our community.",
                        category=category,
                        skill_type='offered',
                        is_approved=True
                    )
                    db.session.add(skill)
                    skills_added += 1
        
        db.session.commit()
        print(f"Successfully added {skills_added} skills to the database!")
        
        # Print summary
        print("\nSkills by Category:")
        for category, skills in skills_data.items():
            count = Skill.query.filter_by(category=category).count()
            print(f"  {category}: {count} skills")


if __name__ == '__main__':
    seed_skills()

