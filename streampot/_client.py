import requests
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum, auto

@dataclass
class Asset:
    name: str
    url: str

class JobStatus(Enum):
    PENDING = auto()
    COMPLETED = auto()
    FAILED = auto()
    UPLOADING = auto()

@dataclass
class JobEntity:
    id: int
    status: JobStatus
    created_at: str
    assets: Optional[List[Asset]] = None

class StreamPotClient:
    def __init__(self, secret: str, base_url: str = 'https://api.streampot.io/v1'):
        self.secret = secret
        self.base_url = base_url
        self.actions = []

    def check_status(self, job_id: str) -> dict:
        response = requests.get(f"{self.base_url}/jobs/{job_id}", headers=self._auth_header())
        response.raise_for_status()
        return response.json()

    def run(self) -> JobEntity:
        response = requests.post(f"{self.base_url}/", headers=self._auth_header(json=True), json=self.actions)
        response.raise_for_status()
        
        job_data = response.json()
        job_data['status'] = JobStatus[job_data['status'].upper()]
        
        return JobEntity(**job_data)

    def _auth_header(self, json: bool = False) -> dict:
        headers = {"Authorization": f"Bearer {self.secret}"}
        if json:
            headers['Accept'] = 'application/json'
            headers['Content-Type'] = 'application/json'
        return headers

    def add_action(self, name: str, *values):
        self.actions.append({"name": name, "value": values})

    # All the actions methods

    def merge_add(self, source: str):
        self.add_action('mergeAdd', source)
        return self
    
    