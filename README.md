# Fitbit Collect
A script to collect Fitbit data from your Fitbit account.

If you own a Fitbit, your data is likely available in your online account. Fitbit offers an API so that you can retreive this data and analyse it yourself. This script runs through the steps needed to access the API

It makes use of the unofficial Fitbit client for Python https://github.com/orcasgit/python-fitbit

More details in my blog post https://davgibbs.com/how-to-get-fitbit-with-python/

## Steps
1. After "git clone" on this repo, start by creating a Python virtualenv (with a Python 3 version) and installing dependencies inside the directory:
```bash
    ./fitbit-collect$ virtualenv --python=/usr/bin/python3.6 venv
    ./fitbit-collect$ source venv/bin/activate
    (venv) ./fitbit-collect$ pip install -r requirements.txt
```

2. Next login to your Fitbit account and create a new application at the URL https://dev.fitbit.com/apps/new.
Fill in details in the form as appropriate. Many of the details are not too important, but ensure that the "OAuth 2.0 Application Type is "Personal" and that the callback URL is "http://127.0.0.1:8080/"
The callback URL will be used to receive the token and secret later on.

3. After completing the form your application "OAuth 2.0 Client ID" and "Client Secret" should be displayed.
OAuth 2.0 Client Id is 6 characters and Client Secret is 32 characters. Copy from the screen and place as arguments for the gather_keys_oauth2 python script:
```bash
    $ (venv) ./fitbit-collect$ python gather_keys_oauth2.py <oauth-client-id> <oauth-secret>
```
This script opens a new browser window. Look inside the script output for the URL that you need. Copy that link into your browser. The link is to confirm that you, as a user, want to give access to the your application to your data. Select all options and then "OK".

As part of the output of this script, two files are written to "client_details.json" and "user_details.json". These files will be used for accessing user data

4. Finally run the other script in the directory. This script will read the content of the two details files and query the Fitbit API:
```bash
    $ (venv) python run_collect.py
```
It will then add that data to the file "fitbit_results.json"

## Refreshing tokens
Automatically tokens expire after 8 hours. The Fitbit application handles this expiration but renewing the tokens and updating the user_details.json file. In this way, you will not have to authenticate again.

## API
Explore the Fitbit API here:
https://dev.fitbit.com/build/reference/web-api/explore/
The script can be updated in the method "_get_api_call" which has different examples of API calls for Steps, Sleep, etc

## Plotting data
The plot.py file uses Python's matplotlib to plot the json data
```bash
    $ (venv) python run_collect.py
```





