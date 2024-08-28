import requests
import os
from dotenv import load_dotenv

load_dotenv()

CREATOMATE_API_KEY = os.getenv("CREATOMATE_API_KEY")

def babe_page_template(video, caption):
  options = {
      'template_id': '3a9874ac-a45c-407f-bd0e-fa6ba9897f77',  # ig reels babe page template
      'modifications': {
          'fff4f28e-77cc-4cb9-8aa4-8ac413e69f88': caption,  # text
          'efc96171-ff37-4127-b731-d29771518697': video  # video
      },
  }

  response = requests.post(
      'https://api.creatomate.com/v1/renders',
      headers={
          'Authorization': f'Bearer {CREATOMATE_API_KEY}',
          'Content-Type': 'application/json',
      },
      json=options
  )

  if response.status_code != 200:
      print(f"Error: {response.status_code}")
      print(f"Response: {response.text}")
      response.raise_for_status()

  return response.json()

def check_status(id):
    response = requests.get(
        f'https://api.creatomate.com/v1/renders/{id}',
        headers={
            'Authorization': f'Bearer {CREATOMATE_API_KEY}',
            'Content-Type': 'application/json',
        }
    )

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(f"Response: {response.text}")
        response.raise_for_status()

    return response.json()

# if __name__ == "__main__":
#     id = 'eaa7b142-72c2-4527-a76f-c208f8c66228'
#     response = check_status(id)
#     print(response)