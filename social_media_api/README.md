 Find Your Soulmate - Dating App API

A modern Django REST Framework API for a dating platform where 
users can find connections, like profiles, and match 
with potential soulmates.

Live Demo
[View Live App]

Features
- Custom User Profiles: Detailed profiles with bio, photos, interests, age, location
- Authentication: Token-based login & registration
- Profile Discovery: Browse and search potential matches with filters
- Likes & Matches: Like profiles and get notified when someone likes you back
- Real-time Notifications: Get alerts for new matches, likes, and messages
- Privacy Controls: Block/report users, hide profile from certain users

 Setup
1. Clone the repository
2. Create a virtual environment
3. Install dependencies:
 pip install -r requirements.txt
 python manage.py migrate
 python manage.py createsuperuser
 python manage.py runserver

API Endpoints Overview
Users
Register: POST /api/accounts/register/
Login: POST /api/accounts/login/
Profile: GET /api/accounts/profile/
Update Profile: PUT /api/accounts/profile/
View User: GET /api/accounts/users/<id>/

Posts
 List: GET /posts/ (supports search & ordering)
 Create: POST /posts/
 Retrieve/Update/Delete: GET | PUT | DELETE /posts/<id>/

Comments
 List: GET /comments/
 Create: POST /comments/
 Retrieve/Update/Delete: GET | PUT | DELETE /comments/<comment_id>/

Likes & Matches

Like User: POST /api/like/<user_id>/
Unlike User: POST /api/unlike/<user_id>/
Likes Sent: GET /api/likes/sent/
Likes Received: GET /api/likes/received/
View Matches: GET /api/matches/
Unmatch: DELETE /api/matches/<match_id>/

Messaging

Conversations: GET /api/conversations/
Send Message: POST /api/conversations/<match_id>/messages/
View Messages: GET /api/conversations/<match_id>/messages/

Notifications

View Notifications: GET /api/notifications/
Unread Count: GET /api/notifications/unread-count/
Mark as Read: POST /api/notifications/<id>/read/

Safety

Block User: POST /api/block/<user_id>/
Report User: POST /api/report/<user_id>/

How Matching Works

User A likes User B → Notification sent to User B
User B likes User A back → MATCH!
Both can now message each other

Tech Stack

Backend: Django, Django REST Framework
Database: PostgreSQL (production) / SQLite (development)
Authentication: Token Authentication
Image Storage: Cloudinary / AWS S3
Geolocation: GeoDjango

 About the Developer

Hi! I’m yoli, a Software Engineering student at AMU and 
an ALX Backend Program participant.
I’m passionate about Python, web development, and 
creating full-stack applications that are both functional 
and user-friendly.
































   
