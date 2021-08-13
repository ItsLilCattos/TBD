import discord
from discord.ext import tasks
from discord.ext import commands
import requests
import random
import os
from constants import PUNCH_IMAGES, HUG_IMAGES, KISS_IMAGES, CRY_IMAGES, RAGE_IMAGES, LAUGH_IMAGES, WAVE_IMAGES
from alive import keep_alive
from asyncio import sleep
from dotenv import load_dotenv
load_dotenv()

@tasks.loop(seconds=15)
async def ping_bot():
  requests.get('http://bot.itsuwuangie.repl.co')

#startup

client = commands.Bot(
    command_prefix=">"
) # hi

#This sets a prefix for the bot, > is the prefix for now


@client.event
async def on_ready():
  ping_bot.start()
  print(f'We have logged in as {client.user}')
  

@client.event
async def on_member_join(member):
    guild = member.guild
    welcome_channel = guild.get_channel(783616997980110854) # YOUR INTEGER CHANNEL ID HERE
    await welcome_channel.send(f'Welcome to the {guild.name} Discord Server, {member.mention} !  :partying_face:')
    await member.send(f'We are glad to have you in the {guild.name} Discord Server, {member.name} !  :partying_face:')


  
# Mod Commands


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):

	await member.kick(reason=reason)

	await ctx.channel.send(f'{member} has been kicked because {reason}')

	await member.send(
	    'You have been kicked from the server because: {}'.format(reason))

@client.command()
async def punch(ctx, member: discord.Member):
  """Punches a member."""

  embed = discord.Embed(title="", description=f"{member.mention} got slapped in the face by: {ctx.author.mention}!", color=0xffb101)
  img_url = random.choice(PUNCH_IMAGES)
  embed.set_image(url=img_url)
  await ctx.send(embed=embed)      

@client.command()
async def hug(ctx, member: discord.Member):
  """Hugs a member."""

  embed = discord.Embed(title="", description=f"{ctx.author.mention} hugged {member.mention}!", color=0xffb101)
  img_url = random.choice(HUG_IMAGES)
  embed.set_image(url=img_url)
  await ctx.send(embed=embed) 

@client.command()
async def wave(ctx, member: discord.Member):
  """Waves at a member."""

  embed = discord.Embed(title="", description=f"{ctx.author.mention} is waving at{member.mention}!", color=0xffb101)
  img_url = random.choice(WAVE_IMAGES)
  embed.set_image(url=img_url)
  await ctx.send(embed=embed) 


@client.command()
async def kiss(ctx, member: discord.Member):
  """Kisses a member."""

  embed = discord.Embed(title="", description=f"{ctx.author.mention} kissed {member.mention}!", color=0xffb101)
  img_url = random.choice(KISS_IMAGES)
  embed.set_image(url=img_url)
  await ctx.send(embed=embed) 


@client.command()
async def rage(ctx):
  embed = discord.Embed(title="", description="", color=0xffb101)
  img_url = random.choice(RAGE_IMAGES)
  embed.set_image(url=img_url)
  await ctx.send(embed=embed) 

@client.command()
async def cry(ctx):
  embed = discord.Embed(title="", description="", color=0xffb101)
  img_url = random.choice(CRY_IMAGES)
  embed.set_image(url=img_url)
  await ctx.send(embed=embed) 

@client.command()
async def laugh(ctx):
  embed = discord.Embed(title="", description="", color=0xffb101)
  img_url = random.choice(LAUGH_IMAGES)
  embed.set_image(url=img_url)
  await ctx.send(embed=embed) 



@client.command()
async def purge(ctx, amount: int):
	await ctx.channel.purge(limit=amount)
	await ctx.channel.send(f'{amount} messages have been deleted')


@client.command()
@commands.has_permissions(manage_channels=True)
async def warn(ctx, member: discord.Member, *, reason):
	await ctx.send('Member has been warned')
	await member.send('You have been warned because {}'.format(reason))


@commands.has_permissions(manage_roles=True, ban_members=True)
@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):

	try:
		await member.ban(reason=reason)
		await ctx.send(f'{member} has been given the ban hammer :hammer:')
		await member.send(
		    f"You have been banned in {ctx.guild}. Reason: {reason}")

	except:
		await ctx.send(f"{member} has been given the ban hammer :hammer:")
		await member.ban(reason=reason)


@client.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_disc = member.split('#')

	for banned_entry in banned_users:
		user = banned_entry.user

		if (user.name, user.discriminator) == (member_name, member_disc):
			await ctx.guild.unban(user)
			await ctx.channel.send(member_name + ' has been unbanned')
			print(ctx.author, 'unbanned', member_name)
			return

		await ctx.send(member + "was not found")


#slowmode

@client.command()
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, amount: int=0):
  if amount > 21600:
    return await ctx.send("You can't set the slowmode higher than 6 hours!")
    return 
  await ctx.channel.edit(slowmode_delay=amount)
  await ctx.send(f"slowmode has been set to {amount}")

# Utility Commands
@client.command()
async def verify(ctx):

	user = ctx.author
	guild = ctx.guild
	roleid = 817298408561049609
	role = discord.utils.get(guild.roles, id=roleid)

	if role in ctx.author.roles:
		await ctx.send("You are already verified!")
		return

	await user.add_roles(role)
	channel = await user.create_dm()
	await channel.send("You are verified in Angies server")


@client.command()
async def ping(ctx):
	time = client.latency * 1000
	await ctx.send(f'Pong! in `{time}`ms')


##### I will continue to work on this bot when i get invited to the test sorted


@client.command()
async def hello(ctx):
	await ctx.send('Hello!')


#Fun commands
@client.command()
async def say(ctx, *, cont):
  await ctx.message.delete() # to delete ur msg
  await ctx.send(cont)


#Fun commands

@client.command(name="8ball")
async def ball(ctx, qu):
	ansk = ["yes", "no", "nope", "yup"]
	ans = random.choice(ansk)
	await ctx.send(ans)


@client.command()
async def roll(ctx):

	dice = random.randint(1, 6)

	if dice == 1:

		e = discord.Embed(title=f"Dice rolled and showed number {dice}")

		e.set_image(
		    url=
		    "https://www.ssaurel.com/blog/wp-content/uploads/2017/05/dice_1.png"
		)

		await ctx.send(embed=e)

	else:

		if dice == 2:

			e = discord.Embed(title=f"Dice rolled and showed number {dice}")

			e.set_image(
			    url=
			    "https://www.ssaurel.com/blog/wp-content/uploads/2017/05/dice_2.png"
			)

			await ctx.send(embed=e)

		else:

			if dice == 3:

				e = discord.Embed(
				    title=f"Dice rolled and showed number {dice}")

				e.set_image(
				    url=
				    "https://www.ssaurel.com/blog/wp-content/uploads/2017/05/dice_3.png"
				)

				await ctx.send(embed=e)

			else:

				if dice == 4:

					e = discord.Embed(
					    title=f"Dice rolled and showed number {dice}")

					e.set_image(
					    url=
					    "https://www.ssaurel.com/blog/wp-content/uploads/2017/05/dice_4.png"
					)

					await ctx.send(embed=e)

				else:

					if dice == 5:

						e = discord.Embed(
						    title=f"Dice rolled and showed number {dice}")

						e.set_image(
						    url=
						    "https://www.ssaurel.com/blog/wp-content/uploads/2017/05/dice_5.png"
						)

						await ctx.send(embed=e)

					else:

						if dice == 6:

							e = discord.Embed(
							    title=f"Dice rolled and showed number {dice}")

							e.set_image(
							    url=
							    "https://www.ssaurel.com/blog/wp-content/uploads/2017/05/dice_6.png"
							)

							await ctx.send(embed=e)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        try:
            client.load_extension(f'cogs.{filename[:-3]}') # my cogs
        except Exception as e:
            raise e
        



client.run(os.environ.get('Token'))

## I made a .env because this repl.it project is public and other people would be able to see our token, but since i put it in a .env file noone will be able to see it

##okay thanks
