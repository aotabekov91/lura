import requests

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36", 
  }

def get_json(word):
    template=f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
    url=template.format(word=word)
    raw = requests.get(url, headers=header)
    if raw.status_code == 200: 
        return raw.content
