import requests


class QATrackAPIClient:
    """Simple client for communicating with the QATrack+ REST API."""

    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {token}",
            "Accept": "application/json",
        })

    def get(self, path: str):
        """GET a resource from the QATrack+ API."""

        if path.startswith("http://") or path.startswith("https://"):
            path = "/" + path.split("/", 3)[-1]

        url = f"{self.base_url}/{path.lstrip('/')}"

        response = self.session.get(url)
        response.raise_for_status()

        data = response.json()

        from pprint import pprint
        pprint(data)

        return data