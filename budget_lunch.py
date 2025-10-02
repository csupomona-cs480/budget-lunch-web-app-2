from flask import Flask, render_template, send_from_directory, send_file, request, session, redirect, url_for, jsonify
import os
import jwt
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key for sessions

# Supabase configuration
SUPABASE_URL = "https://tcncaflslvyvaqwvhjbt.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRjbmNhZmxzbHZ5dmFxd3ZoamJ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTcwMDUwOTEsImV4cCI6MjA3MjU4MTA5MX0.6ScS8s8HH9TtjFH78n48vqawTAqajuFDVPgRZclVChU"
# Note: For production, you should get the service key from your Supabase dashboard
# Go to Settings > API > service_role key
SUPABASE_SERVICE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRjbmNhZmxzbHZ5dmFxd3ZoamJ0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NzAwNTA5MSwiZXhwIjoyMDcyNTgxMDkxfQ.YourServiceKeyHere"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def verify_jwt_token(token):
    """Verify JWT token with Supabase"""
    try:
        # Verify the token with Supabase
        response = supabase.auth.get_user(token)
        if response.user:
            return response.user
        return None
    except Exception as e:
        print(f"Token verification error: {e}")
        return None

def get_user_from_request():
    """Get user from Authorization header or session"""
    # Check Authorization header first
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        user = verify_jwt_token(token)
        if user:
            return user
    
    # Check session
    token = session.get('access_token')
    if token:
        user = verify_jwt_token(token)
        if user:
            return user
    
    return None

def is_authenticated():
    """Check if user is authenticated"""
    return get_user_from_request() is not None

def require_auth(f):
    """Decorator to require authentication for routes"""
    def decorated_function(*args, **kwargs):
        if not is_authenticated():
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


# Authentication routes
@app.route("/login")
def login():
    return send_file('login.html')

@app.route("/signup", methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400
    
    if len(password) < 6:
        return jsonify({'success': False, 'message': 'Password must be at least 6 characters long'}), 400
    
    try:
        # Sign up user with Supabase
        response = supabase.auth.sign_up({
            'email': email,
            'password': password
        })
        
        if response.user:
            return jsonify({
                'success': True, 
                'message': 'Account created successfully! Please check your email to confirm your account.',
                'user': {
                    'id': response.user.id,
                    'email': response.user.email
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Failed to create account'}), 400
            
    except Exception as e:
        error_message = str(e)
        if 'already registered' in error_message.lower():
            return jsonify({'success': False, 'message': 'An account with this email already exists'}), 400
        elif 'invalid email' in error_message.lower():
            return jsonify({'success': False, 'message': 'Please enter a valid email address'}), 400
        else:
            return jsonify({'success': False, 'message': 'Failed to create account. Please try again.'}), 400

@app.route("/login", methods=['POST'])
def login_post():
    data = request.get_json()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email and password are required'}), 400
    
    try:
        # Sign in user with Supabase
        response = supabase.auth.sign_in_with_password({
            'email': email,
            'password': password
        })
        
        if response.user and response.session:
            # Store the access token in session
            session['access_token'] = response.session.access_token
            session['refresh_token'] = response.session.refresh_token
            session['user_id'] = response.user.id
            
            return jsonify({
                'success': True, 
                'message': 'Login successful',
                'user': {
                    'id': response.user.id,
                    'email': response.user.email
                },
                'access_token': response.session.access_token
            })
        else:
            return jsonify({'success': False, 'message': 'Login failed'}), 401
            
    except Exception as e:
        error_message = str(e)
        if 'invalid login credentials' in error_message.lower():
            return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
        elif 'email not confirmed' in error_message.lower():
            return jsonify({'success': False, 'message': 'Please check your email and confirm your account before logging in'}), 401
        else:
            return jsonify({'success': False, 'message': 'Login failed. Please try again.'}), 401

@app.route("/logout", methods=['POST'])
def logout():
    try:
        # Get the current access token
        access_token = session.get('access_token')
        if access_token:
            # Sign out from Supabase
            supabase.auth.sign_out()
        
        # Clear session
        session.pop('access_token', None)
        session.pop('refresh_token', None)
        session.pop('user_id', None)
        
        return jsonify({'success': True, 'message': 'Logged out successfully'})
    except Exception as e:
        # Clear session even if Supabase logout fails
        session.pop('access_token', None)
        session.pop('refresh_token', None)
        session.pop('user_id', None)
        return jsonify({'success': True, 'message': 'Logged out successfully'})

@app.route("/check-auth")
def check_auth():
    user = get_user_from_request()
    if user:
        return jsonify({
            'authenticated': True,
            'user': {
                'id': user.id,
                'email': user.email
            }
        })
    else:
        return jsonify({'authenticated': False})

@app.route("/search/<price>")
def search_food_with_price(price):
    price = float(price)
    res = []

    query_res = supabase.table('lunch_db').select('*').lte('price', price).execute()
    
    for food in query_res.data:        
        res.append(food)
    return res

@app.route("/add/<name>/<price>")
@require_auth
def add_food_item(name, price):
    price = float(price)
    imageurl = request.args.get('imageurl')
    # add the item to the supabase database
    supabase.table('lunch_db').insert({
        "name" : name,
        "price" : price,
        "imageurl" : imageurl
    }).execute()
    return "OK"

@app.route("/update/<int:item_id>", methods=['PUT'])
@require_auth
def update_food_item(item_id):
    data = request.get_json()
    name = data.get('name')
    price = float(data.get('price'))
    imageurl = data.get('imageurl')
    
    # update the item in the supabase database
    supabase.table('lunch_db').update({
        "name": name,
        "price": price,
        "imageurl": imageurl
    }).eq('id', item_id).execute()
    return "OK"

@app.route("/delete/<int:item_id>", methods=['DELETE'])
@require_auth
def delete_food_item(item_id):
    # delete the item from the supabase database
    supabase.table('lunch_db').delete().eq('id', item_id).execute()
    return "OK"

@app.route("/list")
@require_auth
def list_all_items():
    # get all items from the supabase database
    query_res = supabase.table('lunch_db').select('*').execute()
    return query_res.data



@app.route("/")
def home():
    return send_file('index.html')

@app.route("/admin.html")
@require_auth
def serve_admin_html():
    return send_file('admin.html')


@app.route("/styles.css")
def serve_css():
    return send_file('styles.css', mimetype='text/css')

@app.route("/script.js")
def serve_js():
    return send_file('script.js', mimetype='application/javascript')

@app.route("/admin.js")
def serve_js_admin():
    return send_file('admin.js', mimetype='application/javascript')

@app.route("/login.js")
def serve_js_login():
    return send_file('login.js', mimetype='application/javascript')


@app.route("/hello")
def show_hello_world():
    return "Welcome to CS4800 Software Engineering"


app.run(host = "0.0.0.0", port = 5001)