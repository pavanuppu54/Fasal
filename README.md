# Django Movie Website

## Description

This is a Django-based movie website that allows users to search for movies, create lists of movies (similar to YouTube playlists), and share those lists. Users can register, log in, and manage their movie lists. The application uses user authentication with email verification.

![image](https://github.com/pavanuppu54/Fasal/assets/110449636/78fafce7-98b6-47bf-af36-3c08dc2d200a)

## Features

1. **User Authentication**: Sign up and sign in functionalities with email verification for user authentication.
![image](https://github.com/pavanuppu54/Fasal/assets/110449636/4433931d-e6c1-4744-87a2-51d3f852ccc8)

2. **Movie Search**: Users can search for movies using the OMDB API.
![image](https://github.com/pavanuppu54/Fasal/assets/110449636/2e3cb277-5db3-4702-8559-6f2b3db4c1f3)

3. **Movie Lists**: Users can create and manage lists of movies, which can be public or private.
4. ![image](https://github.com/pavanuppu54/Fasal/assets/110449636/7007e607-67cb-4328-9f65-f9d7783f0ade)

5. **Nice Layout**: The search and list pages have a visually appealing layout inspired by other websites/applications.
![image](https://github.com/pavanuppu54/Fasal/assets/110449636/60aff4f4-57d0-4c26-894a-a3d882d573ea)

6. **Feedback Form**: Provides a feedback form for users to submit feedback.
![image](https://github.com/pavanuppu54/Fasal/assets/110449636/55343369-9a64-4e03-abd5-ad58986df51a)

## Project Structure
Fasal/
│
├── app/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── templates/
│   ├── authentication/
│   │   ├── index.html
│   │   ├── signup.html
│   │   ├── signin.html
│   │   ├── activation_failed.html
│   │   └── email_confirmation.html
│   └── movies/
│       ├── home.html
│       ├── search.html
│       ├── create_list.html
│       └── view_list.html
│
├── movies/
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
│
├── project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── README.md


## Steps to Run

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Apply migrations: `python manage.py migrate`
4. Navigate to the project directory: `cd project/`
5. Run the server: `python manage.py runserver`
6. Access the application in your web browser at `http://localhost:8000/`


