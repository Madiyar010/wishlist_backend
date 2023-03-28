# Wishlist backend
## Want to use this project?
Development
Uses the default Django development server.

1. Create two .env files, one should be in the core directory and another within the "wishlist" directory, 
populate them with the enviromental variables:
>DB_NAME 
DB_USER 
DB_PASSWORD 
DB_HOST 
DB_PORT 
EMAIL_FROM 
EMAIL_HOST_USER 
EMAIL_HOST_PASSWORD 

2. Build the images and run the containers:

>$ docker-compose up -d --build

Test it out at http://localhost:8000/swagger.
