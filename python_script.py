import requests
from bs4 import BeautifulSoup
import datetime

def get_site_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def get_deadline(content):
    deadline_tag = content.find("span", text="Son Başvuru Tarihi")
    if deadline_tag:
        deadline = deadline_tag.parent.find("span", class_="date").text
        deadline = datetime.datetime.strptime(deadline, "%d.%m.%Y")
        return deadline
    return None

def is_deadline_expired(deadline):
    today = datetime.datetime.today()
    return today > deadline

def get_expired_burses(site_url):
    soup = get_site_content(site_url)
    burslar = []
    for content in soup.find_all("div", class_="burs"):
        deadline = get_deadline(content)
        if deadline and is_deadline_expired(deadline):
            burslar.append({
                "baslik": content.find("h2").text,
                "aciklama": content.find("p").text,
                "son_basvuru_tarihi": deadline
            })
    return burslar

expired_burses = get_expired_burses("https://www.bursumcepte.com/")
for burs in expired_burses:
    print(burs)
