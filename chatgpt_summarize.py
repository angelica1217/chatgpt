import requests
from bs4 import BeautifulSoup
import os
import openai

'''取得新聞稿內文'''
def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, "html.parser")
    else:
        print("Failed to retrieve the webpage.")
        return None

def print_texts(elements):
    texts = [element.text for element in elements]
    return '\n'.join(texts)

url = "https://www.ithome.com.tw/news/152373"
soup = get_soup(url)

if soup:
    header = soup.find("h1", class_="page-header") #找到文章標題
    summary = soup.select("div.content-summary p") #找到summary
    content = soup.select("div.field-items p") #找到文章內容

    header_text = print_texts([header])
    summary_text = print_texts(summary)
    content_text = print_texts(content)

    news = header_text + "\n\n" + summary_text + "\n\n" + content_text


'''把內容輸入至chatgpt api'''
keyfile = open("key.txt","r")
key = keyfile.readline()
openai.api_key = key

model_name = "gpt-3.5-turbo"

massage = {
    'role': 'user',
    'content': news + "\n\n請給我上述文章的總結"
}

response = openai.ChatCompletion.create(
    model = model_name,
    messages = [massage]
)

chatbot_response = response.choices[0].message['content']
print(chatbot_response)