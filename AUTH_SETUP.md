# Supabase Authentication Setup

## Overview
The Budget Lunch application now uses Supabase authentication for secure user management. This provides enterprise-grade authentication with email verification, password reset, and secure JWT tokens.

## Features
- ✅ **User Registration**: Email/password signup with validation
- ✅ **User Login**: Secure authentication with JWT tokens
- ✅ **Email Verification**: Users must verify their email before accessing admin features
- ✅ **Session Management**: Secure session handling with automatic token refresh
- ✅ **Protected Routes**: All admin operations require authentication
- ✅ **Logout**: Secure session termination

## Setup Instructions

### 1. Supabase Configuration
1. Go to your Supabase dashboard
2. Navigate to **Settings > API**
3. Copy your **service_role** key (not the anon key)
4. Replace the placeholder in `budget_lunch.py`:
   ```python
   SUPABASE_SERVICE_KEY = "your_actual_service_key_here"
   ```

### 2. Authentication Settings
In your Supabase dashboard:
1. Go to **Authentication > Settings**
2. Enable **Email confirmations** (recommended)
3. Configure **Site URL** to match your domain
4. Set up **Redirect URLs** if needed

### 3. Database Permissions
Ensure your `lunch_db` table has proper RLS (Row Level Security) policies:
```sql
-- Allow authenticated users to read all items
CREATE POLICY "Allow authenticated read" ON lunch_db
FOR SELECT USING (auth.role() = 'authenticated');

-- Allow authenticated users to insert items
CREATE POLICY "Allow authenticated insert" ON lunch_db
FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Allow authenticated users to update items
CREATE POLICY "Allow authenticated update" ON lunch_db
FOR UPDATE USING (auth.role() = 'authenticated');

-- Allow authenticated users to delete items
CREATE POLICY "Allow authenticated delete" ON lunch_db
FOR DELETE USING (auth.role() = 'authenticated');
```

## Usage

### For Users
1. **Sign Up**: Click "Sign Up" on the login page
2. **Verify Email**: Check your email and click the verification link
3. **Login**: Use your email and password to access the admin portal
4. **Manage Items**: Full CRUD operations available after authentication

### For Developers
- All admin routes are protected with `@require_auth` decorator
- JWT tokens are automatically verified on each request
- Session management handles token refresh automatically
- Error handling provides user-friendly messages

## Security Features
- **JWT Tokens**: Secure, stateless authentication
- **Email Verification**: Prevents unauthorized account creation
- **Password Validation**: Minimum 6 characters required
- **Session Security**: Automatic token refresh and secure logout
- **CORS Protection**: Proper headers for cross-origin requests

## Troubleshooting

### Common Issues
1. **"Email not confirmed"**: User needs to check email and click verification link
2. **"Invalid credentials"**: Check email/password or verify account exists
3. **"Authentication required"**: User needs to login first
4. **Service key errors**: Ensure you're using the service_role key, not anon key

### Development Tips
- Use browser dev tools to check network requests
- Verify JWT tokens in the session storage
- Check Supabase logs for authentication errors
- Test with different user accounts to verify permissions

## API Endpoints

### Authentication
- `POST /signup` - Create new user account
- `POST /login` - Authenticate user
- `POST /logout` - Terminate user session
- `GET /check-auth` - Verify current authentication status

### Protected Admin Routes
- `GET /admin.html` - Admin portal (requires auth)
- `POST /add/<name>/<price>` - Add new item (requires auth)
- `PUT /update/<id>` - Update item (requires auth)
- `DELETE /delete/<id>` - Delete item (requires auth)
- `GET /list` - List all items (requires auth)

All protected routes return `401 Unauthorized` if authentication fails.

