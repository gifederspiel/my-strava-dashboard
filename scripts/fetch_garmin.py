import os
from garminconnect import Garmin

GARMIN_USERNAME = os.environ["GARMIN_USERNAME"]
GARMIN_PASSWORD = os.environ["GARMIN_PASSWORD"]

def main():
    client = Garmin(GARMIN_USERNAME, GARMIN_PASSWORD)
    client.login()

    # get last 5 activities
    activities = client.get_activities(0, 5)
    # for now, just print them
    for a in activities:
        print(f"{a['startTimeLocal']} - {a['activityName']} - {a.get('distance', 0)}m")

    # TODO: instead of print, push to Supabase / write JSON / commit file

if __name__ == "__main__":
    main()
