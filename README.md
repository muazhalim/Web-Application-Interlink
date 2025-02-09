# Web Application: Interlink  

A **Flask-based web application** that provides user authentication, a social feed, friend connections, and a user profile system. The application supports many-to-many relationships and is designed with accessibility and usability in mind.

## Features  

- **User Authentication**: Sign up, log in, log out, and session management  
- **Social Feed**: Users can post and view content  
- **Friend System**: Send, accept, and decline friend requests  
- **Search & Profile Pages**: Search for users and view their profiles  
- **Database-Driven**: Uses SQLAlchemy for relational data management  
- **Flask-Login Integration**: Secure user sessions  
- **WCAG-Compliant Design**: Ensures accessibility and usability  

## Tech Stack  

- **Backend**: Flask, SQLAlchemy  
- **Frontend**: HTML, CSS, Bootstrap  
- **Database**: SQLite / PostgreSQL  
- **Authentication**: Flask-Login, Flask-WTF  

## How to Run Locally  

### 1. Clone the Repository  

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

### 2. Set Up a Virtual Environment  

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies  

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database  

```bash
flask db upgrade  # Ensure database migrations are applied
```

### 5. Run the Application  

```bash
flask run
```

Access the app in your browser at `http://127.0.0.1:5000/`.

## Example Usage  

### Sign Up  

1. Navigate to `/signup`  
2. Enter **username, email, and password**  
3. Log in to access the **social feed**  

### Social Feed  

- Create posts and view content from other users  
- Engage with friends through interactions  

### Friend Requests  

- Send and accept friend requests  
- View pending requests under **Notifications**  

## Future Improvements  

- Add **real-time notifications** using WebSockets  
- Implement **direct messaging** between users  
