from gtts import gTTS
from playsound3 import playsound
from bs4 import BeautifulSoup
import requests
import csv
import re
import inflect

DIV = "div"
CLASS = "class"
HREF = "href"
CLASS = "class"


def removeHtmlTags(returnedList):
    return [str(item.text.strip().replace('$', '')) for item in returnedList]


# NDTV is the Indian News Channel of choice
URL_INDIAN = "https://www.ndtv.com"
# Div of the top story
DIV_TOP_STORY_INDIAN = 'vjl-row vjl-row-hf1 mb-10 top-stories-8'
# Div of each top story
DIV_EACH_TOP_STORY_INDIAN = 'vjl-md-3b'

r = requests.get(URL_INDIAN)
soup = BeautifulSoup(r.content, 'html5lib')
# print(soup.prettify())

# Get the HTML of the top story div component
topStoriesLinksHtml = soup.find(DIV, attrs={DIV_TOP_STORY_INDIAN})
topStoryLinks = []
topStoryHeaders = []
#
# topStoryLinks = re.findall(r'(https?://[^\s]*)', str(topStories))
i = 0
output = ["Good Morning. Welcome to Today's News. Today we have highlights from"]

topStoryList = []

# print(topStoriesLinksHtml)
# #Gets the links of the top stories
for row in topStoriesLinksHtml.findAll(DIV, attrs={CLASS: DIV_EACH_TOP_STORY_INDIAN}):
    topStoryDict = {}
    topStoryDict["link"] = row.a[HREF]
    soup1 = BeautifulSoup(requests.get(topStoryDict["link"]).content, 'html5lib')
    topStoryDict["header"] = removeHtmlTags(soup1.findAll("h1", {"class": 'sp-ttl'}))
    topStoryDict["body"] = removeHtmlTags(soup1.findAll("p", {"class": None}))[:-2]
    topStoryList.append(topStoryDict)

output.append([item["header"] for item in topStoryList])

output.append("But first" + str(topStoryList[0]["header"]))

output.append([item["body"] for item in topStoryList])

tts = gTTS(str(output), tld='co.in', lang='en',  slow=False)
tts.save('hello.mp3')


