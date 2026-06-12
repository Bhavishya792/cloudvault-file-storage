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

<img width="1921" height="1811" alt="homepage" src="https://github.com/user-attachments/assets/c5865502-905b-4e47-b1eb-ace4d42d56bb" />


### Login Page

<img width="853" height="668" alt="image" src="https://github.com/user-attachments/assets/0db58ec0-7eeb-4001-acc9-2b9ef9dad450" />


### Dashboard

<img width="1921" height="1417" alt="dashboard" src="https://github.com/user-attachments/assets/1222c4f6-8424-4c7b-9285-3f8bbe7edb0e" />


### Version History

<img width="1921" height="895" alt="versions" src="https://github.com/user-attachments/assets/eba7ab0e-8f9d-45c4-8f4a-a0b19a778f7c" />


### Share Link

<img width="1911" height="883" alt="image" src="https://github.com/user-attachments/assets/a4efd85d-7584-4562-bf22-e9cb34a4fb0e" />


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
