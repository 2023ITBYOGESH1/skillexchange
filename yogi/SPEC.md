# SkillSwap - Skill Exchange Platform Specification

## 1. Project Overview

**Project Name:** SkillSwap  
**Project Type:** Full-stack Web Application  
**Core Functionality:** A skill exchange platform where users can teach skills they know and learn skills they want from others  
**Target Users:** Individuals looking to exchange knowledge and skills with others in their community

---

## 2. Technology Stack

- **Backend:** Python + Flask
- **Database:** SQLite
- **Frontend:** HTML5, CSS3, JavaScript
- **Libraries:**
  - Flask-Login (authentication)
  - Flask-WTF (forms)
  - Werkzeug (password hashing)
  - SQLAlchemy (ORM)

---

## 3. Database Models

### User Model
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| username | String(80) | Unique username |
| email | String(120) | Unique email |
| password_hash | String(256) | Hashed password |
| bio | Text | User biography |
| location | String(120) | User location |
| profile_picture | String | Profile picture filename |
| rating | Float | Average rating (default 0) |
| is_admin | Boolean | Admin flag (default False) |
| is_banned | Boolean | Ban status (default False) |
| created_at | DateTime | Account creation timestamp |

### Skill Model
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User |
| title | String(100) | Skill title |
| description | Text | Skill description |
| category | String(50) | Skill category |
| skill_type | String(10) | "offered" or "wanted" |
| is_approved | Boolean | Admin approval status |
| created_at | DateTime | Creation timestamp |

### ExchangeRequest Model
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| sender_id | Integer | Foreign key to User |
| receiver_id | Integer | Foreign key to User |
| sender_skill_id | Integer | Foreign key to Skill |
| receiver_skill_id | Integer | Foreign key to Skill |
| status | String(20) | pending/accepted/rejected/completed |
| message | Text | Request message |
| created_at | DateTime | Creation timestamp |

### Message Model
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| sender_id | Integer | Foreign key to User |
| receiver_id | Integer | Foreign key to User |
| content | Text | Message content |
| created_at | DateTime | Creation timestamp |
| is_read | Boolean | Read status |

### Review Model
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| reviewer_id | Integer | Foreign key to User |
| reviewed_id | Integer | Foreign key to User |
| rating | Integer | Rating (1-5) |
| comment | Text | Review comment |
| created_at | DateTime | Creation timestamp |

### Bookmark Model
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User |
| skill_id | Integer | Foreign key to Skill |
| created_at | DateTime | Creation timestamp |

### Report Model
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| reporter_id | Integer | Foreign key to User |
| reported_id | Integer | Foreign key to User |
| reason | Text | Report reason |
| status | String(20) | pending/reviewed/resolved |
| created_at | DateTime | Creation timestamp |

---

## 4. UI/UX Specification

### Color Palette
- **Primary:** #1a1a2e (Deep Navy)
- **Secondary:** #16213e (Dark Blue)
- **Accent:** #e94560 (Coral Red)
- **Success:** #00d9a5 (Mint Green)
- **Warning:** #ffc107 (Amber)
- **Background:** #0f0f1a (Near Black)
- **Surface:** #1f1f2e (Card Background)
- **Text Primary:** #ffffff
- **Text Secondary:** #a0a0b0
- **Border:** #2a2a3e

### Typography
- **Headings:** 'Outfit', sans-serif (weights: 600, 700)
- **Body:** 'DM Sans', sans-serif (weights: 400, 500)
- **Monospace:** 'JetBrains Mono', monospace

### Font Sizes
- H1: 2.5rem
- H2: 2rem
- H3: 1.5rem
- Body: 1rem
- Small: 0.875rem

### Spacing System
- xs: 0.25rem
- sm: 0.5rem
- md: 1rem
- lg: 1.5rem
- xl: 2rem
- 2xl: 3rem

### Layout
- Max content width: 1200px
- Sidebar width: 250px
- Card border-radius: 12px
- Button border-radius: 8px

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### Visual Effects
- Card shadows: 0 4px 20px rgba(0, 0, 0, 0.3)
- Hover transitions: 0.3s ease
- Gradient accents: linear-gradient(135deg, #e94560, #ff6b6b)
- Glassmorphism on cards: backdrop-filter: blur(10px)

---

## 5. Pages & Routes

### Public Routes
- `/` - Home page with featured skills
- `/register` - Registration page
- `/login` - Login page
- `/skills` - Browse all skills
- `/skills/<id>` - View skill details

### Protected Routes (User)
- `/profile` - User profile
- `/profile/edit` - Edit profile
- `/skills/add` - Add new skill
- `/skills/edit/<id>` - Edit skill
- `/skills/delete/<id>` - Delete skill
- `/bookmarks` - View bookmarked skills
- `/exchange-requests` - View exchange requests
- `/exchange-requests/<id>/accept` - Accept request
- `/exchange-requests/<id>/reject` - Reject request
- `/chat` - Chat with users
- `/chat/<user_id>` - Chat with specific user
- `/reviews/<user_id>` - View user reviews
- `/reviews/add/<user_id>` - Add review

### Admin Routes
- `/admin` - Admin dashboard
- `/admin/users` - List all users
- `/admin/users/<id>` - View user profile
- `/admin/users/edit/<id>` - Edit user
- `/admin/users/delete/<id>` - Delete user
- `/admin/users/ban/<id>` - Ban user
- `/admin/users/unban/<id>` - Unban user
- `/admin/users/promote/<id>` - Promote to admin
- `/admin/users/demote/<id>` - Demote to user
- `/admin/users/reset-password/<id>` - Reset user password
- `/admin/skills` - Moderate skills
- `/admin/skills/approve/<id>` - Approve skill
- `/admin/skills/reject/<id>` - Reject skill
- `/admin/reports` - View reported users

---

## 6. Admin Dashboard Features

### Statistics Cards
- Total Users count
- Total Skills count
- Active Exchanges count
- Pending Requests count

### Top Users Table
- Display top 10 users by rating
- Show username, rating, skills count

### Quick Actions
- Buttons for common admin tasks

---

## 7. Functionality Specification

### Authentication
- User registration with username, email, password
- Login with email and password
- Password hashing with Werkzeug
- Session management with Flask-Login
- Logout functionality

### User Profile
- View and edit profile information
- Upload profile picture
- Add/edit skills offered
- Add/edit skills wanted
- View own reviews

### Skill Management
- Create skills (offered/wanted)
- Edit own skills
- Delete own skills
- Browse skills by category
- Search skills

### Exchange System
- Send exchange requests
- Accept/reject requests
- View request history
- Mark exchanges as completed

### Chat System
- Real-time messaging between users
- Conversation list
- Unread message indicators

### Review System
- Leave ratings (1-5 stars)
- Leave comments
- View user reviews

### Bookmark System
- Bookmark skills
- View bookmarked skills
- Remove bookmarks

### Admin System
- Full user management
- Skill moderation
- Report handling
- System statistics

---

## 8. Acceptance Criteria

### Authentication
- [ ] Users can register with unique email and username
- [ ] Users can login with email and password
- [ ] Passwords are securely hashed
- [ ] Users can logout

### Profile
- [ ] Users can view their profile
- [ ] Users can edit profile information
- [ ] Users can add skills they offer
- [ ] Users can add skills they want to learn

### Skills
- [ ] Users can browse all skills
- [ ] Users can view skill details
- [ ] Users can add new skills
- [ ] Users can edit their skills
- [ ] Users can delete their skills

### Exchange
- [ ] Users can send exchange requests
- [ ] Users can accept/reject requests
- [ ] Users can view request history

### Chat
- [ ] Users can message other users
- [ ] Users can view conversation history

### Reviews
- [ ] Users can leave reviews for others
- [ ] Users can view reviews on their profile

### Bookmarks
- [ ] Users can bookmark skills
- [ ] Users can view bookmarked skills
- [ ] Users can remove bookmarks

### Admin
- [ ] Admin can view dashboard with statistics
- [ ] Admin can view all users
- [ ] Admin can search users
- [ ] Admin can edit user details
- [ ] Admin can delete users
- [ ] Admin can ban/unban users
- [ ] Admin can reset passwords
- [ ] Admin can promote/demote users
- [ ] Admin can view reported users
- [ ] Admin can moderate skills

---

## 9. File Structure

```
yogi/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── models.py               # Database models
├── forms.py                # WTForms definitions
├── routes/
│   ├── __init__.py
│   ├── auth.py             # Authentication routes
│   ├── main.py             # Main routes
│   ├── skills.py           # Skill routes
│   ├── exchange.py         # Exchange routes
│   ├── chat.py             # Chat routes
│   ├── admin.py            # Admin routes
│   └── api.py              # API routes
├── static/
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   ├── js/
│   │   └── main.js         # JavaScript
│   └── images/             # Image assets
├── templates/
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── profile/
│   │   ├── profile.html
│   │   └── edit_profile.html
│   ├── skills/
│   │   ├── skills.html
│   │   ├── skill_detail.html
│   │   └── add_skill.html
│   ├── exchange/
│   │   ├── requests.html
│   │   └── request_detail.html
│   ├── chat/
│   │   ├── chat.html
│   │   └── conversation.html
│   ├── admin/
│   │   ├── dashboard.html
│   │   ├── users.html
│   │   ├── user_detail.html
│   │   ├── skills_moderation.html
│   │   └── reports.html
│   └── partials/
│       ├── navbar.html
│       └── footer.html
├── uploads/                # Uploaded files
├── instance/               # SQLite database
├── requirements.txt       # Python dependencies
└── SPEC.md                # This specification
```

