import json,random
import xmltodict,requests


JSON = json.load(open('Text/Text.json'))
RecentPosts = {}

def GetPost(ID:int,Tags:str) -> dict:
    url = 'https://rule34.xxx/index.php?page=dapi&s=post&q=index'
    Paramaters = {
        'limit' :'100',
        'tags'  : Tags}
    try:
        with requests.get(url,params=Paramaters,timeout=5) as Get:
            Parsed = xmltodict.parse(Get.text)['posts']
    except requests.exceptions.Timeout:
        return JSON['Rule34']['Timeout']
    #If the count is bigger smaller than 2, fail
    if int(Parsed['@count']) < 2:
        return JSON['Rule34']['NoPosts']
    #Remove recent posts
    Parsed = Parsed['post']
    Parsed.sort(key= lambda Key: Key['@score'])
    for Post in Parsed:
        if not(Post['@id'] in RecentPosts[ID]):
            return Post
    return random.choice(Parsed)

def Generate(ID:int,Tags:str) -> str:
    #If hasn't got a valid dictionary yet
    if ID not in RecentPosts.keys():
        RecentPosts[ID] = []
    #If the recent posts exceed the limit, pop the first value
    if len(RecentPosts[ID]) > 100:
        RecentPosts[ID].pop(0)
    #Get the entry
    Entry = GetPost(ID,Tags)
    if type(Entry) == dict:
        #Append the post id to the recent posts
        RecentPosts[ID].append(Entry['@id'])
    return Entry