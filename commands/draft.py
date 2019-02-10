from header import *
async def draft(message, args):
  DRAFT_FLAG = True # set to true while drafting

  if message.server.id == '372042060913442818':
    if len(message.mentions)==0:
      user = message.author
    else:
      user = getmention(message)
      args = args.split(maxsplit=1)[-1]
    userid = user.id
    cursor.execute(draft_select_str, (userid,))
    result = cursor.fetchone()
    if result == None:
      await client.send_message(message.channel, "User is not in the draft league")
      return
    sheet = SHEET_IDS[result[0]]
    mon_col = TEAM_COLS[result[1]]
    point_col = POINT_COLS[result[1]]

    if DRAFT_FLAG == False:
      rosterpage = service.spreadsheets().values().get(spreadsheetId=sheet, range='Rosters', majorDimension='COLUMNS').execute()
      values = rosterpage.get('values', [])
      roster = values[result[1]*3+2][:-1]
      labels = values[1][:-1]
      embed = discord.Embed(title="Draft Info", color=discord.Color(0x85bff8))
      for s in zip(labels, roster):
        if s[0] != '' and s[1] != '':
          embed.add_field(name=s[0], value=s[1])
      await client.send_message(message.channel, embed=embed)
      return

    # Get all the cells of pokemon tiers
    tiers = service.spreadsheets().values().get(spreadsheetId=sheet, range='Tiers', majorDimension='COLUMNS').execute()
    values = tiers.get('values', [])
    # Get all the currently drafted Pokemon
    drafted = service.spreadsheets().values().get(spreadsheetId=sheet,range='Rosters', majorDimension='COLUMNS').execute()
    mons = drafted.get('values', [])
    if args != 'Skip':
      for col in mons:
        if args in col:
          await client.send_message(message.channel, 'That pokemon has already been drafted')
          return
      found = False
      for i, tier in enumerate(values):
        if args in tier:
          tierLevel = values[i][0]
          cost = values[i+1][0][1:-1]
          msg = tierLevel + ' Cost: ' + cost
          found = True

          cellRow = tier.index(args)

          # Update Roster page
          # First, create a list of possible rows
          if 'M' in tierLevel: #If mon is mega
            rows = [13]
          else:
            if '1' in tierLevel:
              rows = [7]
            if '2' in tierLevel:
              rows = [8]
            if '3' in tierLevel:
              rows = [9,10]
            if '4' in tierLevel:
              rows = [11]
            if '5' in tierLevel:
              rows = [12]
            rows.extend([14, 15, 16, 17])
          # Now, find the first row in rows that isn't filled in
          for row in rows:
            roster =service.spreadsheets().values().get(spreadsheetId=sheet,range='Rosters!'+mon_col+str(row), majorDimension='COLUMNS').execute()
            roster = roster.get('values', [])
            if len(roster) == 0: # If the current cell is empty
              service.spreadsheets().values().update(spreadsheetId=sheet, range='Rosters!'+mon_col+str(row)+':'+point_col+str(row),
                  body={'majorDimension':'ROWS','values':[[args, None, cost]], 'range':'Rosters!'+mon_col+str(row)+':'+point_col+str(row)}, valueInputOption='USER_ENTERED').execute()
              # Next, add it to the draft column
              draftlist = service.spreadsheets().values().get(spreadsheetId=sheet,range='Draft!B2:B', majorDimension='COLUMNS').execute()
              draftcount = len(draftlist.get('values', [])[0]) + 2
              service.spreadsheets().values().update(spreadsheetId=sheet, range='Draft!B'+str(draftcount), body={'majorDimension':'ROWS', 'values':[[args]], 'range':'Draft!B'+str(draftcount)}, valueInputOption='USER_ENTERED').execute()
              strike = [{'updateCells':{
                'rows': [{
                  'values':[{
                    'userEnteredFormat': {
                      'textFormat':{
                        'strikethrough': True
                        }
                      }
                    }]
                  }],
                'fields': 'userEnteredFormat.textFormat.strikethrough',
                'range': {
                  'sheetId': 161954080, #Double check when updating
                  'startRowIndex': cellRow,
                  'endRowIndex': cellRow+1,
                  'startColumnIndex': i,
                  'endColumnIndex': i+1
                  }

                }}]
              body = {'requests':strike}
              response = service.spreadsheets().batchUpdate(spreadsheetId=sheet, body=body).execute()
              await client.send_message(message.channel, 'Done')
              return
    else:
      draftlist = service.spreadsheets().values().get(spreadsheetId=sheet,range='Draft!B2:B', majorDimension='COLUMNS').execute()
      draftcount = len(draftlist.get('values', [])[0]) + 2
      service.spreadsheets().values().update(spreadsheetId=sheet, range='Draft!B'+str(draftcount), body={'majorDimension':'ROWS', 'values':[[args]], 'range':'Draft!B'+str(draftcount)}, valueInputOption='USER_ENTERED').execute()
      await client.send_message(message.channel, 'Skipped')
      return
    msg = 'This is not a pokemon you can draft'
    await client.send_message(message.channel, msg)
