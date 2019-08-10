import re
import asyncio
import discord # For Making Embeds
from firestore import db # For Handling Spam users
from difflib import SequenceMatcher
import json

config = json.load(open('./config.json', 'r'))

# Our Different Datasets
spam_dataset_file = open('./assets/spam.csv',encoding = 'ISO-8859-1')
spam_dataset = spam_dataset_file.read()

badwords_dataset_file = open('./assets/bad-words.csv',encoding = 'ISO-8859-1')
badwords_dataset = badwords_dataset_file.read()

# We will combine both the datasets and divide into two datasets one phrases and other words

spam_dataset = spam_dataset.split('\n') # Split at new lines
spam_dataset = map(lambda a: a.split(',')[:2], spam_dataset) # Split each line at comma
spam_dataset = filter(lambda a: a[0].lower() == 'spam', spam_dataset) # If first element is spam then data is spam
spam_dataset = map(lambda a: re.sub(r'([^\s\w]|_)+', '', a[1]).lower(), spam_dataset) # Only Alpha-numeric and lowercase
spam_dataset = list(spam_dataset) # Convert to list

badwords_dataset = badwords_dataset.split('\n')
badwords_dataset = map(lambda a: a.lower(), badwords_dataset)
badwords_dataset = list(badwords_dataset)

# raw dataset mix of both datasets, need to sort this
main_raw_dataset = badwords_dataset + spam_dataset

main_words_dataset = []
main_phrases_dataset = []

# sorts the array based on number of words
for data in main_raw_dataset:
  if (len(data.split(' ')) > 1): main_phrases_dataset.append(data)
  else: main_words_dataset.append(data)

# Checks string similarity
similarity = lambda a, b : SequenceMatcher(None, a, b).ratio()

# The IS SAFE FOR WORK Function
def isSFW(string):
  string = re.sub(r'([^\s\w]|_)+', '', string).lower()
  words = string.lower().split(' ')
  # First Check the words
  for word in words:
    for badword in main_words_dataset:
      # First Check for exact words
      if (word == badword): return False
      # Then Check for similar words
      if (similarity(word, badword) > 7.9): return False

  for phrase in main_phrases_dataset:
    # Then Check for exact phrases
    if (phrase in string): return False
    # Then Check for similar phrases
    if (len(phrase) < len(string)):
      # Iterate through each set of characters of phrase length 
      # And check their similarity with Phrase
      for i in range(len(string) - len(phrase)):
        substr = string[i:len(phrase) + i]
        if (similarity(phrase, substr) > 8.5): return False

  # If none found then
  return True

# Handle Discord Messages Command
async def handleDiscordSpam(message):
  # Check messages
  if not isSFW(message.clean_content): await spam_handle(message)
  # If embeds are there then them too
  if (len(message.embeds) > 0):
    for embed in message.embeds:
      title = embed.title
      description = embed.description
      fields = ' '.join(map(lambda a: a.name + ' ' + a.value, embed.fields))
      if not isSFW('{0} {1} {2}'.format(title, description, fields)):
        await spam_handle(message)

# Handle Discord Spam message
async def spam_handle(message):
  # Delete the message
  await message.delete()
  # Send Warning
  color = discord.Color.from_rgb(100, 100, 150)
  description = 'Your message seemed like a spam <@{0}>'.format(message.author.id)
  embed = discord.Embed(color= color, description= description)
  await message.channel.send(embed=embed)
  # Snowflakes are stored as ints in python so
  author_id = str(message.author.id)
  # Handle User
  # See if user has already spammed before
  user_ref = db.document('discord_spam_users/{0}'.format(author_id)).get()

  # If user exists increment spam counter
  if user_ref.exists: 
    user = user_ref.to_dict()
    user['spams'] += 1
    await handleTimeout(user, message)

  # If user doesnt exist create a new one
  else: 
    data = {
      u'id': author_id,
      u'username': message.author.name,
      u'spams': 1
    }
    await handleTimeout(data, message)

# Edits user also decrements spam
async def handleTimeout(user, message):
  # First add user
  db.collection(u'discord_spam_users').document(user['id']).set(user)
  user = db.document('discord_spam_users/{0}'.format(user['id'])).get().to_dict()
  # If counter is above 10 mute him and report to mod
  if user['spams'] > 10:
    if message.author.roles:
      role = message.guild.get_role(int(config['mute_role']))
      await message.author.add_roles(role)
      # Send warning embed
      color = discord.Color.from_rgb(200, 100, 150)
      description = '> <&{1}>, I muted <@{0}>'.format(str(message.author.id), config['mod_role'])
      embed = discord.Embed(color= color, description= description)
      await message.channel.send(embed=embed)
  # Else decrement his spams count after 10 minutes
  else:
    await asyncio.sleep(60)
    user['spams'] -= 1
    db.collection(u'discord_spam_users').document(user['id']).set(user)

# Tests
def test():
  print(isSFW('duck') == True)
  print(isSFW('fuck') == False)
  print(isSFW('fuuck')== False)
  print(isSFW('Hello how are you doing?') == True)
  print(isSFW('Hello wanat some nude pics of mine?') == False)
  print(isSFW('Want to sit on my dick?') == False)
  print(isSFW('Want to sit on my diick?') == False)  # This one doesnt pass :(
