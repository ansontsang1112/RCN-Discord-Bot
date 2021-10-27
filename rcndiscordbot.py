import discord
import mcs
from discord.ext import commands

# Vars
prefix = "$"
token = "token"

bot = commands.Bot(command_prefix="$")
bot.remove_command('help')

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
    bot.remove_command('help')
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
    dataList = mcs.serverAvailable(args)

    if args == "" and dataList["ip"] == "0.0.0.0":
        returnStatement = "**請輸入伺服器名稱 :globe_with_meridians:**```- 新會市\n- HyperCity\n- MineLifeCity\n- 香港伊甸園\n- 伊織生存伺服器\n- 創造建築伺服器\n```" + "\n> 例如：" + prefix + "status HyperCity"
    elif dataList["ip"] != "0.0.0.0" and dataList["ip"] != "127.0.0.1":
        stateCode = mcs.getServerStatus(dataList["ip"], int(dataList["port"]))
        if stateCode == 200:
            returnStatement = "> :globe_with_meridians: " + args + "\n> 狀態：上線 :o:"
        elif stateCode == 502:
            returnStatement = "> :globe_with_meridians: " + args + "\n> 狀態：下線 :x:"
        elif stateCode == 500:
            returnStatement = "> :globe_with_meridians: 伺服器狀態檢測出現故障，請稍後再試。 "
    else:
        returnStatement = "> :globe_with_meridians: 你所輸入的伺服器名稱並不存在於 RCN 聯網當中。"

    await ctx.channel.send(returnStatement)


@bot.command(name="help")
async def embedHelp(ctx):
    embed = discord.Embed(title="ResonanceCraft 機械人", url="https://www.resonancecraft.net",
                          description="協助您解決 RCN 問題及了解更多關於 RCN 的資訊")
    embed.set_author(name="[HN] 資訊科技部門")
    embed.add_field(name=prefix+"help", value="查詢 RCN 機械人指令", inline=False)
    embed.add_field(name=prefix+"ip", value="查詢 RCN Minecraft 聯網電腦版及手機版的登入 IP", inline=False)
    embed.add_field(name=prefix+"myid", value="查詢自己的 Discord ID 及 帳號 ID", inline=False)
    embed.add_field(name=prefix+"apply", value="用作申請職位或會員用途", inline=True)
    embed.add_field(name="member", value="申請成為 RCN 會員", inline=True)
    embed.add_field(name="staff", value="申請成為 RCN 職員", inline=True)
    embed.add_field(name=prefix+"status", value="查詢聯網伺服器的狀況", inline=True)
    embed.add_field(name="{servername}", value="輸入聯網伺服器名稱", inline=True)
    embed.set_footer(text="ResonanceCraft Network 機器人使用指南 | Member of HyperGroup")
    await ctx.send(embed=embed)

bot.run(token)
