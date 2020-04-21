# Fitbit Collect
A script to collect Fitbit data from your Fitbit account.

If you own a Fitbit, your data is likely available in your online account. Fitbit offers an API so that you can reteive this data and analyse it yourself. This script runs through the steps needed to access the API

It makes use of the unofficial Fitbit client for Python https://github.com/orcasgit/python-fitbit

## Steps
1. After "git clone" on this repo, start by creating a Python virtualenv and installing requirements inside the directory:
```bash
    $ virtualenv --python=/usr/bin/python3.6 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
```

2. Next login to your Fitbit account and create a new application at https://dev.fitbit.com/apps/new.
Fill in details in the form as appropriate. Ensure that the "OAuth 2.0 Application Type is "Personal" and that the callback URL is "http://127.0.0.1:8080/"
The callback URL will be used to receive the token and secret later on.

2. After completing the form your "OAuth 2.0 Client ID" and "Client Secret" should be displayed.
Copy them from screen and paste them into the file "client_details.template.json"
Then rename client_details.template.json to client_details.json
```bash
    $ mv client_details.template.json client_details.json
```

3. Next run the file "gather_keys_oauth2.py" from inside the virtualenv. Inside this file a cherrypi server is used to accepted the OAuth response from Fitbit:
```bash
    $ (venv) python gather_keys_oauth2.py <oauth-client-id> <oauth-secret>
```
This will print out the details to use. Copy them from the output content and into the file "user_details.template.json"
Then rename user_details.template.json to user_details.json
```bash
    $ mv user_details.template.json user_details.json
```

4. Finally run the other script in the directory. This script will read the content of the two details files and query the Fitbit API:
```bash
    $ (venv) python run_collect.py
```
It will then add that data to the file "fitbit_results.json"

## API
Explore the Fitbit API here:
https://dev.fitbit.com/build/reference/web-api/explore/
The script can be updated in the method "_get_api_call" which has different examples of API calls for Steps, Sleep, etc





