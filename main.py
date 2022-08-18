

import fortnitepy
import json
import os
import requests
from fortnitepy.ext import commands
import sched, time
import threading
import queue
import webbrowser
import sys
FORTNITE_API_BASE = 'https://fortnite-api.com'

class MyClient(fortnitepy.Client):
  # filename = "file:///"+os.getcwd()+"/index.html"
  # webbrowser.open_new_tab(filename)
  def __init__(self):
    if fortnitepy.errors.HTTPException:
      
      print("Error: Invalid Credentials")
      time.sleep(5)
      sys.exit(1)
    existing = self.get_device_auth()
    print (existing["email"])
    if existing["email"] == "":
      print("Email not found in config.json")
      time.sleep(5)
      sys.exit(1)
    if existing["password"] == "":
      print("Password not found in config.json")
      time.sleep(5)
      sys.exit(1)
    
    device_auth_details = self.get_device_auth().get(existing["email"], {})
    
    super().__init__(
    command_prefix=".",
    status = "Sub to Twin1 on YouTube",
    auth=fortnitepy.AdvancedAuth(
      email=existing["email"],
      password=existing["password"],
      prompt_authorization_code=True,
      prompt_code_if_invalid=True,
      delete_existing_device_auths=True,
      **device_auth_details
    ),
    )

  
  def get_device_auth(self):
    if os.path.isfile("config.json"):
      with open("config.json", 'r') as fp:
        return json.load(fp)
    return {}

  def store_device_auth(self, email, details):
    existing = self.get_device_auth()
    existing[email] = details

    with open("config.json", 'w') as fp:
      json.dump(existing, fp)
    
  async def event_device_auth_generate(self,details, email):
    self.store_device_auth(email, details)
  s = sched.scheduler(time.time, time.sleep)

   
  
      
  async def event_ready(self):
    print("Ready as")
    print(self.user.display_name)
  
  async def event_friend_request(self, request):
    await request.accept()
  
  async def event_party_invite(self, invite):
    await invite.accept()
  async def event_friend_message(self, message):
    

    split = message.content.split()
    command = split[0].lower()
    args = split[1:]
    joined_args = ' '.join(args)
    
    if command == "!skin":
      # converts the name of the skin to the id
      skin = requests.get(FORTNITE_API_BASE + "/v2/cosmetics/br/search?name=" + joined_args)
      try:
        jskon = skin.json()["data"]["id"]
      except:
          await message.reply("Skin not found")
          return

      # does the other stuff
      me = self.party.me

      await me.set_outfit(
        asset=jskon,
      )
      await message.reply("Skin set to " + joined_args)
    if command == "!emote":
      # converts the name of the emote to the id
      emote = requests.get(FORTNITE_API_BASE + "/v2/cosmetics/br/search?name=" + joined_args)
      try:
        jsemo = emote.json()["data"]["id"]
      except:
          await message.reply("Emote not found")
          return
    
      # does the other stuff
      me = self.party.me

      await me.set_emote(
        asset=jsemo,
      )
    
      
      await message.reply("Emote set to " + joined_args)
    if command == "!backpack":
      # converts the name of the backpack to the id
      backpack = requests.get(FORTNITE_API_BASE + "/v2/cosmetics/br/search?name=" + joined_args)
      try:
        jsbac = backpack.json()["data"]["id"]
      except:
          await message.reply("Backpack not found")
          return

      # does the other stuff
      me = self.party.me

      await me.set_backpack(
        asset=jsbac,
      )
      await message.reply("Backpack set to " + joined_args)
    if command == "!level":
      me = self.party.me

      await me.set_battlepass_info(
        has_purchased=True,
        level=int(joined_args),
      )
      await message.reply("Level set to " + joined_args)
    if command == "!skulltrooper":
      me = self.party.me
      variants = me.create_variant(
        clothing_color=1,
        

      )
      await me.set_outfit(
        asset="CID_030_Athena_Commando_M_Halloween",
        variants=variants,
      )
      




client = MyClient()
client.run()

    