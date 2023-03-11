import discord
from discord.ext import commands, tasks
import feedparser
import aiohttp
import aiosqlite

class RSS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = "vote.db"

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_feeds.start()


    @tasks.loop(seconds=30)
    async def check_feeds(self):
        async with aiosqlite.connect(self.DB) as db:
            async with db.cursor() as cursor:
                await cursor.execute("""CREATE TABLE IF NOT EXISTS weltRSS(
                   id INTEGER PRIMARY KEY,
                   lastMessage TEXT)""")
                await db.commit()

                async with aiohttp.ClientSession() as session:
                    async with session.get("https://www.welt.de/feeds/latest.rss") as response:
                        data = await response.text()
                        feed = feedparser.parse(data)
                        last_entry = feed.entries[0]

                        try:
                            title = last_entry["title"]
                        except KeyError:
                            title = "No title"

                        try:
                            desc = last_entry["description"]
                        except KeyError:
                            desc = "No description"
                        try:
                            published = last_entry["published"]
                        except KeyError:
                            published = "No published date"

                        try:
                            category = last_entry["category"]
                        except KeyError:
                            category = "No category"

                        try:
                            author = last_entry["author"]
                        except KeyError:
                            author = "No author"

                        try:
                            link = last_entry["link"]
                        except KeyError:
                            link = "No Link"
                        try:
                            for content in last_entry["media_content"]:
                                if "image" in content["type"]:
                                    image = content["url"]
                                else:
                                    image = "No image"
                        except KeyError:
                            image = "No Image"

                        query = """SELECT lastMessage FROM weltRSS WHERE lastMessage = ?"""
                        await cursor.execute(query, (title,))
                        result = await cursor.fetchone()

                        if not result:
                            imagea = discord.Embed(color=discord.Color.embed_background())
                            imagea.set_image(url="https://cdn.discordapp.com/attachments/1064530429111189564/1084169270700806224/worldnews2.png")
                            embed = discord.Embed(
                                title=f"{title}",
                                url=f"{link}",
                                description=f"> {desc}"
                                            f"\n\n Bereitgestellt von [Welt.de](https://www.welt.de/feeds/latest.rss)",
                                color=discord.Color.embed_background(),
                                timestamp=discord.utils.utcnow()
                            )

                            if category == "No category":
                                pass
                            else:
                                embed.set_footer(text=f"{category}")

                            if image != "No Image":
                                embed.set_image(url=image)

                            channel = self.bot.get_channel(1084149314529534033) #Dein Welt-News Channel
                            message = await channel.send(embeds=[imagea, embed])
                            try:
                                await message.publish()
                            except:
                                pass
                            else:
                                query2 = """INSERT INTO weltRSS(lastMessage) VALUES(?)"""
                                await cursor.execute(query2, (title,))
                                await db.commit()
                        else:
                            return


def setup(bot):
    bot.add_cog(RSS(bot))
