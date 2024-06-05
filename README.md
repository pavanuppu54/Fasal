# Django Movie Website 
[Visit the website](http://pavanuppu.pythonanywhere.com/)

## Description

This is a Django-based movie website that allows users to search for movies, create lists of movies (similar to YouTube playlists), and share those lists. Users can register, log in, and manage their movie lists. The application uses user authentication with email verification.


![image](https://github.com/pavanuppu54/Fasal/assets/110449636/78fafce7-98b6-47bf-af36-3c08dc2d200a)

## Features

1. **User Authentication**: Sign up and sign in functionalities with email verification for user authentication.
<img src="![image](https://github.com/pavanuppu54/Fasal/assets/110449636/35f7143f-cc16-4f74-8c26-6906104f2205)
" width="425"/> <img src="[image2.png](https://github.com/pavanuppu54/Fasal/assets/110449636/4433931d-e6c1-4744-87a2-51d3f852ccc8)" width="425"/> 


2. **Movie Search**: Users can search for movies using the OMDB API.
![image](https://github.com/pavanuppu54/Fasal/assets/110449636/2e3cb277-5db3-4702-8559-6f2b3db4c1f3)

3. **Movie Lists**: Users can create and manage lists of movies, which can be public or private.
 ![image](https://github.com/pavanuppu54/Fasal/assets/110449636/7007e607-67cb-4328-9f65-f9d7783f0ade)

4. **Nice Layout**: The search and list pages have a visually appealing layout inspired by other websites/applications.
![image](https://github.com/pavanuppu54/Fasal/assets/110449636/60aff4f4-57d0-4c26-894a-a3d882d573ea)

## OMDB API Integration
The application uses the OMDB API to fetch movie data. To use the OMDB API:

1. [Visit the OMDB API website.](http://www.omdbapi.com/)
2. Sign up with your email to generate an API key.
3. Add the API key to your settings.py file:
```
OMDB_API_KEY = 'your_api_key_here'
```
4. Use the API key in your application to make requests to the OMDB API for movie data.


## Steps to Run


1. Clone the repository.
```
git clone https://github.com/pavanuppu54/Fasal.git
```
2. Navigate to the project directory:
```
cd Fasal
```
3. Install dependencies:
```
pip install -r requirements.txt`
```
4. Apply migrations:
```
python manage.py migrate
```
5. Add your OMDB API key to the settings.py file:
```
OMDB_API_KEY = 'your_api_key_here'
```
6. Navigate to the project directory:
```
cd project/
```
7. Run the server:
```
python manage.py runserver
```
8. Access the application in your web browser at http://localhost:8000/.


## Contact
For any inquiries, please contact `pavanuppu54@gmail.com`.


