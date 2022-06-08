import datetime
from hashlib import new
import discord
import json
import random
import os


print("--------------------------------------------------------")
print("開發者已獲得源代碼作者修改 | 發布許可 , 請勿修改 | 公開")
print("源代碼作者 :")
print("https://github.com/HansHans135")
print("--------------------------------------------------------")
print("源代碼 :")
print("https://github.com/HansHans135/sign")
print("--------------------------------------------------------")
print("開發者Discord :")
print("天然呆幻月#1314")
print("--------------------------------------------------------")
print("開發者Discord支援區 :")
print("https://discord.gg/3S5BgMTx47")
print("--------------------------------------------------------")


#設定
with open ("config.json",mode="r",encoding="utf-8") as filt:
    data = json.load(filt)
PREFIX = data["prefix"]
op_id = data["owner_id"]
TOKEN = data["token"]
MAX = data["max"]
MIN = data["min"]
NEW = data["new"]



client = discord.Client()

@client.event   
async def on_ready():
    print('BOT已上線，Botname：',client.user)
    status_w = discord.Status.online
    activity_w = discord.Activity(type=discord.ActivityType.watching, name=f"{PREFIX}help")
    await client.change_presence(status= status_w, activity=activity_w)

@client.event
async def on_message(message):
#help
    if message.content == f"{PREFIX}help":
        await message.delete()
        embed = discord.Embed(title="menu", description=f"prefix是{PREFIX}", color=0x04f108)
        embed.add_field(name=f"{PREFIX}help", value="指令功能查詢")
        embed.add_field(name=f"{PREFIX}new", value="創建帳號")
        embed.add_field(name=f"{PREFIX}sign", value="每日簽到(冷卻時間的計算為每天00:00重製)")
        embed.add_field(name=f"{PREFIX}me", value="查看您有多少錢")
        embed.add_field(name=f"{PREFIX}money <id>", value="查看別的用戶有多少金錢")
        embed.add_field(name=f"{PREFIX}give <id> <金額>", value="轉帳")
        embed.add_field(name=f"{PREFIX}set <id> <金額>", value="設定錢 [ 只限於DEV使用 ]")
        embed.add_field(name=f"{PREFIX}info", value="關於")
        await message.channel.send(content=None, embed=embed)
#info
    if message.content == f"{PREFIX}info":
        await message.delete()
        embed = discord.Embed(title="關於", description=f"前輟是{PREFIX}", color=0x04f108)
        embed.add_field(name="每次簽到最高", value=f"{MAX}$")
        embed.add_field(name="每次簽到最低", value=f"{MIN}$")
        embed.add_field(name="Bot支援區:", value="https://discord.gg/3S5BgMTx47")
        embed.add_field(name="關於此Bot:", value="開發者 : 天然呆幻月#1314 <@848164182334898216>")
        await message.channel.send(content=None, embed=embed)
#創建
    if message.content == f"{PREFIX}new":
      await message.delete()
      filepath = f"money/{message.author.id}.json"
      if os.path.isfile(filepath):
          await message.channel.send(f"{message.author.mention}您已經建立過帳號了!")
      else:
          with open (f"money/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
            data = {"last_time":"0","money":NEW}
            json.dump(data,filt)
            money = data['money']
          await message.channel.send(f"{message.author.mention}帳號建立完成,您目前有`{money}`元")

#簽到
    if message.content == f"{PREFIX}sign":
        await message.delete()
        await message.channel.send("查詢中 , 請稍等[不會太久]....")
        filepath = f"money/{message.author.id}.json"
        if os.path.isfile(filepath):
            today = datetime.date.today()
            with open (f"money/{message.author.id}.json",mode="r+",encoding="utf-8") as filt:
                data = json.load(filt)
                print(data['money'])
                last_time = data['last_time']
            if str(today) == str(last_time):
                await message.channel.send(f"{message.author.mention}您今天已簽到 , 明日再來")
            else:
                with open (f"money/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
                    data = json.load(filt)
                    print(data['money'])
                    upmoney = random.randrange(int(MIN),int(MAX))
                    newmoney = int(upmoney) + int(data['money'])
                data['money'] = newmoney
                with open (f"money/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
                data['last_time'] = str(today)
                with open (f"money/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
                await message.channel.send(f"{message.author.mention}本日簽到獎勵:`{upmoney}`元\n您目前有`{newmoney}`元")
        else:
            await message.channel.send(f"{message.author.mention}您沒有帳號,請建立帳號`{PREFIX}!new`創建一個")
#查詢
    if message.content == f"{PREFIX}me":
        with open (f"money/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
            data = json.load(filt)
        await message.channel.send(f"{message.author.mention}您目前有`{data['money']}`元")

    if message.content.startswith(f'{PREFIX}money'):
      await message.delete()
      tmp = message.content.split(" ",2)
      if len(tmp) == 1:
        await message.channel.send("未提供用戶ID")
      else:
        with open (f"money/{tmp[1]}.json",mode="r",encoding="utf-8") as filt:
            data = json.load(filt)
        await message.channel.send(f"{message.author.mention}您好 , 您查詢的使用者<@{tmp[1]}> `{tmp[1]}`他現在有`{data['money']}`元")
#set
    if message.content.startswith(f'{PREFIX}set'):
        if message.author.id == int(op_id):
          await message.delete()
          tmp = message.content.split(" ",2)
          崁入一 = tmp[1]
          tmp = message.content.split(f"{崁入一} ",2)
          崁入二 = tmp[1]
          #亨哥0126 | 天然呆幻月#1314
          if len(tmp) == 1:
            await message.channel.send(f"{PREFIX}set id 錢")
          else:
              filepath = f"money/{崁入一}.json"
              if os.path.isfile(filepath):
                with open (f"money/{崁入一}.json",mode="r",encoding="utf-8") as filt:
                    data = json.load(filt)
                data['money'] = int(崁入二)
                with open (f"money/{崁入一}.json",mode="w",encoding="utf-8") as filt:
                    json.dump(data,filt)
                with open (f"money/{崁入一}.json",mode="r",encoding="utf-8") as filt:
                    data = json.load(filt)
                await message.channel.send(f"已預設<@{崁入一}>`{崁入一}`用戶金錢設定為`{data['money']}`元")
              else:
                await message.channel.send(f"找不到使用者<@{崁入一}>`{崁入一}`的帳號")
        else:
            await message.channel.send(f"{message.author.mention}你沒有權限")
            
            
#give
    if message.content.startswith(f'{PREFIX}give'):
      await message.delete()
      tmp = message.content.split(" ",2)
      id = tmp[1]
      tmp = message.content.split(f"{id} ",2)
      money = tmp[1]
          #亨哥0126 | 天然呆幻月#1314
      if len(tmp) == 1:
        await message.channel.send(f"{PREFIX}give <id> <金額>")
      else:
          filepath = f"money/{id}.json"
          if os.path.isfile(filepath):
            with open (f"money/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
                if int(data["money"]) > int(money):
                    TO = int(data["money"]) - int(money) 
                    with open (f"money/{id}.json",mode="r",encoding="utf-8") as filt:
                        data = json.load(filt)
                    data['money'] = int(data["money"]) + int(money)
                    with open (f"money/{id}.json",mode="w",encoding="utf-8") as filt:
                        json.dump(data,filt)
                    with open (f"money/{message.author.id}.json",mode="r",encoding="utf-8") as filt:
                        data = json.load(filt)
                    data["money"] = int(TO)
                    with open (f"money/{message.author.id}.json",mode="w",encoding="utf-8") as filt:
                        json.dump(data,filt)
                    await message.channel.send(f"轉帳成功 , 您已經轉帳給[`{id}`] <@{id}>!")
                else:
                    await message.channel.send(f"{message.author.mention}您的錢不夠 , 無法轉帳")
          else:
            await message.channel.send(f"找不到使用者<@{id}>`{id}`的帳號")


#查別人
    if message.content.startswith(f'{PREFIX}money'):
      await message.delete()
      tmp = message.content.split(" ",2)
      if len(tmp) == 1:
        await message.channel.send("未提供用戶ID")
      else:
        filepath = f"money/{tmp[1]}.json"
        if os.path.isfile(filepath):
            with open (f"money/{tmp[1]}.json",mode="r",encoding="utf-8") as filt:
                data = json.load(filt)
            await message.channel.send(f"{message.author.mention}您好 , 您查詢的使用者<@{tmp[1]}>`{tmp[1]}`他現在有`{data['money']}`元")
        else:
            await message.channel.send("未找到這筆資料")

client.run(TOKEN)
