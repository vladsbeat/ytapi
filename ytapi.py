import os
import json
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re

# Function to extract video ID from YouTube URL
def get_video_id(youtube_url):
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', youtube_url)
    if not video_id_match:
        raise ValueError('Invalid YouTube URL')
    return video_id_match.group(1)

# Function to get the transcript
def get_transcript(youtube_url):
    video_id = get_video_id(youtube_url)
    
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
        # Concatenate all text entries into one block of text
        full_transcript = ' '.join([entry['text'] for entry in transcript_list])
        return full_transcript
    except (TranscriptsDisabled, NoTranscriptFound):
        raise ValueError('Transcript not available for this video')

# Main execution
if __name__ == '__main__':
    # Read the input data from the default INPUT key
    with open(os.getenv('APIFY_INPUT_PATH'), 'r') as input_file:
        input_data = json.load(input_file)
    youtube_url = input_data.get('youtubeUrl')
    
    if not youtube_url:
        output = {'error': 'No YouTube URL provided'}
    else:
        try:
            transcript = get_transcript(youtube_url)
            output = {'transcript': transcript}
        except ValueError as e:
            output = {'error': str(e)}

    # Write the output to the default OUTPUT key
    with open(os.getenv('APIFY_OUTPUT_PATH'), 'w') as output_file:
        json.dump(output, output_file)
