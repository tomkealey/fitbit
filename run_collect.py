"""
Script to retrieve Fitbit data for the given user
"""
import json

from fitbit import Fitbit


FITBIT_API = 'https://api.fitbit.com'

CLIENT_DETAILS_FILE = 'client_details.json'  # configuration for for the client
USER_DETAILS_FILE = 'user_details.json'  # user details file

RESULT_FILE = 'fitbit_data.json'  # The place where we will place the results


def refresh_callback(token):
    """
    This method is only called when the authenticate token is out of date
    and a new token has been issued which needs to be stored somewhere for
    the next run
    param (token): A dictionary with the new details
    """
    print('CALLBACK: The token has been updated since last run')
    with open(USER_DETAILS_FILE, 'w') as f:
        json.dump(token, f)
    print('Successfully written update refresh token')


def _get_user_details():
    """
    The specific user that you want to retrieve data for.
    """
    with open(USER_DETAILS_FILE) as f:
        fitbit_user = json.load(f)
        access_token = fitbit_user['access_token']
        refresh_token = fitbit_user['refresh_token']
        expires_at = fitbit_user['expires_at']

    return access_token, refresh_token, expires_at


def _get_client_details():
    """The client is the application which requires access"""
    with open(CLIENT_DETAILS_FILE) as f:
        client_details = json.load(f)
        client_id = client_details['client_id']
        client_secret = client_details['client_secret']

    return client_id, client_secret


def _write_results(json_response):
    with open(RESULT_FILE, 'w') as f:
        json.dump(json_response, f)
    print(f'Successfully written result data to file {RESULT_FILE}')


def _get_api_call():
    """
    Date Api in this format:
    GET /<api-version>/user/<user-id>/<resource-path>/date/<base-date>/<end-date>.<response-format>
    <user-id> can be left as - to get the current user
    date format is '%Y-%m-%d' for example 2020-04-01
    Some examples below
    """
    # Steps in the last 7 days
    steps_last_seven_days = '/1/user/-/activities/log/steps/date/today/7d.json'
    # Steps between two dates
    steps_dates = '/1/user/-/activities/log/steps/date/2020-04-12/2020-04-18.json'
    # calories last 7 days
    calories_last_seven_days = '/1/user/-/activities/log/calories/date/today/7d.json'
    # profile info
    profile_info = '/1/user/-/profile.json'
    # Sleep between two dates
    sleep_dates = '/1.2/user/-/sleep/date/2020-04-17/2020-04-18.json'

    return steps_last_seven_days


def run():
    client_id, client_secret = _get_client_details()
    access_token, refresh_token, expires_at = _get_user_details()

    print(f'Running Fitbit request with details: {client_id} {client_secret}'
           ' {access_token} {refresh_token} {expires_at}')
    auth2_client = Fitbit(client_id, client_secret, oauth2=True,
                          access_token=access_token,
                          refresh_token=refresh_token, expires_at=expires_at,
                          refresh_cb=refresh_callback)

    fitbit_url = FITBIT_API + _get_api_call()
    json_response = auth2_client.make_request(fitbit_url)
    _write_results(json_response)


if __name__ == '__main__':
    run()
