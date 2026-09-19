Project completed so far
1. Database

You created a Neon PostgreSQL database with:

Users

User_Id
User_name
Email
Password_hash
Phone_no

Job_applications

Job_id
User_Id
Job_name
Company
Status
Apply_date
Expected_date

Relationship:

Users 1 ──── many Job_applications

User_Id in Job_applications identifies which user owns each application.

2. Flask setup

You connected Flask to Neon using:

pg8000
python-dotenv
Werkzeug password hashing
Flask session

Your .env contains the database connection and Flask secret key.

Keep .env in your local backup, but do NOT upload it to GitHub.

3. Registration

Implemented:

Register form
    ↓
Flask receives data
    ↓
generate_password_hash()
    ↓
INSERT into Users
    ↓
create session
    ↓
Home

You also added server-side empty-value checks.

You then added JavaScript validation for:

Username
Email
Password
Phone number

The JavaScript checks happen before the form is submitted, while the Flask checks remain as the backend layer.

4. Login

Implemented:

Username + Password
        ↓
SELECT password_hash
        ↓
check_password_hash()
        ↓
correct
        ↓
session["user_id"]
session["user_name"]
        ↓
Home

You also added JavaScript validation for username/password and a show-password checkbox.

5. Sessions / Authentication

You use:

session["user_id"]
session["user_name"]

for identifying the logged-in user.

Protected pages include:

/home
/addjob
/edit
/update
/delete
/profile
/psw
/psw_verify
/psw_update

Unauthenticated users are redirected to /Login.

6. Home dashboard

Home currently shows:

Welcome username
Total Applications
Companies
Applied
In Progress
Rejected

and retrieves the user's applications from the database.

The table displays:

Job Name
Company
Status
Apply Date
Expected Date
Actions
7. Add Application

Implemented the Add Job form.

A new application is inserted with the logged-in user's ID:

session["user_id"]

so applications are associated with the correct account.

JavaScript validation is also implemented for:

Job name
Company
Status
Applied date
Expected date

and Flask also performs backend validation.

8. Edit Application

Implemented:

Home
 ↓
Edit
 ↓
send job_id
 ↓
/edit
 ↓
SELECT application
 ↓
editjob.html
 ↓
change values
 ↓
/update
 ↓
UPDATE database

The selected job_id is carried through the edit form using a hidden input.

9. Update ownership/security

You changed the UPDATE query so the current user's ID is checked too:

job_id + session["user_id"]

So an application must belong to the logged-in user before it can be updated.

You also added backend validation for empty edited fields.

10. Delete Application

Implemented:

Home
 ↓
Delete
 ↓
job_id
 ↓
/delete
 ↓
DELETE

And you added the ownership check:

job_id + session["user_id"]

So the deletion is tied to the logged-in user.

11. Profile

Implemented /profile.

It retrieves:

User name
Email
Phone

using:

session["user_id"]

rather than asking the user which account to retrieve.

12. Change Password

Implemented the two-step flow using the same psw.html page:

Profile
 ↓
Change Password
 ↓
enter current password
 ↓
/psw_verify
 ↓
check_password_hash()
 ↓
Verified = True
 ↓
same page shows new-password fields
 ↓
/psw_update
 ↓
new password + confirmation
 ↓
generate_password_hash()
 ↓
UPDATE Users

You store a temporary verification flag in the session.

JavaScript validation is also implemented for the new password and confirmation.

13. Logout

Implemented:

session.clear()

then redirect to:

/Login
14. JavaScript training

You've now practiced:

DOMContentLoaded
addEventListener
submit
preventDefault()
getElementById()
.value
if / else
regex
regex.test()
form.submit()

and used JavaScript validation across:

Register
Login
Add Job
Edit/Update
Change Password
Current things NOT finished

These are the remaining pieces:

Duplicate username/email validation
More complete backend validation
Better error messages/pages
CSS/UI
More JavaScript enhancements

You specifically decided to leave the status-option backend validation for later.

For your local backup

Back up the entire project folder, especially:

project/
│
├── app.py
├── templates/
│   ├── Register.html
│   ├── Login.html
│   ├── Home.html
│   ├── addjob.html
│   ├── editjob.html
│   ├── profile.html
│   └── psw.html
│
├── .env
├── .gitignore   ← create before GitHub push
├── requirements.txt   ← create/update if needed
└── .venv/             ← local backup optional; don't push to GitHub

Also make a database backup separately. Your code backup and your Neon database/data backup are two different things.

Current roadmap
Display applications ✓
Application management table (Edit + Delete) ✓
Profile page ✓
Logout ✓
Validation / error handling ← CURRENT
CSS/UI
JavaScript enhancements
