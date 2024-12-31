from github import Github,Auth
from dotenv import load_dotenv
import os


load_dotenv()
token=os.getenv('GITHUB_TOKEN')

def get_organisation(token):
    org=Auth.Token(token)
    git=Github(auth=org)
    gg=git.get_organization('Liebert-Industries-LLC')
    
    for repo in gg.get_projects():
        print(repo)
        
print(get_organisation(token=token))