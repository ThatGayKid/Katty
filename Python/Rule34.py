from json import load as jsonload
import xmltodict,requests


JSON = jsonload(open('Text/Text.json'))
RecentPosts={}

def GetPost(ID:int,Tags:str) -> dict:
    try:
        with requests.get('https://rule34.xxx/index.php?page=dapi&s=post&q=index',params={'limit':'100','tags':Tags},timeout=5) as Get:
            Parsed = xmltodict.parse(Get.text)['posts']
    except requests.exceptions.Timeout:
        return JSON['Rule34']['Timeout']
    #If the count is bigger smaller than 2, fail
    if int(Parsed['@count']) < 2:
        return JSON['Rule34']['NoPosts']
    #Remove recent posts
    Parsed = Parsed['post']
    for Post in Parsed:
        if not(int(Post['@id']) in RecentPosts[ID]):
            RecentPosts[ID].append(int(Post['@id']))
            return Post
    return JSON['Rule34']['NoMorePost']

def Generate(ID:int,Tags:str) -> str:
    #If hasn't got a valid dictionary yet
    if ID not in RecentPosts.keys():
        RecentPosts[ID] = []
    #If the recent posts exceed the limit, pop the first value
    if len(RecentPosts[ID]) > 100:
        RecentPosts[ID].pop(0)
    #Get the entry
    return GetPost(ID,Tags)