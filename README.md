# vacation-recommender-app
This project has a virtual environment (env), a backend (backend), and a frontend webiste (vacation-recommender)

## Start server and website
To start the server, make sure you are in the `vacation-recommender-app` directory. Then run the following commands:
```
$ Set-ExecutionPolicy Unrestricted -Scope Process
$ env\Scripts\activate
$ cd .\backend\
$ python manage.py runserver
```
From there, the backend api should be listening. \
Then, to start the website, make sure you are in the `vacation-recommender` directory. If you are currently in the `backend` directory, run:
```
$ cd ..
$ cd .\vacation-recommender\
```
to get to the correct directory. From there, to start the website, run:
```
$ npm install
$ npm run
```
and it should be up and running.
