import os
from typing import Iterable

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube"]

API_KEY = ''

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


class YoutubeAgent:
    def __init__(self):
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "client-secret.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_local_server(port=0)
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

    def get_videos_details(self, ids: Iterable[str]):
        request = self.youtube.videos().list(
            part="contentDetails",
            id=','.join(ids)
        )
        response = request.execute()
        return response
