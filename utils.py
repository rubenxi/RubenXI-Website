from github import Github
import pickle
import os.path
import requests
from lxml import html
import re
import base64
import pickle
from datetime import datetime
g = Github()

def save_repos():
    if g.get_rate_limit().core.remaining != 0:
        try:
            user = g.get_user("rubenxi")
            repos = user.get_repos()
            repos_local = []
            for repo in repos:
                if repo.fork is False:
                    url = 'https://raw.githubusercontent.com/rubenxi/' + repo.name + '/refs/heads/main/README.md'
                    response = requests.get(url)
                    readme = response.text
                    if "404: Not Found" == readme:
                        url = 'https://raw.githubusercontent.com/rubenxi/' + repo.name + '/refs/heads/master/README.md'
                        response = requests.get(url)
                        readme = response.text
                    if "404: Not Found" == readme:
                        readme = "No readme in this repo"
                    repos_local.append([repo.name, repo.description, repo.html_url, repo.stargazers_count, repo.language, readme])
        except Exception:
            print("Rate limit GitHub")
            pass
        with open('repos.pkl', 'wb') as f:
            pickle.dump(repos_local, f)
    else:
        print("Rate limit GitHub")

def get_repos_github():
    if os.path.exists('./repos.pkl'):
        with open('repos.pkl', 'rb') as f:
            repos_local = pickle.load(f)
            return repos_local
    else:
        return None

headers = {'User-Agent': 'Mozilla/5.0'}

def get_news(country_code, options_name_link):
    url = options_name_link[int(country_code)][2]
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tree = html.fromstring(response.content)
        news = []
        xpath_all = '/html/body/div[3]/div[6]/div[1]/div[2]/div[2]/div'
        news_size = tree.xpath(xpath_all)
        if len(news_size) <= 1:
            xpath_all = '/html/body/div[3]/div[5]/div[1]/div[2]/div[2]/div'
            news_size = tree.xpath(xpath_all)
        for i in range(1, len(news_size) + 1):
            time = tree.xpath(xpath_all + '[' + str(i) + ']/div[1]/span')
            title = tree.xpath(xpath_all + '[' + str(i) + ']/div[2]')
            link = tree.xpath(xpath_all + '[' + str(i) + ']/div[1]/div/a/@href')
            news.append([time[0].text_content(), title[0].text_content(), link[0]])
        return news

    else:
        return None

def get_coords(url_coords):
    lat = 0
    lon = 0
    response_coords = requests.get(url_coords, headers=headers)
    if response_coords.status_code == 200:
        tree_coords = html.fromstring(response_coords.content)
        xpath_all_coords = '//script/text()'
        scripts = tree_coords.xpath(xpath_all_coords)
        for script in scripts:
            if "zoom" in script:
                matches = re.findall(r'lat\s*=\s*([-]?\d+\.\d+);', script)
                lng_matches = re.findall(r'lng\s*=\s*([-]?\d+\.\d+);', script)
                if matches and lng_matches:
                    lat = float(matches[-1])
                    lon = float(lng_matches[-1])
                else:
                    print("No map location available")
    return [lat,lon]

def show_options():
    options_name_link = []
    url_options = 'https://liveuamap.com'
    response_options = requests.get(url_options, headers=headers)
    if response_options.status_code == 200:
        tree = html.fromstring(response_options.content)
        xpath_all = '/html/body/div[3]/div[3]/div/div'
        options_size = tree.xpath(xpath_all)
        for i in range(2, len(options_size) + 1):
            country_row = tree.xpath(xpath_all + '[' + str(i) + ']/div')
            for j in range(1, len(country_row) + 1):
                name = tree.xpath(xpath_all + '[' + str(i) + ']/div[' + str(j) + ']/a[2]/span')
                link = tree.xpath(xpath_all + '[' + str(i) + ']/div[' + str(j) + ']/a[2]/@href')
                if '#' not in link:
                    options_name_link.append((len(options_name_link) + 1, name[0].text_content(), link[0]))
    else:
        return None

    return options_name_link


def load_date(date_file):
    if os.path.exists(date_file):
        with open(date_file, "rb") as f:
            return pickle.load(f)
    return []


def save_date(date_today, date_file):
    with open(date_file, "wb") as f:
        pickle.dump(date_today, f)

def load_n(n_file):
    if os.path.exists(n_file):
        with open(n_file, "rb") as f:
            return pickle.load(f)
    return []


def save_n(n, n_file):
    with open(n_file, "wb") as f:
        pickle.dump(n, f)


save_repos()


