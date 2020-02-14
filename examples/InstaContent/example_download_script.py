import instaloader

# Create an instance of instaloader
L = instaloader.Instaloader()

# Download all metadata and content associated with the specified hashtag
# Takes the first max_count results from Instagram's search function
L.download_hashtag('cat', max_count=30)