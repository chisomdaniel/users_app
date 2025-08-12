# Users App

The goal of this project is to build an end to end solution for user account management in any application. It is designed to be a stand alone app that can easily be integrated into any django project or microservice architecture based system with a few tweeks in its configuration depending on your expertise. It is designed to have the following features:

- [x] Custom User model and managers
- [x] Custom admin forms
- [x] User registration
- [x] User authentication
- [x] Email verification with otp
- [x] Email verification with link
- [x] Separate User profile model
- [x] User image upload
- [x] User account and profile update
- [x] User profile view
- [x] Password reset
- [x] User email notification on updates
- [x] Social auth with Google
- [x] Custom social adapter to manage custom user model on create
- [x] Documentation with swagger

#### Other backend services includes (optional updates, not included yet):
- Background processes to manage time heavy - task (sending email, compressing image)
- Caching
- Social auth with Facebook
- Send verification code with text message

### Technology
Built with **Django**, **Django rest framework**, **Django allauth**, **Django rest auth**, and other supporting packages.

### Setup
You can easily set this project up the usual way you'd setup a Django project.
- Download the repo
    ```
    git clone <repo link>
    ```
- Create a virtual environment
    ```
    python3 -m venv .venv
    ```
- Activate virtual environment
    ```
    source .venv/bin/activate
    ```
- setup dependencies
    ```
    pip install -r requirement.txt
    ```
- fill the example env file `env-example` and save it as `.env`
- Run test
    ```
    python3 manage.py test apps.accounts.tests
    ```
- Run on localhost
    ```
    python3 manage.py runserver
    ```
- View Swagger UI in browser at: `localhost:8000/api/schema/swagger/`

### Contribution
You are very much welcome to contribute to this project in any way you seem fit. You have a better way something can be implemented? go ahead, fork it and create a pull request. Want to add more interesting features? be my guest!!
