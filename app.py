from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import uuid
import nltk
from flask import session
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from dotenv import load_dotenv
from flask_migrate import Migrate
 



# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///studycoore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Initialize database
from models import db
db.init_app(app) 

# Initialize Flask-Migrate
migrate = Migrate(app, db)  # Add this line after db initialization

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Import models after db initialization
from models import User, Notebook, Note, Tag, note_tags

# User loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's notebooks and recent notes
    notebooks = Notebook.query.filter_by(user_id=current_user.id).all()
    recent_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html', notebooks=notebooks, recent_notes=recent_notes)

# Auth routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('login'))
            
        login_user(user, remember=remember)
        return redirect(url_for('dashboard'))
        
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email address already exists')
            return redirect(url_for('register'))
            
        new_user = User(
            email=email,
            name=name,
            password=generate_password_hash(password, method='sha256')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
        
    return render_template('auth/register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Notebook routes
@app.route('/notebooks')
@login_required
def list_notebooks():
    notebooks = Notebook.query.filter_by(user_id=current_user.id).all()
    return render_template('notebooks/list.html', notebooks=notebooks)

@app.route('/notebooks/create', methods=['GET', 'POST'])
@login_required
def create_notebook():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        new_notebook = Notebook(
            title=title,
            description=description,
            user_id=current_user.id
        )
        
        db.session.add(new_notebook)
        db.session.commit()
        
        flash('Notebook created successfully!')
        return redirect(url_for('list_notebooks'))
        
    return render_template('notebooks/create.html')

@app.route('/notebooks/<int:notebook_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_notebook(notebook_id):
    notebook = Notebook.query.get_or_404(notebook_id)
    
    if notebook.user_id != current_user.id:
        flash('You do not have permission to edit this notebook.')
        return redirect(url_for('list_notebooks'))
        
    if request.method == 'POST':
        notebook.title = request.form.get('title')
        notebook.description = request.form.get('description')
        
        db.session.commit()
        
        flash('Notebook updated successfully!')
        return redirect(url_for('list_notebooks'))
        
    return render_template('notebooks/edit.html', notebook=notebook)

@app.route('/notebooks/<int:notebook_id>/delete')
@login_required
def delete_notebook(notebook_id):
    notebook = Notebook.query.get_or_404(notebook_id)
    
    if notebook.user_id != current_user.id:
        flash('You do not have permission to delete this notebook.')
        return redirect(url_for('list_notebooks'))
        
    db.session.delete(notebook)
    db.session.commit()
    
    flash('Notebook deleted successfully!')
    return redirect(url_for('list_notebooks'))

# Note routes
@app.route('/notes')
@login_required
def list_notes():
    notebook_id = request.args.get('notebook_id')
    tag_name = request.args.get('tag')
    
    # Base query
    query = Note.query.filter_by(user_id=current_user.id)
    
    # Filter by notebook if specified
    if notebook_id:
        query = query.filter_by(notebook_id=notebook_id)
    
    # Filter by tag if specified
    if tag_name:
        query = query.join(note_tags).join(Tag).filter(Tag.name == tag_name)
    
    notes = query.all()
    notebooks = Notebook.query.filter_by(user_id=current_user.id).all()
    
    # Get all tags for the user
    user_tags = Tag.query.join(note_tags).join(Note).filter(Note.user_id == current_user.id).distinct().all()
    
    return render_template('notes/list.html', notes=notes, notebooks=notebooks, tags=user_tags)

# Update the create_note route
@app.route('/notes/create', methods=['GET', 'POST'])
@login_required
def create_note():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        notebook_id = request.form.get('notebook_id')
        tags_input = request.form.get('tags', '')
        
        # Process tags - split by comma and clean up
        tags = []
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        
        new_note = Note(
            title=title,
            content=content,
            notebook_id=notebook_id,
            user_id=current_user.id
        )
        
        # Process tags
        for tag_name in tags:
            tag_name = tag_name.strip()
            if tag_name:
                # Check if tag already exists (case-insensitive)
                tag = Tag.query.filter(db.func.lower(Tag.name) == db.func.lower(tag_name)).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                new_note.tags.append(tag)
        
        db.session.add(new_note)
        db.session.commit()
        
        flash('Note created successfully!')
        return redirect(url_for('view_note', note_id=new_note.id))
        
    notebooks = Notebook.query.filter_by(user_id=current_user.id).all()
    return render_template('notes/create.html', notebooks=notebooks)

@app.route('/notes/<int:note_id>')
@login_required
def view_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if note.user_id != current_user.id:
        flash('You do not have permission to view this note.')
        return redirect(url_for('list_notes'))
        
    return render_template('notes/view.html', note=note)

# Update the edit_note route
@app.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if note.user_id != current_user.id:
        flash('You do not have permission to edit this note.')
        return redirect(url_for('list_notes'))
        
    if request.method == 'POST':
        note.title = request.form.get('title')
        note.content = request.form.get('content')
        note.notebook_id = request.form.get('notebook_id')
        tags_input = request.form.get('tags', '')
        
        # Process tags - split by comma and clean up
        tags = []
        if tags_input:
            tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        
        # Update tags
        note.tags.clear()
        for tag_name in tags:
            tag_name = tag_name.strip()
            if tag_name:
                # Check if tag already exists (case-insensitive)
                tag = Tag.query.filter(db.func.lower(Tag.name) == db.func.lower(tag_name)).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                note.tags.append(tag)
        
        note.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Note updated successfully!')
        return redirect(url_for('view_note', note_id=note.id))
        
    notebooks = Notebook.query.filter_by(user_id=current_user.id).all()
    tags = ', '.join([tag.name for tag in note.tags])
    
    return render_template('notes/edit.html', note=note, notebooks=notebooks, tags=tags)

@app.route('/notes/<int:note_id>/delete')
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if note.user_id != current_user.id:
        flash('You do not have permission to delete this note.')
        return redirect(url_for('list_notes'))
        
    db.session.delete(note)
    db.session.commit()
    
    flash('Note deleted successfully!')
    return redirect(url_for('list_notes'))


# Profile routes
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.name = request.form.get('name')
        current_user.bio = request.form.get('bio')
        
        # Handle profile picture upload
        if 'profile_pic' in request.files:
            file = request.files['profile_pic']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Add UUID to prevent filename collisions
                unique_filename = f"{uuid.uuid4().hex}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', unique_filename)
                
                # Create directory if it doesn't exist
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                file.save(filepath)
                
                # Delete old profile picture if exists
                if current_user.profile_pic:
                    old_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', current_user.profile_pic)
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)
                
                current_user.profile_pic = unique_filename
        
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('profile'))
        
    return render_template('profile.html')

@app.route('/profile/remove-pic', methods=['POST'])
@login_required
def remove_profile_pic():
    if current_user.profile_pic:
        # Delete the file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'profiles', current_user.profile_pic)
        if os.path.exists(filepath):
            os.remove(filepath)
        
        # Update database
        current_user.profile_pic = None
        db.session.commit()
    
    return jsonify({'success': True})

# Share routes
@app.route('/share/<int:note_id>', methods=['GET', 'POST'])
@login_required
def share_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if note.user_id != current_user.id:
        flash('You do not have permission to share this note.')
        return redirect(url_for('list_notes'))
        
    if request.method == 'POST':
        # Check if we're making it private or public
        if 'make_private' in request.form:
            note.is_public = False
            db.session.commit()
            flash('Note is now private. The share link has been disabled.')
            return redirect(url_for('view_note', note_id=note.id))
        else:
            # Generate shareable link
            note.is_public = True
            db.session.commit()
            
            share_url = url_for('view_shared_note', note_id=note.id, _external=True)
            return render_template('share.html', note=note, share_url=share_url)
        
    return render_template('share.html', note=note)

@app.route('/shared/<int:note_id>')
def view_shared_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if not note.is_public:
        return render_template('notes/view_shared.html', 
                             error="This note is not shared publicly.",
                             note=note)
        
    return render_template('notes/view_shared.html', note=note)

# Helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Update user preferences
        current_user.theme_preference = request.form.get('theme_preference', 'system')
        current_user.email_notifications = 'email_notifications' in request.form
        current_user.auto_save = 'auto_save' in request.form
        current_user.summary_length = int(request.form.get('summary_length', 150))
        current_user.items_per_page = int(request.form.get('items_per_page', 10))
        
        db.session.commit()
        session['theme'] = current_user.theme_preference 
        
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('settings'))
    
    return render_template('settings.html')

# Create necessary directories
with app.app_context():
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'profiles'), exist_ok=True)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    