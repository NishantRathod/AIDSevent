# 📚 KnowledgeShare - PDF Sharing Platform

A modern, feature-rich web application for sharing educational PDFs with a token-based reward system. Built with Flask and SQLite.

## ✨ Features

### 🔐 Authentication & User Management
- **User Registration** - Sign up with email and password validation
- **Secure Login** - Password hashing with Werkzeug
- **Session Management** - Secure user sessions with login_required decorator
- **Profile Management** - Edit name and bio

### 🪙 Token System
- **Welcome Bonus** - Get 50 tokens upon registration
- **Upload Rewards** - Earn 10 tokens for each PDF upload
- **View Cost** - Spend 5 tokens to view others' PDFs (free for your own)
- **Download Cost** - Spend 3 tokens to download others' PDFs
- **Token History** - Complete transaction log with timestamps

### 📤 PDF Upload & Management
- **Easy Upload** - Simple drag-and-drop interface
- **Metadata** - Title, subject, and description for each PDF
- **Subject Categories** - 11+ subject categories (Computer Science, Math, Physics, etc.)
- **File Validation** - PDF-only uploads with proper error handling
- **My Uploads** - View all your uploaded PDFs
- **Delete Function** - Remove your own uploads

### 📥 PDF Discovery & Access
- **Browse PDFs** - Beautiful grid layout with cards
- **Advanced Search** - Search by title or description
- **Subject Filter** - Filter by specific subjects
- **Sort Options** - Sort by recent, popular, or oldest
- **View Online** - Open PDFs in browser
- **Download** - Save PDFs to your device
- **Statistics** - View count and download count for each PDF

### 📊 Dashboard & Statistics
- **Personal Dashboard** - Overview of your activity
- **Statistics Cards** - Track uploads, downloads, views, and tokens
- **Recent Uploads** - Quick access to your latest PDFs
- **Token Balance** - Always visible token count

### 🏆 Leaderboard
- **Top Contributors** - Rankings by token count
- **Medals** - Gold, silver, bronze for top 3 users
- **User Stats** - Display uploads and total views
- **Competitive Element** - Encourage quality contributions

### 🎨 Modern UI/UX
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Beautiful Gradients** - Purple/violet color scheme
- **Smooth Animations** - Slide-in, fade-in effects
- **Interactive Cards** - Hover effects and transitions
- **Google Fonts** - Poppins font family
- **Flash Messages** - User feedback for all actions
- **Icons & Emojis** - Visual indicators throughout

### 🔧 Technical Features
- **SQLite Database** - Lightweight, no configuration needed
- **Secure File Handling** - Files saved with unique names
- **Session Security** - Secret key for session encryption
- **Error Handling** - Comprehensive validation and error messages
- **Auto Database Init** - Tables created automatically on first run
- **Download History** - Track all PDF downloads
- **Transaction Log** - Complete audit trail for tokens

## 🗂️ Database Schema

### Users Table
- `id` - Primary key
- `name` - User's full name
- `email` - Unique email address
- `password` - Hashed password
- `tokens` - Token balance (default: 50)
- `bio` - User biography
- `created_at` - Registration timestamp

### PDFs Table
- `id` - Primary key
- `title` - PDF title
- `subject` - Subject category
- `description` - Optional description
- `filename` - Stored filename
- `uploader_id` - Foreign key to users
- `views` - View count
- `downloads` - Download count
- `created_at` - Upload timestamp

### Token History Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `change` - Token amount (+/-)
- `reason` - Transaction description
- `created_at` - Transaction timestamp

### Download History Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `pdf_id` - Foreign key to pdfs
- `downloaded_at` - Download timestamp

## 🚀 Installation & Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Application**
   - Open browser to `http://127.0.0.1:5000`
   - Register a new account
   - Start uploading and sharing!

## 📱 Pages & Routes

### Public Routes
- `/` - Login page
- `/register` - Registration page

### Protected Routes (Login Required)
- `/dashboard` - Main dashboard with statistics
- `/upload` - PDF upload form
- `/pdfs` - Browse all PDFs with filters
- `/open/<id>` - View PDF in browser
- `/download/<id>` - Download PDF file
- `/tokens` - View token transaction history
- `/leaderboard` - Community rankings
- `/profile` - View and edit profile
- `/my-uploads` - Manage your uploads
- `/delete-pdf/<id>` - Delete your PDF
- `/edit-profile` - Update profile information
- `/logout` - Log out

## 🎯 Token Economics

| Action | Tokens |
|--------|--------|
| Register | +50 🎁 |
| Upload PDF | +10 💎 |
| View Own PDF | Free ✓ |
| View Others' PDF | -5 👀 |
| Download Own PDF | Free ✓ |
| Download Others' PDF | -3 📥 |

## 🎨 Color Scheme

- **Primary Gradient**: `#667eea` → `#764ba2` (Purple/Violet)
- **Background**: `#f5f7fa` (Light gray-blue)
- **Cards**: `#ffffff` (White)
- **Success**: `#28a745` (Green)
- **Error**: `#dc3545` (Red)
- **Warning**: `#ffc107` (Yellow)

## 📂 Project Structure

```
AIDS event/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── database.db           # SQLite database (auto-created)
├── uploads/
│   └── pdfs/            # Uploaded PDF files
└── templates/
    ├── index.html        # Login page
    ├── register.html     # Registration page
    ├── dashboard.html    # User dashboard
    ├── upload.html       # PDF upload form
    ├── view_pdfs.html    # Browse PDFs
    ├── token_history.html # Token transactions
    ├── leaderboard.html  # Community rankings
    ├── profile.html      # User profile
    └── my_uploads.html   # User's uploads
```

## 🔒 Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Login required decorator for protected routes
- SQL injection prevention with parameterized queries
- File type validation (PDF only)
- User-specific file access control
- CSRF protection through Flask sessions

## 🌟 Best Practices Implemented

- Clean, readable code with comments
- Consistent naming conventions
- Error handling and validation
- User feedback with flash messages
- Responsive mobile-first design
- Accessible UI elements
- Semantic HTML structure
- CSS animations and transitions
- Database normalization

## 🚦 Future Enhancements (Optional)

- PDF preview thumbnails
- Comments and ratings system
- Advanced search with tags
- Email verification
- Password reset functionality
- Admin panel
- Bulk upload
- PDF encryption
- API endpoints
- Social sharing
- Notifications system

## 📝 Notes

- Default admin/test credentials: Create via registration
- Tokens cannot go negative - insufficient token checks in place
- PDF files stored with unique names to prevent conflicts
- All timestamps in UTC
- Maximum file size limited by Flask defaults (16MB)

## 🤝 Contributing

Feel free to fork, improve, and submit pull requests!

## 📄 License

This project is open source and available for educational purposes.

---

**Made with ❤️ using Flask and Python**
