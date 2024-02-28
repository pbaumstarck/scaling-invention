"""

 0%[>                   ]
10%[==>                 ]
20%[====>               ]
30%[======>             ]
40%[========>           ]
50%[==========>         ]
60%[============>       ]
70%[==============>     ]
80%[================>   ]
90%[==================> ]


"""

import math


def simulate_progress_bar(bar, multi_line=False):
  for i in [0, 10, 20, 30, 40, 50, 52, 55, 60, 70, 80, 90, 100]:
    if multi_line:
      print('Progress', '% 4d%%' % i)
      print(bar.progress(i / 100.0))
    else:
      print('Progress', '% 4d%%' % i, bar.progress(i / 100.0))


class ProgressBar(object):
  def __init__(self, pattern, num_chars=32):
    self.pattern = pattern
    self.num_chars = num_chars

  def progress(self, fraction):
    """Returns the progress bar to the certain fraction of characters.

    Args:
      fraction double: The fractional percentage.
    """
    fraction = min(1.0, max(0.0, fraction))

    # Split the bar into the fixed, progress, and padded regions.
    fixed_chars_len = len(self.pattern)
    left_pad_len = min(
      self.num_chars - fixed_chars_len,
      round((self.num_chars - fixed_chars_len) * fraction),
    )
    right_pad_len = self.num_chars - fixed_chars_len - left_pad_len

    return (
      '[' +
      ' ' * left_pad_len +
      self.pattern +
      ' ' * right_pad_len +
      ']'
    )



class MultiLineProgressBar(object):
  def __init__(self, pattern, num_chars=32, progress_bar_cls=ProgressBar):
    self.progress_bars = [progress_bar_cls(_, num_chars=num_chars) for _ in pattern.split('\n')]

  def progress(self, fraction):
    return '\n'.join(_.progress(fraction) for _ in self.progress_bars)


class VariableProgressBar(object):
  def __init__(self, pattern, num_chars=32):
    self.num_chars = num_chars
    self.pattern_segments = []

    ix = 0
    while ix < len(pattern):
      ch = pattern[ix]
      if ix + 1 < len(pattern) and pattern[ix + 1] == '*':
        self.pattern_segments.append((ch, '*'))
        ix += 2
      else:
        self.pattern_segments.append((ch, None))
        ix += 1

    if not any(repeat for segment, repeat in self.pattern_segments):
      self.pattern_segments.insert(0, (' ', '*'))

    # Now '=*>' will parse as: `[('=', '*'), ('>', None')]`.

  def progress(self, fraction):
    fraction = min(1.0, max(0.0, fraction))

    fixed_chars_len = sum(0 if repeat else len(segment) for segment, repeat in self.pattern_segments)
    variable_chars_len = sum(len(segment) if repeat else 0 for segment, repeat in self.pattern_segments)

    # Calculate how many copies of the variable chars we'll need.
    num_variable_segments = min(
      math.floor((self.num_chars - fixed_chars_len) / variable_chars_len),
      round((self.num_chars - fixed_chars_len) * fraction / variable_chars_len),
    )
    accounted_len = fixed_chars_len + num_variable_segments * variable_chars_len
    right_pad_len = self.num_chars - accounted_len

    return (
      '[' +
      ''.join(
        segment * num_variable_segments if repeat else segment
        for segment, repeat in self.pattern_segments
      ) +
      ' ' * right_pad_len +
      ']'
    )



BODY = 'body'
REPEAT = 'repeat'
FIXED_CHARS_LEN = 'fixed_chars_len'
VARIABLE_CHARS_LEN = 'variable_chars_len'

class RotatingProgressBar(object):
  def __init__(self, pattern, num_chars=32):
    self.num_chars = num_chars
    self.pattern_segments = []
    self.counter = 0

    ix = 0
    while ix < len(pattern):
      ch = pattern[ix]
      if ch == '[':
        # Parse sub-region ...
        start_ix = ix
        ix += 1
        while ix < len(pattern) and pattern[ix] != ']':
          ix += 1

        ch = pattern[start_ix + 1:ix]
        if ',' in ch:
          ch = ch.split(',')
          # TODO: Check length.

      if ix + 1 < len(pattern) and pattern[ix + 1] == '*':
        self.pattern_segments.append((ch, '*'))
        ix += 2
      else:
        self.pattern_segments.append((ch, None))
        ix += 1

    # Make sure we have at least one repeating character, even a leading space.
    if not any(repeat for segment, repeat in self.pattern_segments):
      self.pattern_segments.insert(0, (' ', '*'))

  def progress(self, fraction):
    fraction = min(1.0, max(0.0, fraction))

    fixed_chars_len = sum(
      0 if repeat else len(segment[0] if isinstance(segment, list) else segment)
      for segment, repeat in self.pattern_segments
    )
    variable_chars_len = sum(
      len(segment[0] if isinstance(segment, list) else segment) if repeat else 0
      for segment, repeat in self.pattern_segments
    )

    # Calculate how many copies of the variable chars we'll need.
    num_variable_segments = min(
      math.floor((self.num_chars - fixed_chars_len) / variable_chars_len),
      round((self.num_chars - fixed_chars_len) * fraction / variable_chars_len),
    )
    accounted_len = fixed_chars_len + num_variable_segments * variable_chars_len
    right_pad_len = self.num_chars - accounted_len

    # Increment the counter to get segment animation.
    counter = self.counter
    self.counter += 1

    return (
      '[' +
      ''.join(
        (segment[self.counter % len(segment)] if isinstance(segment, list) else segment) *
          (num_variable_segments if repeat else 1)
        for segment, repeat in self.pattern_segments
      ) +
      ' ' * right_pad_len +
      ']'
    )



simulate_progress_bar(ProgressBar('>'))
simulate_progress_bar(ProgressBar('<>'))
simulate_progress_bar(ProgressBar('(>\'o\')>'))
simulate_progress_bar(VariableProgressBar('>'))
simulate_progress_bar(VariableProgressBar('=*>'))
simulate_progress_bar(VariableProgressBar('<=*>'))
simulate_progress_bar(VariableProgressBar('<=*-*>'))
simulate_progress_bar(RotatingProgressBar('[=-]'))
simulate_progress_bar(RotatingProgressBar('[=-]*'))
simulate_progress_bar(RotatingProgressBar('[=,-]*'))
simulate_progress_bar(RotatingProgressBar('[<,>]*'))
simulate_progress_bar(RotatingProgressBar('[<,>]*'))

simulate_progress_bar(
  MultiLineProgressBar(
    '=(^-^)=\n.*[_,\\](u_u) ',
    progress_bar_cls=RotatingProgressBar),
  multi_line=True)
