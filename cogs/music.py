import disnake 
from disnake.utils import get
from disnake import FFmpegPCMAudio
from youtube_dl import YoutubeDL
from disnake.ext import commands


class main(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.players = {}


  def next_song(self, ctx, voice, source):
    queue = self.players[ctx.guild.id]
    queue.remove(source)
    if len(queue) == 0:
        self.players.pop(ctx.guild.id)
        return self.bot.dispatch("queue_end", ctx)
    next_source = queue[0]
    voice.play(next_source, after = lambda _: self.next_song(ctx, voice, next_source))
    return self.bot.dispatch("next_song", ctx)

  @commands.command()
  async def join(self, ctx):
      channel = ctx.message.author.voice.channel
      voice = get(self.bot.voice_clients, guild=ctx.guild)
      if voice and voice.is_connected():
          await voice.move_to(channel)
      else:
          voice = await channel.connect()


  @commands.command()
  async def play(self, ctx, url):
      YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
      FFMPEG_OPTIONS = {
          'before_options': '-reconnect 1 -reconnect_streamed 1  -reconnect_delay_max 5', 'options': '-vn'}
      voice = get(self.bot.voice_clients, guild=ctx.guild)

      with YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)

      URL = info['url']
      source = FFmpegPCMAudio(URL, **FFMPEG_OPTIONS)

      if not voice.is_playing():
          self.players[ctx.guild.id] = [source]
          voice.play(source, after = lambda _: self.next_song(ctx,voice, source))
          voice.is_playing()
          await ctx.send('Bot is playing')

      # check if the bot is already playing
      else:
          self.players[ctx.guild.id].append(source)
          await ctx.send(f"Song queued.")


# command to resume voice if it is paused
  @commands.command()
  async def resume(self, ctx):
      voice = get(self.bot.voice_clients, guild=ctx.guild)

      if not voice.is_playing():
          voice.resume()
          await ctx.send('Bot is resuming')


  # command to pause voice if it is playing
  @commands.command()
  async def pause(self, ctx):
      voice = get(self.bot.voice_clients, guild=ctx.guild)

      if voice.is_playing():
          voice.pause()
          await ctx.send('Bot has been paused')


  # command to stop voice
  @commands.command()
  async def stop(self, ctx):
      voice = get(self.bot.voice_clients, guild=ctx.guild)

      if voice.is_playing():
          voice.stop()
          await ctx.send('Stopping...')





def setup(bot):
	bot.add_cog(main(bot))