import requests
import json
import feedparser
import sqlite3
import time

_version = "0.1-krabbetein"

# webhook setup
username = 'PUBG News'
id = ''
token = ''

# sqlite3 setup
conn = sqlite3.connect('pubg.db')
c = conn.cursor()
try:
   c.execute('''CREATE TABLE news (id)''')
except sqlite3.OperationalError:
   print("sqlite table already exists")

class Webhook:
   def __init__(self, id, token, username):
      self.hookId = id
      self.token = token
      self.url = "https://discordapp.com/api/webhooks/"+self.hookId+"/"+self.token 
      self.headers = {
        'user-agent': 'pubg-webhook '+_version,
        'content-type': 'application/x-www-form-urlencoded'
      }
      self.username = username

   def webhook(self, message):
      w = {}
      w['content'] = message
      w['username'] = self.username
      r = requests.post(self.url, headers=self.headers, data=json.dumps(w))

   def checkForum(self, url):
      pubg_news = feedparser.parse(url)
      
      # check 5 last news
      n = 5
      for x in range(0, n):
         entry = pubg_news['entries'][x]['link']
         id = pubg_news['entries'][x]['id']
         c.execute('SELECT id FROM news WHERE id = ?', (id,))
         data = c.fetchone()
         if(data is None):
            self.webhook(entry)
            c.execute('INSERT INTO news VALUES (?)', (id,))
            conn.commit()
         time.sleep(3)

   def run(self):
      self.checkForum('https://forums.playbattlegrounds.com/forum/5-news-announcements.xml/')
      self.checkForum('https://forums.playbattlegrounds.com/forum/205-patch-notes-known-issues.xml/')

# run
def main():
   w = Webhook(id, token, username)
   w.run()

if __name__ == '__main__':
   if(token and id):
      main()
   else:
      print("Please add tokenid and/or id to bot.py")