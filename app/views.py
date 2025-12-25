from flask import url_for, redirect, render_template, flash, g, session, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from app import app, lm, db
from app.forms import ExampleForm, LoginForm
from app.models import User
import requests


@app.route('/')
def index():
	return render_template('index.html')


@app.route('/list/')
def posts():
	return render_template('list.html')


@app.route('/new/')
@login_required
def new():
	form = ExampleForm()
	return render_template('new.html', form=form)


@app.route('/save/', methods = ['GET','POST'])
@login_required
def save():
	form = ExampleForm()
	if form.validate_on_submit():
		print("salvando os dados:")
		print(form.title.data)
		print(form.content.data)
		print(form.date.data)
		flash('Dados salvos!')
	return render_template('new.html', form=form)

@app.route('/view/<id>/')
def view(id):
	return render_template('view.html')

# === User login methods ===

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login/', methods = ['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Find user by username
        user = User.query.filter_by(user=form.user.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')

    return render_template('login.html', 
        title = 'Sign In',
        form = form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

# === API Authentication endpoints ===

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """API endpoint for authentication"""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400
    
    user = User.query.filter_by(user=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({
            'success': True,
            'message': 'Logged in successfully',
            'user': {
                'id': user.id,
                'username': user.user,
                'name': user.name,
                'email': user.email
            }
        }), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def api_logout():
    """API endpoint for logout"""
    logout_user()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

@app.route('/api/auth/status', methods=['GET'])
def api_auth_status():
    """Check authentication status"""
    if current_user.is_authenticated:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': current_user.id,
                'username': current_user.user,
                'name': current_user.name,
                'email': current_user.email
            }
        }), 200
    else:
        return jsonify({'authenticated': False}), 200

# === Proxy endpoints ===

@app.route('/api/proxy/<path:proxy_name>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy_endpoint(proxy_name):
    """
    Proxy requests to configured external URLs.
    Configure proxy endpoints in configuration.py under PROXY_ENDPOINTS.
    Example: PROXY_ENDPOINTS = {'/api/proxy/example': 'https://api.example.com'}
    """
    proxy_config = app.config.get('PROXY_ENDPOINTS', {})
    
    # Build the full proxy path
    proxy_path = f'/api/proxy/{proxy_name}'
    
    # Find matching proxy configuration
    target_url = None
    for config_path, url in proxy_config.items():
        if proxy_path.startswith(config_path):
            # Replace the config path with the target URL
            target_url = url + proxy_path.replace(config_path, '')
            break
    
    if not target_url:
        return jsonify({'error': 'No proxy configuration found for this path'}), 404
    
    # Forward the request
    try:
        # Prepare headers (exclude host header)
        headers = {key: value for key, value in request.headers if key.lower() != 'host'}
        
        # Forward the request with the same method, headers, and body
        response = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            params=request.args,
            allow_redirects=False
        )
        
        # Return the response
        return (response.content, response.status_code, response.headers.items())
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Proxy request failed: {str(e)}'}), 502

# ====================
