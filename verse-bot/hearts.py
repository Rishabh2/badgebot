from header import *
import time
import sqlite3

@client.event
async def on_ready():
  print('Logged in as')
  print(client.user.name)
  print(client.user.id)
  print(datetime.datetime.now())
  print('------')
  while True:
    await client.send_message(id_to_discorduser('142100044521144322'), '<:shark:416720236713345025>')
    time.sleep(1)




#client.run('MzY4MjA3OTA4MjU4NzA5NTA4.DVEzAw.5EcJ2rBPRcRi6RJeKCg96cdLUX0')
conn=sqlite3.connect('friendcodes.db')
c=conn.cursor()
swears = [
('202380877349650432', 1),
('227824927854559242', 1),
('282638912227115008', 4),
('178255522531639296', 1),
('179905636727914496', 1),
('281880295895203842', 1),
('242735447288053760', 1),
('103049236525887488', 3),
('109904754091524096', 1),
('287124726252437505', 1),
('360163090639224832', 1),
('343460386164441088', 1),
        ]
c.executemany('INSERT INTO swears VALUES (?,?)', swears)
conn.commit()
conn.close()
