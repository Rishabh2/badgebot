from header import *
async def leaks(message, args):
  roles = message.server.roles
  for role in roles:
    if role.name=='Leaks':
      leak_role=role

  if any([role == leak_role for role in message.author.roles]):
    await client.remove_roles(message.author, leak_role)
  else:
    await client.add_roles(message.author, leak_role)
