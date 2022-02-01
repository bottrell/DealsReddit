import json
import requests
import praw

#Special thanks to JEAN-CHRISTOPHE-CHOUINARD for this great article! https://www.jcchouinard.com/post-on-reddit-api-with-python-praw/

def main():
    #first we need to read the credentials file
    credentials = 'secrets.json'
    with open(credentials) as f:
        creds = json.load(f);

    #to authenticate with PRAW, we will use the praw.Reddit() function
    reddit = praw.Reddit(client_id=creds['client_id'],
                         client_secret = creds['client_secret'],
                         user_agent=creds['user_agent'],
                         redirect_uri=creds['redirect_uri'],
                         refresh_token=creds['refresh_token']
                         )

    #Making a post to a subreddit
    subname = 'pythonsandlot'
    subreddit = reddit.subreddit(subname)
    title = "this is a test title!"
    selftext = '''this is a test body!'''

    #Submit the post
    subreddit.submit(title,selftext=selftext)

main()