"""
Script to retrieve Fitbit data for the given user
"""
import json
import arrow
from datetime import date
import pandas as pd

from fitbit import Fitbit

FITBIT_API = 'https://api.fitbit.com'

CLIENT_DETAILS_FILE = './config/client_details.json'  # configuration for for the client
USER_DETAILS_FILE = './config/user_details.json'  # user details file

RESULT_FILE = './output/fitbit_data.json'  # The place where we will place the results

FIRST_RECORD = arrow.get("2019-06-01") # First Fitbit weigh-in
TODAY = arrow.get(date.today()) 

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
    sleep_dates = '/1.2/user/-/sleep/date/2020-04-13/2020-04-17.json'
    # Weight
    weight_dates = '/1/user/-/body/weight/date/2022-06-01/today.json'
    weight_series = '/1/user/-/body/log/weight/date/2022-07-01/2022-07-31.json'

    return weight_series
 
def _get_date_ranges():
    # Create a series of 30-day date-range tuples since FIRST_RECORD until TODAY
    date_ranges = []
    start_range = FIRST_RECORD
    
    while start_range < TODAY:
        if start_range.shift(days=30) < TODAY:
            date_ranges.append((start_range, start_range.shift(days=30)))
            start_range = start_range.shift(days=31)
        else:
            date_ranges.append((start_range, TODAY))
            start_range = TODAY
            
    return date_ranges

def _get_weight_series(client, date_ranges):
    weight_series = []

    for date_range in date_ranges:
        #print(f"Requesting data for {date_range[0].date()} to {date_range[1].date()}.")
        url = FITBIT_API + f"/1/user/-/body/log/weight/date/{date_range[0].year}-{date_range[0].month:02}-{date_range[0].day:02}/{date_range[1].year}-{date_range[1].month:02}-{date_range[1].day:02}.json"
        json_response = client.make_request(url)
        weight_series.append(json_response)

    return weight_series

def convert_weight (data):
  # lbs to kgs
  return round(data/2.205, 2)

def _get_weight_data(weight_series):
    weight_data = []

    for weigths in weight_series:
        for weight in weigths["weight"]:
            weight_data.append(dict(
                logId=weight["logId"],
                date=weight["date"],
                time=weight["time"],
                weight=convert_weight(weight["weight"]),
                fat=round(weight.get("fat", 0.00), 2),
                bmi=round(weight["bmi"],2)
            ))
    
    return pd.DataFrame(weight_data)

def run():
    client_id, client_secret = _get_client_details()
    access_token, refresh_token, expires_at = _get_user_details()

    #print(f'Running Fitbit request with details: {client_id} {client_secret}'
    #      f' {access_token} {refresh_token} {expires_at}')
    auth2_client = Fitbit(client_id, client_secret, oauth2=True,
                          access_token=access_token,
                          refresh_token=refresh_token, expires_at=expires_at,
                          refresh_cb=refresh_callback)
    
    # Sample run
    #fitbit_url = FITBIT_API + _get_api_call()
    #json_response = auth2_client.make_request(fitbit_url)
    #_write_results(json_response)

    # We wish to extract ALL recorded weights. As the 'Get Weight Time Series by Date Range' API
    # is limited to 30 days, we need to generate all of the 30 day periods between our 
    # ultimate date targets
    date_ranges = _get_date_ranges()
    weight_series = _get_weight_series(auth2_client, date_ranges)
    weight_data = _get_weight_data(weight_series)
    
    print("Total:", len(weight_data), "records")

    # Export your activities file as a csv 
    # to the folder you're running this script in
    weight_data.to_csv('./output/fitbit_records.csv')

if __name__ == '__main__':
    run()
