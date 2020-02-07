import discord
from discord.ext import commands, tasks

import random
from itertools import cycle

from creds import TOKEN



client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
	await client.change_presence(status=discord.Status.idle, activity=discord.Game('Hello there.'))
	change_status.start()
	print('Bot is online.')


@client.event
async def on_member_join(member):
	print(f'{member} has joined a server.')


@client.event
async def on_member_remover(member):
	print(f'{member} has left a server.')


@client.command()
async def ping(ctx):
	await ctx.send(f'Pong! {client.latency:.2}s')


@client.command(aliases=['8ball'])  # All of aliases can be used to run a command
# Every word after the command is used as a separate parameter.
# We use asterisk to treat it as a whole and put it to the last parameter.
async def _8ball(ctx, *, question):
	responses = [
		'It is certain',
		'Without a doubt',
		'Reply hazy try again',
		'Don’t count on it'
	]

	await ctx.send(f'Question: {question}\nAnser: {random.choice(responses)}')


@client.command()
async def clear(ctx, amount=5):
	await ctx.channel.purge(limit=amount+1)


@client.command()
@commands.has_permissions(manage_messages=True)
async def kick(ctx, member : discord.Member, *, reason=None):
	await member.kick(reason=reason)
	await ctx.send(f'Kicked {user.mention}')

@client.command()
async def ban(ctx, member : discord.Member, *, reason=None):
	await member.ban(reason=reason)
	await ctx.send(f'Banned {user.mention}')

@client.command()
async def unban(ctx, *, member):
	banned_users = await ctx.guild.bans()
	member_name, member_discriminator = member.split('#')

	for ban_entry in banned_users:
		user = ban_entry.user

		if (user.name, user.discriminator) == (member_name, member_discriminator):
			await ctx.guild.unban(user)
			await ctx.send(f'Unbanned {user.mention}')
			return


# Loops / background task
# We start a loop in on_ready
STATUS = cycle(['This is the first status!', 'The second status here.'])
# STATUS = cycle(['status1', 'status2'])
@tasks.loop(seconds=10)
async def change_status():
	await client.change_presence(activity=discord.Game(next(STATUS)))


# Errors
# One way of dealing with errors / more general
# If done this way only errors specify here will be triggered[!]
@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Please pass in all required arguments.')

	if isinstance(error, commands.CommandNotFound):
		await ctx.send('Invalid command.')

# Second way of dealing with errors / these are triggered first 
@clear.error
async def clear_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('Please specify an amount of messages to delete.')

@client.command()
async def clean(ctx, amount : int):
	await ctx.channel.purge(limit=amount)


# Custom checks
def is_it_me(ctx):
	return ctx.author.id == 333383838388383

@client.command()
@commands.check(is_it_me)
async def example(ctx):
	await ctx.send(f"Hi I'm {ctx.author}.")

client.run(TOKEN)