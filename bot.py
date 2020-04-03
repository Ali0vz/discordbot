import discord
import random
import os

TOKEN = os.environ["discord_t"]
client = discord.Client()

manager = None
gld = None
chnl = None
on_vote = False
join = False
removeST = False
voteList = []
voters = []
players = []
addrole = []


@client.event
async def on_ready():
    print("is ready")


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global voters, chnl, gld, manager, on_vote, join, players, removeST, addrole, voteList
    if message.content.lower() == "help":
        await  message.channel.send("""کسی که این دستور را بزند مدیر بازی میشود   : mng
دستور های مدیر:
انصراف ازمدیریت :  nomng
افزودن بازیکن ها : join
پایان افزودن بازکن ها : nojoin
لیست بازیکن های بازی : players
افزودن نقش ها: addrole role role role role  
مثال : addrole mafia godfather dr karagah
دادن نقش ها به بازیکن ها به صورت رندوم : setrole
لیست بازیکن ها با ترتیب رندوم : rnd
شروع رای گیری : vote
پایان رای گیری : novote
نشان دادن آرا : showvote
افرادی که رای داده اند : voters
افرادی که رای نداده اند : novoters
حذف بازیکن : del
پایان بازی : endgame
دستور های بازیکن ها :
اضافه شدن به بازی : !
رای دادن : پس از شروع رای گیری نام فرد مورد نظر را به همراه ! در اول اسم به ربات دایرکت دهید
مثال: alivz!
""")
        return

    if message.content.lower() == 'mng' and not gld and message.guild:
        manager = message.author
        gld = message.guild
        chnl = message.channel
        st = str(manager)[0:str(manager).rfind("#")]
        await message.channel.send(f"مدیر بازی: {st}")
        return
    if (message.author.permissions_in(channel=message.channel).administrator or message.author == manager) and message.guild == gld and message.channel == chnl :
        if message.content.lower() == 'nomng':
            await chnl.send("مدیر از مدیریت انصراف داد")
            manager = None
            gld = None
            chnl = None
            return
    if message.author == manager and message.guild == gld and message.channel == chnl:
        if message.content.lower() == 'vote':
            voteList = []
            voters = []
            on_vote = True
            await chnl.send("""شروع رای گیری
نام فرد مورد نظر را به همراه ! در اول اسم به ربات دایرکت دهید
مثال: alivz!""")
            return
        if message.content.lower() == 'novote':
            on_vote = False
            await chnl.send("پایان رای گیری")
            return
        if message.content.lower() == "endgame":
            await chnl.send("اتمام بازی")
            on_vote = False
            voteList = []
            voters = []
            manager = None
            gld = None
            chnl = None
            players = []
            join = False
            removeST = False
            addrole = []
            return
        if message.content.lower() == "join":
            join = True
            await chnl.send("افرادی که میخواهند در بازی شرکت کنند ! بفرستند")
            return
        if message.content.lower() == "nojoin":
            join = False
            await chnl.send(f"تعداد بازیکن ها: {len(players)}")
            return
        if message.content.lower().find("addrole") == 0:
            roles = str(message.content)
            idx = roles.find("addrole") + 1
            roles = roles[idx:]
            idx = roles.find(" ")
            addrole.clear()
            while idx != -1:
                idx2 = roles.find(" ", idx + 1)
                if idx2 == -1:
                    idx2 = len(roles)
                if idx2 - idx > 1:
                    addrole.append(roles[idx + 1:idx2])
                roles = roles[idx2:]
                idx = roles.find(" ")
            seprator = " - "
            await chnl.send(f"نقش ها :\n {seprator.join(addrole)}")
            return
        if message.content.lower() == "players":
            rms = []
            for i in players:
                aut_str = str(i)
                rms.append(aut_str[0:aut_str.rfind("#")])
            seprator = "\n"
            await chnl.send(f"بازیکن ها:\n{seprator.join(rms)} ")
            return
        if message.content.lower() == "rnd":
            if len(players) > 1:
                rnList = []
                for i in players:
                    aut_str = str(i)
                    aut_str = aut_str[0: aut_str.rfind("#")]
                    rnList.append(aut_str)
                random.shuffle(rnList)
                seprator = "\n"
                await chnl.send("ترتیب رندوم : \n" + seprator.join(rnList))
            else:
                await chnl.send("تعداد بازیکن ها کم است")
                return
        if message.content.lower() == "setrole":
            setroles = []
            players_roles = []
            if len(addrole) <= len(players):
                for i in players:
                    setroles.append(i)
                for j in addrole:
                    rnd = random.randint(0, len(setroles) - 1)
                    dm = setroles[rnd]
                    del setroles[rnd]
                    try:
                        players_roles.append(str(dm)[0:str(dm).rfind("#")] + " : " + j)
                        if not dm.dm_channel:
                            await dm.create_dm()
                        await dm.send(j)
                    except:
                        chnl.send("خطا در فرستادن نقش برای : " + str(dm))
                        return
                dm = manager
                seprator = "\n"
                try:
                    if not dm.dm_channel:
                        await dm.create_dm()
                    await dm.send("نقش ها: \n" + seprator.join(players_roles))
                except:
                    chnl.send("خطا در فرستادن نقش برای : " + str(dm))
                finally:
                    return
            else:
                await chnl.send("تعداد نقش ها از تعداد بازیکن ها بیشتر است")
                return
        if message.content.lower() == "showvote":
            seprator = "\n"
            await chnl.send(seprator.join(voteList))
            return
        if message.content.lower() == "novoters":
            rms = []
            for i in players:
                if not (i in voters):
                    aut_str = str(i)
                    rms.append(aut_str[0:aut_str.rfind("#")])
            seprator = " , "
            await chnl.send(f"  افرادی که رای نداده اند:\n {seprator.join(rms)} ")
            return
        if message.content.lower() == "voters":
            rms = []
            for i in voters:
                aut_str = str(i)
                rms.append(aut_str[0:aut_str.rfind("#")])
            seprator = " , "
            await chnl.send(f"افرادی که رای داده اند:\n {seprator.join(rms)} ")
            return
        if message.content.lower() == "del":
            if len(players) == 0:
                await chnl.send("بازیکنی وجود ندارد")
                return
            removeST = True
            rms = []
            num = 1
            for i in players:
                aut_str = str(i)
                rms.append(str(num) + ". " + aut_str[0:aut_str.rfind("#")])
                num += 1
                seprator = " \n "
            await chnl.send("عدد بازیکن مورد نظر را بفرستید: \n" + seprator.join(rms))
            return
        if removeST:
            try:
                nt = int(message.content)
                aut_str = str(players[nt - 1])
                aut_str = aut_str[0:aut_str.rfind("#")]
                del players[nt - 1]
                await chnl.send("بازیکن" + aut_str + " از بازی حذف شد ")
                removeST = False
            except:
                await chnl.send(" دستور اشتباه ")
                removeST = False
            finally:
                return
    if join and message.content.lower() == "!" and message.channel == chnl:
        if message.author not in players:
            players.append(message.author)
        return
    if on_vote and (message.author in players or len(players) == 0) and message.channel != chnl and not (
            message.author in voters) and message.content.find("!") == 0:
        pers_vote = str(message.content)[1:]
        if pers_vote.replace(" ", "") == "":
            return
        voters.append(message.author)
        aut_str = str(message.author)
        voteList.append(f'{aut_str[0:aut_str.rfind("#")]} : {pers_vote}')
        remainings = len(players) - len(voteList)
        await chnl.send(f"{len(voteList)} رای")
        if remainings == 0:
            seprator = "\n"
            await chnl.send("پایان رای گیری")
            await chnl.send(seprator.join(voteList))
            on_vote = False
            voteList = []
            voters = []
        return


client.run(TOKEN)
