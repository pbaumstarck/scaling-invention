"""A simple Discord bot that responds to programming prompts.

= Permutations =
$ permute 1 2 3 4
> 1 2 4 3
"""

import discord
import os
import re

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.all()
client = discord.Client(intents=intents)


def split_iterable(str):
  """Split a string into spaced or comma-separated elements."""
  return [_.strip() for _ in re.split(r'(\s*\,\s*|\s+)', str) if _.strip()]


def permute(body):
  """Permute the items listed in the `body` string.

  Args:
    body: A string such as "1 2 3 4".

  Returns:
  Permuted string such as "1 2 4 3".
  """
  if not body:
    return '<no items to permute>'

  items = list(map(int, split_iterable(body)))

  # Anchoring from the rightmost index, find the stretch of monotonically increasing numbers.
  right = len(items) - 1
  left = right
  while left > 0 and items[left - 1] > items[left]:
    left -= 1

  # TODO: Possibly simplify this.
  if left == right:
    # This element is bigger than all, so just swap it with the next in.
    new_items = items[:-2] + [items[-1], items[-2]]
  elif left == 0:
    # All elements are sorted in descending or, so reverse them to restart the permutation.
    new_items = list(reversed(items))
  else:
    # Place the next largest element out front then restart the rest of the elements sorted.
    # E.g., 1 2 4 3 => 1 3 2 4
    new_item = items[left - 1]
    shuffle_items = items[left - 1:]
    greater_items = [_ for _ in items[left:] if _ > new_item]
    new_pivot_item = min(greater_items)
    new_items = items[:left - 1] + [new_pivot_item] + list(sorted(_ for _ in shuffle_items if _ != new_pivot_item))

  return ' '.join(map(str, new_items))


def process_command(command):
  """Processes a Discord command."""
  command = command.strip()

  COMMANDS = {
    'permute': permute,
  }
  for keyword, func in COMMANDS.items():
    if command.startswith(keyword):
      return func(command[len(keyword):].strip())

  return 'Unknown command "%s"' % command


if True:
  # Test the permutation first.
  # TODO: Convert this into a unit test.
  items = '1 2 3 4'
  for i in range(24):
    new_items = process_command('permute %s' % items)
    print(items, '->', new_items)
    items = new_items


@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  await message.channel.send(process_command(message.content))

client.run(TOKEN)
