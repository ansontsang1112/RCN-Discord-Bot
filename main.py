import discord
import mcs
from discord.ext import commands

# Vars
prefix = "$"
token = "ODQxODc4NjE2Nzg2MjA2NzIw.YJtKjw._y09ei-sBAGZyG8DVzEyCR79ExA"

bot = commands.Bot(command_prefix="$")


@bot.event
async def on_ready():
    print('目前登入身份：', bot.user)
    print('登入身份 ID：', bot.user.id)
    onActivity = discord.Game("RCN 系統中")

    await bot.change_presence(status=discord.Status.dnd, activity=onActivity)


@bot.command(name="ip")
async def getMinecraftServerIP(ctx):
    await ctx.channel.send("電腦版本入口: mc.resonancecraft.net \n手機版本入口: be.resonancecraft.net:58990")


@bot.command(name="myid")
async def getUserID(ctx):
    discordID = str(ctx.message.author)
    discordSystemID = str(ctx.message.author.id)
    await ctx.channel.send("你的 DiscordID 是 " + discordID + "\n你的帳號 ID 是 " + discordSystemID)


@bot.command(pass_context=True)
async def apply(ctx, args="null"):
    userID = ctx.message.author

    if args == "member":
        await ctx.channel.send("申請詳情已經成功私訊到你的 Discord 當中")
        await ctx.author.send("請填寫以下連結以完成會員申請：\nhttps://apps.hypernology.com/members/progress1.php?discordID=" + str(
            userID) + "&tpo=true")
    if args == "staff":
        await ctx.channel.send("職員申請暫時未開放，請稍後再提出申請！")
    else:
        await ctx.channel.send("請選擇你需要申請的類型：" + prefix + "apply member , " + prefix + "apply staff")


@bot.command(name="status")
async def serverStatus(ctx, args=""):
    stateCode, returnStatement = 0, ""
    if not mcs.serverAvailable(args):
        dataList = mcs.serverAvailable(args)
        stateCode = mcs.getServerStatus(dataList["ip"], int(dataList["port"]))

    if args == "":
        returnStatement = "請輸入伺服器名稱，新會市, HyperCity, MineLife City, 香港伊甸園, 伊織生存伺服器, 創造建築伺服器\n" + "例如：" + prefix + "status HyperCity"
    else:
        args = "會員大堂"

    if stateCode == 200:
        returnStatement = args + " 正處於上線狀態。"
    elif stateCode == 502:
        returnStatement = args + " 正處於下線狀態。"
    elif stateCode == 500:
        returnStatement = "伺服器狀態檢測出現故障，請稍後再試。"

    await ctx.channel.send(returnStatement)


bot.run(token)
