import json
import requests
import praw
from azure.cosmos import CosmosClient
from numpy import random

#Special thanks to JEAN-CHRISTOPHE-CHOUINARD for this great article! https://www.jcchouinard.com/post-on-reddit-api-with-python-praw/

# Key references the topic of the subreddit, value represents the subreddit name
list_of_subreddits = {"*":"deals", 
                      "*":"amazonspecials", 
                      "Gaming":"GameDeals", 
                      "PC":"buildapcsales", 
                      "*":"blackfriday", 
                      "gaming":"steamdeals", 
                      "*":"DealsReddit",
                      "*":"DealsCouponsBargains",
                      "*":"DealsAndPromotions",}

#Takes in a json object corresponding to the deal that we want to post
#Returns a list of the subreddits which are relevant to post to 
def chooseSubreddit(deal):
    #returns a list of relevant subreddits
    return ["deals"]

# takes in the authentication object from cosmos db and returns the json representation
# of a random item from our database
def getItemFromDatabase(client):
    #we want to use the "products" container and choose a random item 
    database_name = 'dealsreddit'
    database = client.get_database_client(database_name)
    container_name = 'products'
    container = database.get_container_client(container_name)

    result = []
    #Create the query get all the items from products table
    for item in container.query_items(
        query = "Select * from products", enable_cross_partition_query=True):
        result.append(json.dumps(item))

    #select a random item from the table
    randomitem = random.randint(len(result))
    return result[randomitem]

def main():
    #first we need to read the credentials file to authenticate to both PRAW and Cosmos
    credentials = 'secrets.json'
    with open(credentials) as f:
        creds = json.load(f)

    #to authenticate with PRAW, we will use the praw.Reddit() function
    reddit = praw.Reddit(client_id=creds['client_id'],
                         client_secret = creds['client_secret'],
                         user_agent=creds['user_agent'],
                         redirect_uri=creds['redirect_uri'],
                         refresh_token=creds['refresh_token']
                         )
    # Get the deal from our database
    #to authenticate to cosmos, we wil use the CosmosClient function
    cosmos_client = CosmosClient(creds["cosmos_account_uri"], creds["cosmos_account_key"])  
    result = getItemFromDatabase(cosmos_client)
 
    #Making a post to each subreddit returned in the chooseSubreddit() function
    subnames = chooseSubreddit(result)

    #serialize the json object and access the necessary members for the post
    result = json.loads(result)
    productName = result["productName"]
    discountPercent = result["discountpercent"]
    discountPrice =  result["discountprice"]
    customURL = result["customURL"]

    # import pprint
    # for submission in reddit.subreddit("deals").hot(limit=2):
    #     sub = submission
    #     print(sub.title)
    #     pprint.pprint(vars(sub))
        

    #post in each sub
    for sub in subnames:
        subname = 'deals'
        subreddit = reddit.subreddit(sub)
        title = f"{discountPercent} off {productName} - {discountPrice}"
        selftext = f"{customURL}"
        print(title)
        flairid = "5e7115b4-872b-11e9-80d7-0e4143261286"
        #Submit the post
        subreddit.submit(title,url=selftext)
        #subreddit.submit(title,url=selftext,flair_id=flairid, flair_text="computers & electronics")

main()