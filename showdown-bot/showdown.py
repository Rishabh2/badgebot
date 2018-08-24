import asyncio
import discord
import websockets
import time
import re
import os

showdown_name_reg=r'\|queryresponse\|userdetails\|{"userid":"(.*?)"'
showdown_battle_reg='(battle-gen7.*?)":'
showdown_inbattle_reg=r'>(battle-.*?)\n(.*)'
showdown_win_reg=r'>(battle-.*?-\d*).*\|win\|'
query = '|/cmd userdetails %s'
opps = ['thatdude9795', 'nuzboa']

async def send(websocket):
  await client.wait_until_ready()
  while not client.is_closed:
    for opp in opps:
      new_q = query % opp
      await websocket.send(new_q)
      await asyncio.sleep(30)

async def recieve(websocket):
  await client.wait_until_ready()
  current_battles = []
  while not client.is_closed:
    response = await websocket.recv()
    #Case 1: Recieved userdetails response
    name = re.search(showdown_name_reg, response)
    if name != None:
      name = name.group(1)
      matches = re.findall(showdown_battle_reg, response)
      for match in matches:
        entry = [name, match, '']
        if 'random' not in match and 'factory' not in match and all([(e[1] != match) for e in current_battles]):
          if len(current_battles) > 50:
            current_battles.pop()
          current_battles.append(entry)
          await websocket.send('|/join ' + match)
          await sendH2(name + ': https://play.pokemonshowdown.com/' + match)
    #Case 2: Recieve in-battle message
    battle = re.search(showdown_inbattle_reg, response, re.DOTALL)
    if battle != None:
      for i, _ in enumerate(current_battles):
        if current_battles[i][1]==battle.group(1):
          current_battles[i][2] += battle.group(2)
    #Case 3: Recieved battle end response
    battle = re.search(showdown_win_reg, response, re.DOTALL)
    if battle != None:
      battle = battle.group(1)
      for i, _ in enumerate(current_battles):
        if current_battles[i][1]==battle:
          writebattle(current_battles[i])
          await websocket.send('|/leave ' + battle)

async def sendH2(message):
  i=0
  h2=client.get_server('372042060913442818').get_member('242558859300831232')
  while i+1000<len(message):
    await client.send_message(h2, message[i:i+1000])
    i+=1000
  await client.send_message(h2, message[i:])

def writebattle(entry):
  fl = '/root/showdown-bot/battles/' + entry[0] + '/' + entry[1]
  if not os.path.exists(os.path.dirname(fl)):
    try:
      os.makedirs(os.path.dirname(fl))
    except:
      if exc.errno != errno.EEXIST:
        raise

  fo = open(fl, 'w')
  fo.write(entry[2])
  fo.close()

async def connect(future):
  websocket = await websockets.connect('ws://sim.smogon.com:8000/showdown/websocket')
  future.set_result(websocket)

client = discord.Client()
future = asyncio.Future()
asyncio.ensure_future(connect(future))
client.loop.run_until_complete(future)
websocket = future.result()
client.loop.create_task(send(websocket))
client.loop.create_task(recieve(websocket))
client.run('MzY4MjA3OTA4MjU4NzA5NTA4.DlZnfQ.7mAb9yTYOdT-w2NYl6ffd1uskBc')
