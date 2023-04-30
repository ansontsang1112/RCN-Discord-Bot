# Author: Anson Tsang
from interactions import StatusType, PresenceActivityType, ClientPresence

import mcs
import interactions

# Vars
token = "OTg4NDUyMjQ4NjI5NzAyNzI3.G6e2RU.WTDTYmS-Svexs_QuTe7NSZD9s0M24_isFqjEhc"
welcome_channel_id = "440910838832955412"
guild_id = "440910838401073174"


bot = interactions.Client(command_prefix="$", token=token, intents=interactions.Intents.GUILD_MEMBERS)

@bot.event
async def on_start():
    print('RCN Discord Bot：機械人已經成功啟動')
    activity = interactions.PresenceActivity(name="ResonanceCraft Network", type=PresenceActivityType.LISTENING)
    await bot.change_presence(
        interactions.ClientPresence(
            status=StatusType.ONLINE,
            activities=[activity]
        )
    )


@bot.command(
    name="myid",
    description="獲取你的 Discord ID"
)
async def _myid(ctx: interactions.CommandContext):
    await ctx.send(f"<@{ctx.user.username}> 你的 DiscordID 是 " + str(ctx.user.id))


@bot.command(
    name="apply",
    description="申請 RCN 會員"
)
async def _apply(ctx: interactions.CommandContext):
    userID = ctx.user.id
    await ctx.send("申請詳情已經成功私訊到你的 Discord 當中")
    await ctx.user.send("請填寫以下連結以完成會員申請：\nhttps://apps.hypernology.com/members/progress1.php?discordID=" + str(userID) + "&tpo=true")


@bot.command(name="status")
async def serverStatus(ctx, args=""):
    stateCode, returnStatement = 0, ""
    dataList = mcs.serverAvailable(args)

    if args == "" and dataList["ip"] == "0.0.0.0":
        returnStatement = "**請輸入伺服器名稱 :globe_with_meridians:**```- HyperCity\n- 香港伊甸園\n- 伊織生存伺服器\n- 創造建築伺服器\n```" + "\n> 例如：/status HyperCity"
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


@bot.command(
    name="help",
    description="RCN 官方小助手"
)
async def _help(ctx: interactions.CommandContext):
    embed = interactions.Embed(title="ResonanceCraft 機械人", url="https://www.resonancecraft.net", description="協助您了解更多 RCN 社群資訊")
    embed.set_author(name="[RCN] 資訊科技委員會 | HyperNitePo. 協助製作")
    embed.add_field(name="/help", value="查詢 RCN 機械人指令", inline=False)
    embed.add_field(name="/myid", value="查詢自己的 Discord ID 及 帳號 ID", inline=False)
    embed.add_field(name="/apply", value="申請會員用途", inline=False)
    embed.set_footer(text="ResonanceCraft Network 機器人使用指南 | Member of HyperGroup")
    await ctx.send(embeds=embed)


@bot.event
async def on_guild_member_add(member: interactions.Member):
    def welcome_message(id):
        embed = interactions.Embed(title="歡迎登陸 ResonanceCraft Network", url="https://resonancecraft.net", description="屬於香港&台灣地區的「輔助性」託管組織")
        embed.set_author(name="ResonanceCraft Network 執行委員會")
        embed.add_field(name="", value=f"歡迎 <@{id}> 加入 ResonanceCraft Network！註冊成為會員，以享用更全面的服務吧~")
        embed.add_field(name="關於我們", value="RCN 隸屬於 Hyper Group，致力為用戶提供輔助性託管服務。現主要提供 Minecraft、Discord 機器人及網站託管。", inline=False)
        embed.add_field(name="申請服務", value="各位用戶須首先註冊成為 RCN 正式會員才能使用服務，透過 **/apply** 了解更多註冊資訊。完成註冊後，請開啟<#840288195320086588> 聯絡 RCN 幹事會", inline=False)
        embed.add_field(name="常用連結", value="[面板](https://panel.resonancecraft.net) [主網頁](https://resonancecraft.net) [會員系統](https://portal.resonancecraft.net)", inline=False)
        embed.set_footer(text="ResonanceCraft Network | 屬於香港&台灣地區的「輔助性」託管組織")
        return embed

    channel = await interactions.get(bot, interactions.Channel, object_id=welcome_channel_id)
    print(f'{member.id} has joined a server.')
    await member.send(embeds=welcome_message(member.id))   # Private DM
    await channel.send(embeds=welcome_message(member.id))  # Public Message


bot.start()
