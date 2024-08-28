import os
import requests

from config import (
    AIRTABLE_API_KEY,
    AIRTABLE_BASE_ID,
    AIRTABLE_REELS_TABLE,
    AIRTABLE_REELS_BABE_PAGE_TEMPLATE_VIEW,
    AIRTABLE_BASE_ID_2,
    AIRTABLE_CAPTIONS_TABLE,
    AIRTABLE_ACTIVE_CAPTIONS_VIEW,
    bp_source_scraper_base_id,
    videos_table,
    tiktok_videos_view
)

# obj oriented approach for consolidating these fetch functions
class AirtableClient:
    def __init__(self, base_id, api_key):
        self.base_id = base_id
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def fetch_records(self, table_name, view_name=None):
        # Construct the endpoint with or without the view parameter
        if view_name:
            endpoint = f"https://api.airtable.com/v0/{self.base_id}/{table_name}?view={view_name}"
        else:
            endpoint = f"https://api.airtable.com/v0/{self.base_id}/{table_name}"

        all_records = []
        offset = None

        while True:
            params = {}
            if offset:
                params['offset'] = offset
            response = requests.get(endpoint, headers=self.headers, params=params)
            data = response.json()
            all_records.extend(data['records'])

            if 'offset' in data:
                offset = data['offset']
            else:
                break

        return all_records

    def update_record(self, table_name, record_id, fields):
        url = f"https://api.airtable.com/v0/{self.base_id}/{table_name}/{record_id}"
        data = {"fields": fields}
        response = requests.patch(url, headers=self.headers, json=data)

        if response.status_code != 200:
            raise Exception(f"Failed to update Airtable record: {response.status_code}, {response.text}")

        return response.json()

def fetch_reels_from_airtable(): # sfc vault
    """
    this function is fetching instagram reel videos from our database: SFC VAULT

    this is a competitor analysis base, with only instagram reels in there

    this base has a lot of different instagram accounts in there, and the purpose
    was to analyse what our competition is posting

    """
    AIRTABLE_REELS_ENDPOINT = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_REELS_TABLE}?view={AIRTABLE_REELS_BABE_PAGE_TEMPLATE_VIEW}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    all_records = []
    offset = None

    while True:
        params = {}
        if offset: 
            params['offset'] = offset
        response = requests.get(AIRTABLE_REELS_ENDPOINT, headers=headers, params=params)
        data = response.json()
        all_records.extend(data['records'])
        
        if 'offset' in data:
            offset = data['offset']
        else:
            break

    return all_records

def update_airtable_record(record_id): # sfc vault
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_REELS_TABLE}/{record_id}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    fields = {
        "BABE PAGE TEMPLATE USED": True
    }
    data = {
        "fields": fields
    }
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update Airtable record: {response.status_code}, {response.text}")
    
    return response.json()

def fetch_captions_from_airtable():
    AIRTABLE_CAPTIONS_ENDPOINT = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID_2}/{AIRTABLE_CAPTIONS_TABLE}?view={AIRTABLE_ACTIVE_CAPTIONS_VIEW}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    all_records = []
    offset = None

    while True:
        params = {}
        if offset: 
            params['offset'] = offset
        response = requests.get(AIRTABLE_CAPTIONS_ENDPOINT, headers=headers, params=params)
        data = response.json()
        all_records.extend(data['records'])
        
        if 'offset' in data:
            offset = data['offset']
        else:
            break

    return all_records

def fetch_tiktoks_from_airtable():
    """
    this function is fetching tiktok videos from database: bp-source-scraper

    """
    airtable_tiktok_videos = f"https://api.airtable.com/v0/{bp_source_scraper_base_id}/{videos_table}?view={tiktok_videos_view}"
    headers = {"Authorization": f"Bearer {AIRTABLE_API_KEY}"}
    all_records = []
    offset = None

    while True:
        params = {}
        if offset: 
            params['offset'] = offset
        response = requests.get(airtable_tiktok_videos, headers=headers, params=params)
        data = response.json()
        all_records.extend(data['records'])
        
        if 'offset' in data:
            offset = data['offset']
        else:
            break

    return all_records

def update_airtable_record_tiktok(record_id): # sfc vault
    url = f"https://api.airtable.com/v0/{bp_source_scraper_base_id}/{videos_table}/{record_id}"
    headers = {
        "Authorization": f"Bearer {AIRTABLE_API_KEY}",
        "Content-Type": "application/json"
    }
    fields = {
        "BABE PAGE TEMPLATE USED": True
    }
    data = {
        "fields": fields
    }
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code != 200:
        raise Exception(f"Failed to update Airtable record: {response.status_code}, {response.text}")
    
    return response.json()