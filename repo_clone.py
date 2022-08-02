#!/usr/bin/python3

import os
import git
import yaml
import requests
from urllib.parse import urlparse

gh_user = os.environ.get('GH_USER')
gh_token = os.environ.get('GH_TOKEN')

gitlab_url = "lvashhdngitu1.bmwgroup.net"
gitlab_grp = "cacf"

repo_list = [{"url": "https://github.kyndryl.net/eu-hst/services.git", "branch": "master"}, 
        {"url": "https://github.kyndryl.net/Continuous-Engineering/ansible-project-gts-cm-tools.git", "branch": "v5.6"},
        {"url": "https://github.kyndryl.net/Continuous-Engineering/ansible-project-gts-cm-support-lite.git", "branch": "v5.6"},
        {"url": "https://github.kyndryl.net/Continuous-Engineering/ansible-project-gts-cm-calibration-migration.git", "branch": "v5.6"},
        {"url": "https://github.kyndryl.net/Continuous-Engineering/ansible-project-gts-cm-sonatype-nexus.git", "branch": "v5.6"},
        {"url": "https://github.kyndryl.net/Continuous-Engineering/ansible-project-gts-cm-mssql.git", "branch": "v5.6"},
        {"url": "https://github.kyndryl.net/Continuous-Engineering/ansible-project-gts-cm-windows.git", "branch": "v5.6"},
        {"url": "https://github.kyndryl.net/Continuous-Engineering/ansible-project-gts-cm-vcenter.git", "branch": "v5.6"},
        {"url": "https://github.kyndryl.net/Continuous-Engineering/ansible-project-gts-cm-esxi.git", "branch": "v5.6"},
        {"url": "https://github.kyndryl.net/Continuous-Engineering/ansible-project-gts-cm-sudo.git", "branch": "v5.6"},
        {"url": "https://github.kyndryl.net/Continuous-Engineering/ansible-project-gts-cm-linux.git", "branch": "v5.6"},
        {"url": "https://github.kyndryl.net/Continuous-Engineering/ansible-project-gts-cm-ssh.git", "branch": "v5.6"}]
#repo_list = [{"url": "https://github.kyndryl.net/Continuous-Engineering/ansible-project-gts-cm-ssh.git", "branch": "v5.6"}]

requests.get("https://github.kyndryl.net")

def get_repo(url, user, token, branch, path):
    path = path + "-" + branch
    repo_clone = git.Repo.clone_from('https://' + user + ':' + token + '@' + url.replace('https://',''), path, branch=branch )
    return repo_clone



def find_deps(name, path):
    results = []
    for root,dirs,files in os.walk(path):
        if name in files:
            results.append(os.path.join(root, name))
    return results


def update_deps(path):
    changed = False
    with open(path, "r") as fr:
        reqs = yaml.load(fr)

    for req in reqs:
        if "github.kyndryl.net" in req["src"]:
            if {"url": req["src"].replace("git+", ""), "branch": req["version"].replace("origin/","")} not in repo_list:
                repo_list.append({"url": req["src"].replace("git+", ""), "branch": req["version"].replace("origin/","")})
            req["src"] = "git+https://" + gitlab_url + ":" + gitlab_grp + "/" + os.path.basename(urlparse(req["src"]).path)
            changed = True

    if changed:
        with open(path, "w") as fw:
            for req in reqs:
                fw.writelines(["- name: " + req["name"] + "\n", "  src: " + req["src"] + "\n", "  version: " + req["version"] + "\n\n"])
    return changed



for repo in repo_list:
    print(repo['url'] + " - " + repo['branch'])
    repo_clone = get_repo(url=repo['url'], user=gh_user, token=gh_token, branch=repo["branch"], path=os.path.basename(urlparse(repo['url']).path))
    for req in find_deps('requirements.yml', repo_clone.working_dir):
        update_deps(req)
        repo_clone.index.add(req)
        repo_clone.index.commit("update kyn urls")
    new_remote = "git@" + gitlab_url + ":" + gitlab_grp + "/" + os.path.basename(urlparse(repo['url']).path)
    repo_clone.create_remote("gitlab", url=new_remote)
    repo_clone.remotes.gitlab.push(repo['branch'])
