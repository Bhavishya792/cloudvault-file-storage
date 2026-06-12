# CloudVault

CloudVault is a cloud-based file storage and version management platform built using Flask and AWS S3.

This project was developed as a personal project during my Cloud Computing Internship at CodeC Technologies.

## Author

Bhavishya Garg

## Features

- User Registration and Login
- Secure Password Hashing
- AWS S3 File Storage
- File Upload and Download
- File Version Management
- Secure Share Links
- Activity Tracking
- Search Functionality
- Responsive Dashboard UI

## Tech Stack

### Backend

- Flask
- SQLAlchemy
- Flask-Login
- Boto3

### Database

- SQLite

### Cloud Services

- AWS S3

### Frontend

- HTML
- CSS
- Jinja2

## Project Structure

```text
cloudvault/
│
├── app.py
├── models.py
├── s3_utils.py
├── requirements.txt
│
├── templates/
│
├── static/
│   ├── css/
│   └── js/
│
└── instance/
```

## Screenshots

### Home Page



### Login Page



### Dashboard



### Version History



### Share Link



## Setup Instructions

### Clone Repository

```bash
git clone REPOSITORY_URL
```

### Create Virtual Environment

```bash
python -m venv env
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create .env File

```env
SECRET_KEY=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=
AWS_BUCKET_NAME=
```

### Run Application

```bash
python app.py
```

## Future Improvements

- OAuth Authentication
- AWS Cognito Integration
- Storage Quotas
- File Preview Support
- Team Collaboration Features

## Internship Information

This project was developed by Bhavishya Garg as a personal project completed during the Cloud Computing Internship Program conducted by CodeC Technologies.