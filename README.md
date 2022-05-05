# Structure of Networks Web

## Directions:

1. Run the server-side Flask app in one terminal window:

    ```sh
    $ cd server
    $ python3.9 -m venv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt
    (env)$ python app.py
    ```

2. Run the client-side Vue app in a different terminal window:

    ```sh
    $ cd client
    $ npm install
    $ npm run serve
    ```

    This will automatically serve content on localhost:8080
