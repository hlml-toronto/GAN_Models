import instaloader
import os
download_dir = 'instagram_downloads'
# Create an instance of instaloader
L = instaloader.Instaloader(dirname_pattern=download_dir,download_videos=False,download_video_thumbnails=False,download_geotags=False,download_comments=False,save_metadata=False)

# Download all metadata and content associated with the specified hashtag
# Takes the first max_count results from Instagram's search function
L.download_hashtag('cat', max_count=3)
# Remove post text, which is also downloaded from the above code
dir_name = os.path.join(os.getcwd(), download_dir)
directory = os.listdir(dir_name)
for item in directory:
    if item.endswith(".txt"):
        os.remove(os.path.join(dir_name, item))