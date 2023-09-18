# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import xml.etree.ElementTree as ET
import csv
import os
from pytube import YouTube
from moviepy.editor import VideoFileClip, ImageClip
import ffmpeg



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def create_csv_from_yt(captions, path):
    # Initialize an array to store subtitle data
    subtitle_data = []
    for caption in captions:
        # Parse the XML caption data
        caption_data = ET.fromstring(caption.xml_captions)
        for p in caption_data.findall('.//p'):
            text_start = int(p.get('t', 0)) / 1000.0  # Convert milliseconds to seconds
            text_end = (int(p.get('t', 0)) + int(p.get('d', 0))) / 1000.0  # Convert milliseconds to seconds
            text = ''.join(s.text for s in p.findall('.//s'))
            # if text == '':
            #     continue
            subtitle_data.append({
                'text_start': text_start,
                'text_end': text_end,
                'text': text
            })
    # Create and write the CSV file
    csv_file_path = os.path.join(path, 'subtitles.csv')
    with open(csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = ['text_start', 'text_end', 'text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for subtitle in subtitle_data:
            writer.writerow(subtitle)

def get_fodler_name(videos_directory):
    # Get a list of subdirectories in the "videos" directory
    subdirectories = [d for d in os.listdir(videos_directory) if os.path.isdir(os.path.join(videos_directory, d))]
    if len(subdirectories) == 0:
        return '0-!_'

    # Initialize variables to keep track of the largest number and folder name
    largest_number = -1
    largest_folder_name = ""

    # Iterate through the subdirectories and find the largest number
    for folder_name in subdirectories:
        # Check if the folder name starts with a number followed by a hyphen and an exclamation mark
        if folder_name.startswith(('#', '!', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            parts = folder_name.split('-', 1)
            if len(parts) == 2:
                try:
                    # Extract the number from the folder name and convert it to an integer
                    number = int(parts[0])
                    if number > largest_number:
                        largest_number = number
                        largest_folder_name = folder_name
                except ValueError:
                    pass
    return str(largest_number+1)+'-!_'

def set_permissions(parent_folder_path, new_folder_path):
    try:
        # Create the new folder
        os.makedirs(new_folder_path, exist_ok=True)

        # Get the permissions of the root C:\ drive
        get_permissions_command = f'icacls C:\\'
        permissions_output = os.popen(get_permissions_command).read()

        # Apply the same permissions to the new folder
        set_permissions_command = f'icacls "{new_folder_path}" /inheritance:r /grant *S-1-5-32-545:(OI)(CI)F'
        os.system(set_permissions_command)
    except Exception as error:
        print('error')

def create_readme(path,video_url):
    # CREATE README WITH YOUTUBE URL
    with open(path + '\\link_video.txt', 'w') as readme_file:
        readme_file.write(f'YouTube Video URL: {video_url}')

def download_youtube(url, file_name = 'video', download_directory = '/videos', extension = '.mp4'):
    try:
        video_url = 'https://www.youtube.com/watch?v='+url
        yt = YouTube(video_url)
        # Choose the stream you want to download (e.g., highest resolution)
        stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
        # SET PATH
        script_directory = os.path.dirname(os.path.abspath(__file__))
        name_path = get_fodler_name(script_directory+'/videos')
        path = script_directory+'\\videos\\'+name_path+yt.title
        # DOWNLOAD VIDEO
        stream.download(output_path=path, filename=file_name+extension)
        # Create extra url and csv
        create_readme(path, video_url)
        captions = yt.captions.all()
        create_csv_from_yt(captions, path)

    except Exception as error:
        print('error')

def split_video(video_path, start_time, end_time):
    try:
        video_path+='\\video.mp4'
        video_path+='\\short.mp4'
        video = VideoFileClip(video_path)
        segment_1 = video.subclip(start_time, end_time)
        segment_1.write_videofile(video_path)
        #PER JUNTAR CLIPS EN UN PER ARA NO MINTERESA
        # final_video = clips_array([[segment_1]])  # Add more segments as needed
        # final_video.write_videofile(video_path+'\\short1.mp4')
        video.close()
    except Exception as error:
        print('error')

def time_splitter(video_path):
    try:
        return 443.16, 468.3
        return start_time, end_time
    except Exception as error:
        print('error')

def overlay_video(video_path):
    try:
        # Load the video
        video = VideoFileClip(video_path+'\\video.mp4')

        # Create a full-screen image clip
        image_clip = ImageClip(video_path+'\\image1.png', duration=2).set_duration(2).set_start(2)  # Set the duration to 2 seconds

        # Resize the image to match the video's dimensions
        # image_clip = image_clip.resize(height=video.h, width=video.w)

        # Overlay the image on the video for the desired duration
        video_with_overlay = video.set_duration(video.duration)  # Ensure the video duration matches
        video_with_overlay = video_with_overlay.set_pos('center')
        video_with_overlay = video_with_overlay.set_mask(image_clip)

        # Write the final video
        video_with_overlay.write_videofile(video_path+'\\final_video_with_image_overlay.mp4')

        # Close the clips
        video.close()
        image_clip.close()
    except Exception as error:
        print('error')


def overlay_video2(video_path):
    try:
        video_input_path = os.path.abspath('short.mp4')
        image_input_path = os.path.abspath('image1.png')
        output_path = os.path.abspath('final_video_with_overlay.mp4')
        # video_input_path = os.path.abspath(video_path + '\\short.mp4')
        # image_input_path = video_path + '\\image1.png'
        # output_path = video_path+'\\final_video_with_overlay.mp4'
        # ffmpeg_object = ffmpeg.filter([ffmpeg.input('short.mp4'), ffmpeg.input('image1.png')], 'overlay', 0, 0)
        # ffmpeg_object = ffmpeg_object.filter('enable', 'between(t, 2, 4)')

        # ffmpeg_object.output('test.mp4').run()
        # pass

        (
            ffmpeg
            .input(video_input_path)
            .output(output_path, vf='select=gte(t\,2)*lt(t\,4)+if(eq(n\,0)\,1\,ld(2))')
            .output(image_input_path)
            .run()
        )
        (
            ffmpeg
            .filter([ffmpeg.input(video_input_path), ffmpeg.input(image_input_path)], 'overlay', 100, 100)
            .output(output_path)
            .run()
        )


        # Paths to your video and image files

        # Output path for the final video with overlay
        # Define the input video and image streams
        # Define the input video and image streams
        input_video = ffmpeg.input(video_input_path)
        input_image = ffmpeg.input(image_input_path)


        #
        # Overlay the image on the video at the specified position (10:10)
        output = ffmpeg.output(input_video, input_image, vf='overlay=2:10', format='yuv420p', vcodec='libx264',
                               output_path=output_path, filename='potato', )

        # Run the FFmpeg command to create the final video with overlay
        ffmpeg.run(output)

        pass
        path_video = video_path+'\\video.mp4'
        path_png = video_path+'\\image.png'
        ffmpeg_object = ffmpeg.input(path_video)
        ffmpeg_object = ffmpeg_object.overlay(path_png, enable='between(t,4,7)')
        ffmpeg_object.output(video_path+'\\output.mp4').run()



    except Exception as error:
        print('error')



if __name__ == '__main__':
    # download_youtube('jZmAhusBK0U')
    start = end = 0
    start, end = time_splitter('sd')
    video_path = 'C:\\Users\\P21\\PycharmProjects\\Shorts_Land\\videos\\9-!_How to Create, Edit, and Post YouTube Shorts Automatically'
    video_path = 'C:\\Users\\P21\\PycharmProjects\\Shorts_Land\\videos\\9-!_How to Create, Edit, and Post YouTube Shorts Automatically'
    # split_video(video_path, start, end)
    overlay_video2(video_path)


    print_hi('PyCharm')

