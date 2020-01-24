import discord
from discord.ext import commands

import random

from creds import TOKEN



client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
	print('Bot is ready.')


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


client.run(TOKEN)