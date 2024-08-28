from airtable import fetch_reels_from_airtable, update_airtable_record, fetch_captions_from_airtable, fetch_tiktoks_from_airtable, update_airtable_record_tiktok
from googledrive import authenticate_drive_api, upload_file_to_drive, download_file_from_url, retrieve_drive_file_info, upload_creatomate_video_to_drive
from creatomate_func import babe_page_template, check_status
from slack_alert import send_slack_notification
from mirror import apply_mirror_video
from topaz import upscale_video
import itertools
import os
import io
import time

def main():
    service = authenticate_drive_api()
    # records = fetch_reels_from_airtable() # for when we want to take from sfc vault base
    records = fetch_tiktoks_from_airtable() # functin for fetching tiktoks from bp-source-scraper
    print(len(records))
    captions = fetch_captions_from_airtable()

    for record, caption_record in zip(records, itertools.cycle(captions)):
        download_url = record['fields']['DOWNLOAD URL']
        caption = caption_record['fields']['CAPTION']
        
        if not download_url:
            send_slack_notification(f"No download URL for record {record['id']}")
            continue

        try:
            # Attempt to download the video file from the provided URL
            file_ioo = download_file_from_url(download_url)
        except Exception as e:
            error_message = f"Failed to download file from URL {download_url} for record {record['id']}: {e}"
            send_slack_notification(error_message)
            print(error_message)
            continue  # Skip to the next record

        # Create an in-memory output buffer
        output_io = io.BytesIO()

        unique_id = record['fields']['UNIQUE ID']
        file_name_1 = "babe_" + str(unique_id) + "_mirror.mp4"

        try:
            # Apply the mirror effect and process the video
            apply_mirror_video(file_ioo, output_io)
            
            # Reset the buffer position to the beginning
            output_io.seek(0)
            
            # Upload the processed file to Google Drive
            webviewlink = upload_file_to_drive(service, output_io, file_name_1)
        except Exception as e:
            error_message = f"Failed to process or upload video for record {record['id']}: {e}"
            send_slack_notification(error_message)
            print(error_message)
            continue  # Skip to the next record

        time.sleep(20)

        try:
            # Send video to Creatomate and get the processed video URL
            creatomate_response = babe_page_template(webviewlink, caption)
        except Exception as e:
            error_message = f"Failed to process video with Creatomate for record {record['id']}: {e}"
            send_slack_notification(error_message)
            print(error_message)
            continue  # Skip to the next record

        time.sleep(60)

        if isinstance(creatomate_response, list) and len(creatomate_response) > 0:
            creatomate_response = creatomate_response[0]
        else:
            error_message = f"Invalid response from Creatomate for record {record['id']}"
            send_slack_notification(error_message)
            print(error_message)
            continue

        id = creatomate_response.get("id")
        status_json = None

        for attempt in range(3):
            status_json = check_status(id)
            if status_json.get("status") == 'succeeded':
                break
            time.sleep(60)
        
        if status_json.get("status") != 'succeeded':
            error_message = f"Creatomate did not return a successful status for record {record['id']} after 3 attempts. CM ID: {id}"
            send_slack_notification(error_message)
            print(error_message)
            continue

        creatomate_download_url = status_json.get('url')
        
        if not creatomate_download_url:
            error_message = f"Creatomate did not return a URL for record {record['id']}"
            send_slack_notification(error_message)
            print(error_message)
            continue

        try:
            # Download the video file from Creatomate URL
            creatomate_file_io = download_file_from_url(creatomate_download_url)
        except Exception as e:
            error_message = f"Failed to download processed video from Creatomate for record {record['id']}: {e}"
            send_slack_notification(error_message)
            print(error_message)
            continue  # Skip to the next record

        input_temp_path = f"temp_input_{record['fields']['UNIQUE ID']}.mp4"
        output_temp_path = f"temp_output_{record['fields']['UNIQUE ID']}.mp4"

        # Save the downloaded file to a temporary path
        with open(input_temp_path, 'wb') as temp_file:
            temp_file.write(creatomate_file_io.read())

        try:
            upscale_video(input_temp_path, output_temp_path)
            # Read the upscaled video back into a BytesIO object
            with open(output_temp_path, 'rb') as temp_file:
                file_io = io.BytesIO(temp_file.read())
        except Exception as e:
            error_message = f"Failed to upscale video for record {record['id']}: {e}"
            send_slack_notification(error_message)
            print(error_message)
            continue  # Skip to the next record
        finally:
            # Clean up the temporary files
            os.remove(input_temp_path)
            os.remove(output_temp_path)

        file_name_2 = "creatomate_4K_" + file_name_1
        
        try:
            file_id = upload_creatomate_video_to_drive(service, file_io, file_name_2)
            file_info = retrieve_drive_file_info(service, file_id)
        except Exception as e:
            error_message = f"Failed to upload Creatomate video {file_name_2} to Google Drive for record {record['id']}: {e}"
            send_slack_notification(error_message)
            print(error_message)
            continue  # Skip to the next record
        
        print(file_info)
        
        # Only update the Airtable record if the file was successfully uploaded
        if file_info and 'id' in file_info:
            try:
                # update_airtable_record(record['id']) # sfc vault reels
                update_airtable_record_tiktok(record['id']) # bp-source-scraper tiktok
            except Exception as e:
                error_message = f"Failed to update Airtable record {record['id']}: {e}"
                send_slack_notification(error_message)
                print(error_message)

if __name__ == "__main__":
    main()
