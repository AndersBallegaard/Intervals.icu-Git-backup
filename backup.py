import requests
import os
import datetime


INTERVALS_ICU_BASE_URL = " https://intervals.icu"

# Use GITHUB_WORKSPACE if we are running as an action, otherwise use the current directory
WORKSPACE = os.environ.get('GITHUB_WORKSPACE', '.')
OUTPUT_DIR = os.environ.get('FIT_FILE_BACKUP_DIR', 'activities')
ACTIVITIES_DIR = os.path.join(WORKSPACE, OUTPUT_DIR)


class IntervalsAPI:
    def __init__(self, username, password, athleteid):
        self.username = username
        self.password = password
        self.athleteid = athleteid

    def getActivityDownload(self, activity_id):
        url = f"{INTERVALS_ICU_BASE_URL}/api/v1/activity/{activity_id}/fit-file"
        print(f"Downloading activity {activity_id} from {url}")
        response = requests.get(url, auth=(self.username, self.password))
        response.raise_for_status()
        return response.content
    
    def getLastActivities(self, days=2):
        iso6801_date = (datetime.datetime.now() - datetime.timedelta(days=days)).isoformat()
        url = f"{INTERVALS_ICU_BASE_URL}/api/v1/athlete/{self.athleteid}/activities?oldest={iso6801_date}"
        response = requests.get(url, auth=(self.username, self.password))
        id_list = [activity['id'] for activity in response.json()]
        return id_list
    
    def downloadLoop(self, days=2, output_dir="backups"):
        # check dir exists, and create if not
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        # download all activities in the last X days
        id_list = self.getLastActivities(days)

        # Filter out activities that have already been downloaded
        existing_files = os.listdir(output_dir)
        id_list = [activity_id for activity_id in id_list if f"{activity_id}.fit" not in existing_files]


        # download each activity and save to output_dir
        for activity_id in id_list:
            fit_file = self.getActivityDownload(activity_id)
            with open(f"{output_dir}/{activity_id}.fit", "wb") as f:
                f.write(fit_file)


if __name__ == "__main__":
    username = "API_KEY"
    
    # Get INTERVALS_API_KEY from environment variable
    password = os.environ.get('INTERVALS_API_KEY')

    if not password:
        raise ValueError("INTERVALS_API_KEY environment variable not set")
    
    # Get athleteID from enviroment
    athleteid = os.environ.get('INTERVALS_ATHLETE_ID')
    if not athleteid:
        raise ValueError("INTERVALS_ATHLETE_ID environment variable not set")
    
    intervals_api = IntervalsAPI(username, password, athleteid)

    intervals_api.downloadLoop(days=2, output_dir=ACTIVITIES_DIR)