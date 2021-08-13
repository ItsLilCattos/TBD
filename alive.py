from flask import Flask
from threading import Thread
from discord.ext import tasks

app = Flask('')

@app.route('/')
def main():
    return "Your bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start() 

# nothing to loop over... leaving
# @tasks.loop(seconds=15) 
