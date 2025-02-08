from selectors import SelectSelector

from github import Github
import pickle
import os.path

def save_repos():
    if Github().get_rate_limit().core.remaining != 0:
        try:
            user = Github().get_user("rubenxi")
            repos = user.get_repos()
            repos_local = []
            for repo in repos:
                if repo.fork is False:
                    repos_local.append([repo.name, repo.description, repo.html_url, repo.stargazers_count, repo.language, repo.get_readme()])
                    print(repo.get_readme().content)
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
