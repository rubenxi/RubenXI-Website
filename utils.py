from github import Github
import pickle
import os.path
import requests

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
            print("Rate limit")
            pass
        with open('repos.pkl', 'wb') as f:
            pickle.dump(repos_local, f)
    else:
        print("Rate limit")

def get_repos_github():
    if os.path.exists('./repos.pkl'):
        with open('repos.pkl', 'rb') as f:
            repos_local = pickle.load(f)
            return repos_local
    else:
        return None

save_repos()
