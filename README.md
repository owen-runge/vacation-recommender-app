# vacation-recommender-app
This project contains a few main parts: a virtual environment, a backend (backend), and a frontend website (vacation-recommender). A virtual environment must be made for each new device running the code.

## Cloning project down to local
Since the frontend (vacation-recommender) itself is a git repository located within this repository, special care must be taken to make sure the entire project is cloned down to your local device. This can be achieved by running the following command:
```
$ git clone --recursive https://github.com/owen-runge/vacation-recommender-app.git
```
which clones both repositories. From there, everything can be installed and the website can be run.

## Create virtual environment
To create your virtual environment, ensure you are in the `vacation-recommender-app` directory. Then run the following commands, making sure you substitute `ENV_NAME` for the name you've chosen for your virtual environment:
```
$ python -m venv ENV_NAME
$ Set-ExecutionPolicy Unrestricted -Scope Process
$ ENV_NAME\Scripts\activate
$ pip install django
$ pip install django-rest-framework
$ pip install django-cors-headers
$ pip install pandas numpy seaborn matplotlib plotly scipy
$ pip install -U scikit-learn
```
## Start server and website
To start the server, ensure you are in the `vacation-recommender-app` directory and have your virtual environment activated. If not activated, activate your virtual environment by running:
```
$ Set-ExecutionPolicy Unrestricted -Scope Process
$ ENV_NAME\Scripts\activate
```
making sure again to substitute `ENV_NAME` with the name of your virtual environment.
Then run the following commands:
```
$ cd .\backend\
$ python manage.py runserver
```
From there, the backend api should be listening.

Note: instructions on how to install and run the frontend are located in that repository's README file.
