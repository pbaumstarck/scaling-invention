import datetime
import json
import re

from bs4 import BeautifulSoup


def textify(soup_node, trim_footnotes=True):
  text = re.sub(r' ,', ',', soup_node.get_text(separator=' ').strip())
  if trim_footnotes:
    text = re.sub(r'\s\s+', ' ', re.sub(r'\[[^\]]*\]', '', text))

  # Trim whitespace.
  text = re.sub(r'(^\s*|\s*$)', '', text)
  # Fix 'NEXT -4'.
  text = re.sub(r'\s+(\-\d+)', r'\1', text)

  return text


class RocketListParser(object):
  def parse_orbit(self, rocket, raw_str):
    rocket['orbit_raw'] = raw_str
    # TODO: HTO -> HEO? Re: https://en.wikipedia.org/wiki/Magnetospheric_Multiscale_Mission
    for valid, _class in (
      ('ISS', 'leo'),
      ('LEO', 'leo'),
      ('MEO', 'heo'),
      ('HEO', 'heo'),
      ('SSO', 'sso'),
      ('GEO', 'geo'),
      ('Lunar', 'lunar'),
      ('GTO', 'geo'),
      ('HTO', 'lunar'),
      ('L1', 'lunar'),
      ('Sun–Earth L 1 insertion', 'lunar'),
      ('L2', 'lunar'),
      ('L3', 'lunar'),
      ('Heliocentric', 'lunar'),
      ('heliocentric', 'lunar'),
      ('Sun–Earth L 2', 'lunar'),
    ):
      if valid in raw_str:
        rocket['orbit_str'] = valid
        rocket['orbit_class'] = _class
        return

    if 'Highly elliptical' in raw_str or 'Molniya' in raw_str:
      rocket['orbit_str'] = 'HEO'
      rocket['orbit_class'] = 'heo'
      return
    elif 'GSO' in raw_str:
      rocket['orbit_str'] = 'GEO'
      rocket['orbit_class'] = 'geo'
      return
    elif 'Sub-orbital' in raw_str or 'Suborbital' in raw_str:
      rocket['orbit_str'] = 'Sub-orbital'
      rocket['orbit_class'] = 'leo'
      return
    elif 'Ballistic lunar transfer' in raw_str or 'TLI' in raw_str:
      rocket['orbit_str'] = 'Lunar'
      rocket['orbit_class'] = 'lunar'
      return

    raise ValueError('orbit_raw: %s' % raw_str)

  @classmethod
  def parse_file(cls, filename):
    raise NotImplemented()

  @classmethod
  def validate_rocket(cls, rocket):
    if 'booster_count' not in rocket:
      raise Exception('%s missing "booster_count"' % rocket['header'])

    if 'payload_mass_kg' not in rocket:
      raise Exception('%s missing "payload_mass_kg"' % rocket['header'])

    if 'orbit_str' not in rocket:
      raise Exception('%s missing "orbit_str"' % rocket['header'])
      # This should be validated by `parse_orbit`.

  @classmethod
  def parse_file_wrapper(cls, filename):
    rockets = cls.parse_file(filename)
    for rocket in rockets:
      cls.validate_rocket(rocket)

    return rockets

  def parse_launch_datetime(self, rocket, raw_str, strptime_formats):
    rocket['launch_datetime_raw'] = raw_str
    rocket['launch_datetime_str'] = re.sub(
      r'\s\s+',
      ' ',
      re.sub(
        r'\s*\(.*\)\s*$',
        '',
        re.sub(
          r'(,|\s*\[.*\]\s*$)',
          '',
          rocket['launch_datetime_raw'],
        ),
      ),
    )
    parsed = False
    for strptime_format in strptime_formats:
      try:
        rocket['launch_datetime'] = datetime.datetime.strptime(rocket['launch_datetime_str'], strptime_format)  # '%d %B %Y %H:%M')
        parsed = True
      except:
        pass

    if not parsed:
      raise Exception('Failed to parse datetime: ' + rocket['launch_datetime_str'])

    rocket['launch_datetime'] = str(rocket['launch_datetime'])

  def parse_payload_mass(self, rocket, raw_str):
    rocket['payload_mass_raw'] = raw_str
    rocket['payload_mass_str'] = raw_str
    rocket['payload_mass_kg'] = None
    if (rocket['payload_mass_str'] in ('Classified', 'Unknown', 'Unknown )') or
      'Classified' in rocket['payload_mass_str'] or
      'No payload' in rocket['payload_mass_str']):
      return
    elif not rocket['payload_mass_str']:
      if rocket['header'] in ('1', '2'):
        # Use the mass from the third flight.
        rocket['payload_mass_str'] = '525 kg'
        rocket['payload_mass_kg'] = 525
        return
      else:
        rocket['payload_mass_str'] = 'Unknown'
        return

    match = re.match(r'~?\s?(?P<m1>(\d+,)?\d+)([-–](?P<m2>(\d+,)?\d+))?', raw_str)
    if not match:
      raise Exception('Failed to parse payload mass', raw_str)

    mass_kg = int(re.sub(r',', '', match.group('m1')))
    if match.group('m2'):
      # Average them together.
      mass_kg = int(0.5 * (mass_kg + int(re.sub(r',', '', match.group('m2')))))

    rocket['payload_mass_kg'] = mass_kg

  @classmethod
  def get_tables(cls, soup):
    return soup.find_all('table', class_='wikitable')

  @classmethod
  def get_tr_offset(cls, filename):
    raise NotImplemented()

  def booster_landing_not_applicable(self, rocket):
    rocket['booster_landing_raw'] = 'N/A'
    rocket['booster_landing_str'] = 'N/A'
    rocket['booster_landing_method'] = 'N/A'
    rocket['booster_landing_class'] = 'not-applicable'

class Falcon9Parser(RocketListParser):
  RETIRING_FLIGHTS = set([
    'B1019.1',
    'B1022.1',
    'B1023.2',
    'B1025.2',
    'B1026.1',
    'B1021.2',
    'B1029.2',
    'B1031.2',
    'B1032.2',
    'B1035.2',
    'B1042.1',
    'B1055.1',
    'B1058.19',  # Destroyed during recovery (JRTI).
  ])

  def __init__(self):
    self.unknown_booster_number = 8

  def parse_booster_version(self, rocket, raw_str):
    rocket['booster_version_raw'] = raw_str
    rocket['booster_version_str'] = re.sub(r'\s\s+', ' ', re.sub(r'(♺|\s*\[[^\]]*\].*?$)', '', rocket['booster_version_raw']))

    if rocket['booster_version_str'].startswith('Falcon Heavy'):
      rocket['booster_version'] = 'FH Core'
    else:
      search = re.search(r'F9 \S+', rocket['booster_version_str'])
      if search:
        rocket['booster_version'] = search.group(0)
      else:
        # FH side boosters are missing this keyword.
        rocket['booster_version'] = 'FH Side'

    # TODO: 'F9 B5[311] B1046.1[268]' did not parse.
    # Also 'F9 B5[349] B1048.1[350]'.
    search = re.search(r'(B\d{4})(\.(\d+))?', rocket['booster_version_str'])
    if not search:
      # Early things are missing this.
      rocket['booster'] = 'B%04d' % self.unknown_booster_number
      self.unknown_booster_number += 1
      rocket['booster_flight'] = 1
    else:
      rocket['booster'] = search.group(1)
      rocket['booster_flight'] = int(search.group(3)) if search.group(3) else 1

    rocket['booster_version_class'] = re.sub(r'[^\w]', '_', rocket['booster_version'])

  def process_booster_landing(self, rocket, raw_str):
    rocket['booster_landing_raw'] = raw_str
    if raw_str in ('No attempt', 'Expended'):
      rocket['booster_landing_str'] = raw_str
      rocket['booster_landing_method'] = raw_str
    else:
      match = re.match(r'^(Failure|Success|Uncontrolled|Controlled|Precluded)', raw_str)
      if not match:
        raise Exception('Booster landing str not handled:', raw_str)

      rocket['booster_landing_str'] = match.group(1)

      search = re.search(r'\((.*)\)', raw_str)
      if search:
        rocket['booster_landing_method'] = search.group(1)[0].upper() + search.group(1)[1:]
      else:
        rocket['booster_landing_method'] = ''

    rocket['booster_landing_class'] = re.sub(r'\W', '-', rocket['booster_landing_str'].lower())

  def process_rocket_row(self, th, tr):
    rocket = {
      '_operator': 'SpaceX',
      '_class': 'F9',
    }

    try:
      # Parse header.
      header = re.sub(r'\s*\[.*\]\s*$', '', textify(th))
      rocket['header'] = header
      rocket['booster_count'] = 1

      # Get all cells.
      tds = tr.find_all('td')

      self.parse_launch_datetime(rocket, textify(tds[0]), ['%d %B %Y %H:%M', '%d %B %Y %H:%M:%S'])
      self.parse_booster_version(rocket, textify(tds[1]))
      rocket['launch_site_raw'] = textify(tds[2])

      rocket['payload_raw'] = textify(tds[3])
      rocket['payload_str'] = re.sub(
        r'\s*(\(.*\)|\[.*\])',
        '',
        rocket['payload_raw'])
      rocket['payload_str'] = rocket['payload_str']  # [:14]

      self.parse_payload_mass(rocket, textify(tds[4]))
      self.parse_orbit(rocket, textify(tds[5]))
      rocket['customer_raw'] = textify(tds[6])

      rocket['launch_outcome_raw'] = textify(tds[7])
      rocket['launch_outcome_str'] = re.match(r'^\w+', rocket['launch_outcome_raw']).group(0)
      rocket['launch_outcome_class'] = re.sub(r'\W', '-', rocket['launch_outcome_str'].lower())

      self.process_booster_landing(rocket, textify(tds[8]))

      rocket['is_crewed'] = 'Crew-' in rocket['payload_str'] or rocket['payload_str'] == 'Crew Dragon Demo-2'
    except Exception as e:
      print('Failed on rocket:', rocket, e)
      raise

    return self._post_process_rocket(rocket)

  def _post_process_rocket(self, rocket):
    rocket['is_retiring'] = (
      rocket['booster_landing_str'] in ('Failure', 'No attempt', 'Expended', 'Precluded', 'Uncontrolled', 'Controlled') or
      '%s.%d' % (rocket['booster'], rocket['booster_flight']) in self.RETIRING_FLIGHTS
    )
    return rocket

  def process_side_booster_row(self, rocket_base, row):
    rocket = rocket_base.copy()

    tds = row.find_all('td')
    self.parse_booster_version(rocket, textify(tds[0]))
    self.process_booster_landing(rocket, textify(tds[1]))

    return self._post_process_rocket(rocket)

  @classmethod
  def get_tr_offset(cls, filename):
    return 1

  @classmethod
  def parse_file(cls, filename):
    html_doc = open(filename, 'r').read()
    # print(html_doc)
    soup = BeautifulSoup(html_doc, 'html.parser')
    tables = cls.get_tables(soup)
    # print(tables, 'TABLES!')

    parser = cls()
    rockets = []
    for table in tables:
      # print(table)
      trs = table.find_all('tr')
      tr_ix = cls.get_tr_offset(filename)
      while tr_ix < len(trs):
        tr = trs[tr_ix]
        # print(tr)
        th = tr.find('th')
        if not th:
          # Reached the end of this table.
          break

        rowspan = int(th['rowspan'])
        if rowspan != 2:
          print('Uncommon rowspan:', th['rowspan'])

        rocket = parser.process_rocket_row(th, tr)
        rockets.append(rocket)

        if rowspan == 4:
          # It's a Falcon Heavy, so process the side boosters.
          rockets.append(parser.process_side_booster_row(rocket, trs[tr_ix + 1]))
          rockets.append(parser.process_side_booster_row(rocket, trs[tr_ix + 2]))

        tr_ix += rowspan

    print('\n'.join(
      _['header'] + ': ' + _['booster']
      # _['header'] + ': ' + str(_['launch_datetime'])
      # _['header'] + ': ' + _['booster_version_str'] + ' --> ' + _['booster_version'] + ' x ' + _['booster'] + ' > ' + str(_['booster_flight'])
      # _['header'] + ': ' + str(_['launch_site_raw'])
      # _['header'] + ': ' + str(_['payload_str'])
      # _['header'] + ': ' + str(_['payload_mass_str']) + ' --> ' + str(_['payload_mass_kg'])
      # _['header'] + ': ' + _['orbit_raw']
      # _['header'] + ': ' + _['launch_outcome_raw'] + ' --> ' + _['launch_outcome_str']
      # _['header'] + ': ' + _['booster_landing_raw'] + ' --> ' + _['booster_landing_str'] + ' _ ' + _['booster_landing_method']
      for _ in rockets
    ))

    return rockets


class UlaParser(RocketListParser):

  def __init__(self):
    pass

  def process_rocket_row(self, th, tr):
    rocket = {
      '_operator': 'ULA',
    }

    try:
      # Parse header.
      header = re.sub(r'\s*\[.*\]\s*$', '', textify(th))
      rocket['header'] = header
      rocket['booster'] = header

      # Get all cells.
      tds = tr.find_all('td')

      self.parse_launch_datetime(
        rocket,
        textify(tds[0]),
        [
          '%B %d %Y %H:%M',
          '%B %d %Y %H:%M:%S',
          '%d %B %Y %H:%M',
          '%d %B %Y %H:%M:%S',
        ],
      )
      rocket['booster_version'] = textify(tds[1])
      match = re.match(r'^Delta (\w+)', rocket['booster_version'])
      if match:
        # Put the Delta number in the header.
        header = 'D-' + header
        rocket['header'] = header
        rocket['booster'] = header
        rocket['_class'] = 'Delta'
        # All Delta IV Heavy's have 3 boosters.
        rocket['booster_count'] = 3 if 'Heavy' in rocket['booster_version'] else 1
      else:
        rocket['_class'] = 'Atlas'
        rocket['booster_count'] = 1

      rocket['booster_version_class'] = 'atlas-booster' if 'Atlas' in rocket['booster_version'] else 'delta-booster'
      rocket['launch_site'] = textify(tds[2])
      rocket['payload_str'] = re.sub(r'((?<=\()\s+|\s+(?=\)))', '', textify(tds[3]))
      self.parse_payload_mass(rocket, textify(tds[4]))

      self.parse_orbit(rocket, textify(tds[5]))
      rocket['customer_str'] = textify(tds[6])

      rocket['launch_outcome_raw'] = textify(tds[7])
      rocket['launch_outcome_str'] = re.match(r'^\w+', rocket['launch_outcome_raw']).group(0)
      rocket['launch_outcome_class'] = re.sub(r'\W', '-', rocket['launch_outcome_str'].lower())

      self.booster_landing_not_applicable(rocket)

      rocket['is_retiring'] = True

      # self.process_booster_landing(rocket, textify(tds[8]))
    except Exception as e:
      print('Atlas Failed on row:', tr, e)
      raise

    return rocket

  @classmethod
  def get_tr_offset(cls, filename):
    if 'atlas_2020' in filename:
      # The 2020's page doesn't have the extra header row.
      return 1
    else:
      return 2

  @classmethod
  def parse_file(cls, filename):
    html_doc = open(filename, 'r').read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    tables = cls.get_tables(soup)

    parser = cls()
    rockets = []
    for table in tables:
      trs = table.find_all('tr')
      tr_ix = cls.get_tr_offset(filename)

      while tr_ix < len(trs):
        tr = trs[tr_ix]
        th = tr.find('th')
        if not th:
          td = tr.find('td')
          if td and td.has_attr('colspan') and td['colspan'] == '9':
            # Hit a year break.
            if 'Future' in textify(td):
              # Found 'Future Launches' table and we should stop.
              break

            tr_ix += 2
            continue
          else:
            break

        rowspan = int(th['rowspan'])
        if rowspan != 2:
          print('Uncommon rowspan:', th['rowspan'])

        rocket = parser.process_rocket_row(th, tr)
        rockets.append(rocket)
        tr_ix += rowspan

    print('\n'.join(
      # _['header']
      # _['header'] + ': ' + str(_['launch_datetime'])
      # _['header'] + ': ' + _['booster_version']
      # _['header'] + ': ' + str(_['launch_site_raw'])
      # _['header'] + ': ' + str(_['payload_str'])
      # _['header'] + ': ' + str(_['payload_mass_str']) + ' --> ' + str(_['payload_mass_kg'])
      _['header'] + ': ' + _['orbit_str']
      # _['header'] + ': ' + _['launch_outcome_raw'] + ' --> ' + _['launch_outcome_str']
      # _['header'] + ': ' + _['booster_landing_raw'] + ' --> ' + _['booster_landing_str'] + ' _ ' + _['booster_landing_method']
      for _ in rockets
    ))

    return rockets


class ArianespaceParser(UlaParser):

  def process_rocket_row(self, th, tr):
    rocket = super(ArianespaceParser, self).process_rocket_row(th, tr)
    rocket['_operator'] = 'Arianespace'
    self.booster_landing_not_applicable(rocket)
    return rocket

  @classmethod
  def parse_file(cls, filename):
    html_doc = open(filename, 'r').read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    tables = cls.get_tables(soup)

    parser = cls()
    rockets = []
    for table in tables:
      trs = table.find_all('tr')
      tr_ix = cls.get_tr_offset(filename)
      while tr_ix < len(trs):
        tr = trs[tr_ix]
        th = tr.find('th')
        if not th:
          # print('not th!', tr)
          td = tr.find('td')
          if td and td.has_attr('colspan') and td['colspan'] == '9':
            # Hit a year break.
            if 'Future' in textify(td):
              # Found 'Future Launches' table and we should stop.
              break

            tr_ix += 2
            continue
          else:
            break

        rowspan = 2
        rocket = parser.process_rocket_row(th, tr)
        rockets.append(rocket)
        tr_ix += rowspan

    print('\n'.join(
      # _['header']
      # _['header'] + ': ' + str(_['launch_datetime'])
      # _['header'] + ': ' + _['booster_version']
      # _['header'] + ': ' + str(_['launch_site_raw'])
      # _['header'] + ': ' + str(_['payload_str'])
      # _['header'] + ': ' + str(_['payload_mass_str']) + ' --> ' + str(_['payload_mass_kg'])
      _['header'] + ': ' + _['orbit_str']
      # _['header'] + ': ' + _['launch_outcome_raw'] + ' --> ' + _['launch_outcome_str']
      # _['header'] + ': ' + _['booster_landing_raw'] + ' --> ' + _['booster_landing_str'] + ' _ ' + _['booster_landing_method']
      for _ in rockets
    ))

    return rockets


class ArianeParser(ArianespaceParser):

  @classmethod
  def get_tr_offset(cls, filename):
    if 'ariane_2020' in filename:
      # The 2020's page doesn't have the extra header row.
      return 1
    else:
      return 2

  def process_rocket_row(self, th, tr):
    rocket = super(ArianeParser, self).process_rocket_row(th, tr)

    match = re.match('^Ariane 5 (.*)$', rocket['booster_version'])
    if match:
      rocket['_class'] = 'Ariane'
      rocket['booster_version_class'] = 'ariane-booster'
      rocket['booster_version'] = 'Ariane 5'
      rocket['header'] = rocket['booster'] = re.sub(r'\s+', '-', match.group(1))
      rocket['booster_count'] = 1
    else:
      raise Exception('Bad Ariane booster version: %s' % rocket['booster_version'])

    return rocket


class VegaParser(ArianespaceParser):

  @classmethod
  def get_tr_offset(cls, filename):
    return 1

  def process_rocket_row(self, th, tr):
    rocket = super(ArianespaceParser, self).process_rocket_row(th, tr)
    # rocket['_operator'] = 'Arianespace'
    rocket['_class'] = 'Vega'
    rocket['booster_version_class'] = 'vega-booster'
    rocket['booster_count'] = 1
    return rocket



class SoyuzGuianaParser(ArianespaceParser):

  def process_rocket_row(self, th, tr):
    rocket = {
      '_operator': 'Arianespace',
      '_class': 'Soyuz',
    }

    try:
      # Get all cells.
      tds = tr.find_all('td')

      self.parse_launch_datetime(
        rocket,
        textify(tds[0]),
        [
          '%B %d %Y %H:%M',
          '%B %d %Y %H:%M:%S',
          '%d %B %Y %H:%M',
          '%d %B %Y %H:%M:%S',
        ],
      )

      # Parse header.
      header = re.sub(r'\s*\[.*\]\s*$', '', textify(tds[1]))
      rocket['header'] = header
      rocket['booster'] = header
      rocket['booster_version'] = 'Soyuz'
      rocket['booster_version_class'] = 'soyuz-booster'
      rocket['booster_count'] = 1

      rocket['launch_site'] = 'Guiana Space Centre'
      rocket['payload_str'] = textify(tds[2])
      self.parse_payload_mass(rocket, textify(tds[3]))

      # rocket['orbit_str'] = textify(tds[4])
      self.parse_orbit(rocket, textify(tds[4]))

      rocket['launch_outcome_raw'] = textify(tds[5])
      rocket['launch_outcome_str'] = rocket['launch_outcome_raw']
      rocket['launch_outcome_class'] = re.sub(r'\W', '-', rocket['launch_outcome_str'].lower())

      self.booster_landing_not_applicable(rocket)

      rocket['is_retiring'] = True
    except Exception as e:
      print('Soyuz at Guiana failed on row:', tr, e)
      raise

    return rocket

  @classmethod
  def get_tr_offset(cls, filename):
    return 1

  @classmethod
  def get_tables(cls, soup):
    # Chop off that extra "Orbit" table.
    return soup.find_all('table', class_='wikitable')[1:]

  @classmethod
  def parse_file(cls, filename):
    html_doc = open(filename, 'r').read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    tables = cls.get_tables(soup)

    parser = cls()
    rockets = []
    for table in tables:
      trs = table.find_all('tr')
      tr_ix = cls.get_tr_offset(filename)
      all_done = False
      while tr_ix < len(trs):
        tr = trs[tr_ix]
        tds = tr.find_all('td')
        if tds and len(tds) >= 6 and 'Planned' in textify(tds[5]):
          # We've hit the planned launches, so exit.
          all_done = True
          break

        rocket = parser.process_rocket_row(None, tr)
        rockets.append(rocket)
        tr_ix += 1

      if all_done:
        break

    print('\n'.join(
      # _['header']
      # _['header'] + ': ' + str(_['launch_datetime'])
      # _['header'] + ': ' + _['booster_version']
      # _['header'] + ': ' + str(_['launch_site'])
      # _['header'] + ': ' + str(_['payload_str'])
      # _['header'] + ': ' + str(_['payload_mass_str']) + ' --> ' + str(_['payload_mass_kg'])
      _['header'] + ': ' + _['orbit_str']
      # _['header'] + ': ' + _['launch_outcome_raw'] + ' --> ' + _['launch_outcome_str'] + ' (' + _['launch_outcome_class'] + ')'
      # _['header'] + ': ' + _['booster_landing_raw'] + ' --> ' + _['booster_landing_str'] + ' _ ' + _['booster_landing_method']
      for _ in rockets
    ))

    return rockets


class Soyuz2Parser(ArianespaceParser):

  def process_rocket_row(self, th, tr):
    rocket = {
      '_operator': 'Arianespace',
      '_class': 'Soyuz',
    }

    try:
      # Get all cells.
      tds = tr.find_all('td')

      self.parse_launch_datetime(
        rocket,
        textify(tds[1]),
        [
          '%B %d %Y %H:%M',
          '%B %d %Y %H:%M:%S',
          '%d %B %Y %H:%M',
          '%d %B %Y %H:%M:%S',
          '%d %B %Y',
          '%d %B %Y %H:%M',
          '%d %B %Y %H:%M:%S',
        ],
      )

      rocket['booster_version'] = re.sub(r'Fregat.*', '', re.sub(r'\s*\[.*\]\s*$', '', textify(tds[2]))).strip()
      rocket['booster_version_class'] = 'soyuz-booster'
      rocket['booster_count'] = 1

      rocket['launch_site'] = textify(tds[3])
      rocket['launch_outcome_raw'] = textify(tds[4])
      rocket['launch_outcome_str'] = rocket['launch_outcome_raw']
      rocket['launch_outcome_class'] = re.sub(r'\W', '-', rocket['launch_outcome_str'].lower())

      rocket['payload_str'] = textify(tds[5])
      if 'OneWeb' in rocket['payload_str'] and 'OneWeb-1 ' not in rocket['payload_str']:
        # Only save OneWeb missions past 1, which are already listed from Soyuz at Guiana.
        match = re.search(r'OneWeb\-(\d+)', rocket['payload_str'])
        if match:
          rocket['booster'] = rocket['header'] = 'ST-%d' % self.st_mission_counter
          self.st_mission_counter += 1
        elif 'OneWeb ' in rocket['payload_str']:
          rocket['booster'] = rocket['header'] = 'ST-%d' % self.st_mission_counter
          self.st_mission_counter += 1
        else:
          raise ValueError('Bad OneWeb launch: %s' % rocket['payload_str'])
        # rocket['booster'] = rocket['header'] = 'ST-%d' % int(25 + int(match.group(1)))
      else:
        return None

      rocket['payload_mass_str'] = '5,689 kg'
      rocket['payload_mass_kg'] = 5689
      # self.parse_payload_mass(rocket, textify(tds[3]))

      rocket['orbit_str'] = 'LEO'
      rocket['orbit_class'] = 'leo'

      self.booster_landing_not_applicable(rocket)

      rocket['is_retiring'] = True
    except Exception as e:
      print('Soyuz2 failed on row:', tr, e)
      raise

    return rocket

  @classmethod
  def get_tr_offset(cls, filename):
    return 1

  @classmethod
  def get_tables(cls, soup):
    # Chop off that extra "Orbit" table.
    return soup.find_all('table', class_='wikitable')

  @classmethod
  def parse_file(cls, filename):
    html_doc = open(filename, 'r').read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    tables = cls.get_tables(soup)

    parser = cls()
    parser.st_mission_counter = 27

    rockets = []
    for table in tables:
      trs = table.find_all('tr')
      tr_ix = cls.get_tr_offset(filename)
      all_done = False
      while tr_ix < len(trs):
        tr = trs[tr_ix]
        tds = tr.find_all('td')
        if tds:
          if len(tds) < 4:
            # Just a bad row.
            tr_ix += 1
            continue
          elif 'Scheduled' in textify(tds[3]) or 'Planned' in textify(tds[3]):
            # We've hit the planned launches table, so exit.
            all_done = True
            break

        rocket = parser.process_rocket_row(None, tr)
        if rocket:
          rockets.append(rocket)

        tr_ix += 1

      if all_done:
        break

    print('\n'.join(
      # _['header']
      # _['header'] + ': ' + str(_['launch_datetime'])
      # _['header'] + ': ' + _['booster_version']
      # _['header'] + ': ' + str(_['launch_site'])
      _['header'] + ': ' + str(_['payload_str'])
      # _['header'] + ': ' + str(_['payload_mass_str']) + ' --> ' + str(_['payload_mass_kg'])
      # _['header'] + ': ' + _['orbit_str']
      # _['header'] + ': ' + _['launch_outcome_raw'] + ' --> ' + _['launch_outcome_str'] + ' (' + _['launch_outcome_class'] + ')'
      # _['header'] + ': ' + _['booster_landing_raw'] + ' --> ' + _['booster_landing_str'] + ' _ ' + _['booster_landing_method']
      for _ in rockets
    ))

    return rockets


tallies = {}
all_rockets = []

to_parse = (
  # '*' +
  ','.join([
    'spacex',
    # 'ula',
    # 'atlas',
    # 'delta',
    # 'arianespace',
    # 'ariane5',
    # 'vega',
    # 'soyuz_guiana',
    # 'soyuz2',
  ])
)


def get_tallies(tallies, label, rockets):
  global all_rockets
  all_rockets.extend(rockets)
  tallies[label] = {
    'num_launches': len(rockets),
    'num_boosters': sum(_['booster_count'] for _ in rockets),
    'payload_mass_kg': sum(_['payload_mass_kg'] or 0 for _ in rockets),
  }


# SpaceX
if '*' in to_parse or 'spacex' in to_parse or 'falcon9' in to_parse:
  print('\n\nParsing Falcon 9 and Falcon Heavy ...')
  f9_input_filenames = [
    'web_pages/falcon9_2010s_20220526.html',
    'web_pages/falcon9_2020s_20240301.html',
  ]
  spacex_output_filename = '../pgbsv/public/js/spacex_rockets_parsed.js'
  rockets_f9_fh = [__ for _ in f9_input_filenames for __ in Falcon9Parser.parse_file_wrapper(_)]
  if False:
    print('\n' + ''.join([
      'ViaSat: %d' % i
      for i in range(len(rockets_f9_fh))
      if rockets_f9_fh[i]['payload_raw'].startswith('ViaSat-3')
    ]))
    rockets_f9_fh = rockets_f9_fh[230:]

  with open(spacex_output_filename, 'w') as f:
    f.write('function getFalcon9FalconHeavyLaunches() {\n  return ')
    f.write(json.dumps(rockets_f9_fh, indent=2))
    f.write(';\n}\n')

  print('Parsed', f9_input_filenames, 'to', spacex_output_filename)
  get_tallies(tallies, 'SpaceX', rockets_f9_fh)


# ULA
if '*' in to_parse or 'ula' in to_parse or 'atlas' in to_parse or 'delta' in to_parse:
  print('\n\nParsing ULA ...')
  atlas_input_filenames = (
    (
      [
        'web_pages/atlas_2010s_20210605.html',
        'web_pages/atlas_2020s_20220601.html',
      ] if '*' in to_parse or 'atlas' in to_parse else []
    ) + (
      [
        'web_pages/delta_2010s_20210606.html',
        'web_pages/delta_2020s_20220203.html',
      ] if '*' in to_parse or 'delta' in to_parse else []
    )
  )
  atlas_output_filename = 'ula_rockets_parsed.js'
  rockets_ula = [__ for _ in atlas_input_filenames for __ in UlaParser.parse_file_wrapper(_)]
  rockets_ula.sort(key=lambda x: x['launch_datetime'])
  with open(atlas_output_filename, 'w') as f:
    f.write('function getUlaLaunches() {\n  return ')
    f.write(json.dumps(rockets_ula, indent=2))
    f.write(';\n}\n')

  print('Parsed', ','.join(atlas_input_filenames), 'to', atlas_output_filename)
  # tallies['ULA'] = len(rockets_ula)
  get_tallies(tallies, 'ULA', rockets_ula)


# Arianespace
# TODO: https://en.wikipedia.org/wiki/Soyuz_at_the_Guiana_Space_Centre
# TODO: https://en.wikipedia.org/wiki/List_of_Vega_launches
# TODO: All the OneWeb launches off here: https://en.wikipedia.org/wiki/Soyuz-2
if ('*' in to_parse or 'arianespace' in to_parse or 'ariane5' in to_parse or 'vega' in to_parse or
    'soyuz_guiana' in to_parse or 'soyuz2' in to_parse):
  print('\n\nParsing Arianespace ...')
  arianespace_input_filenames = (
    (
      [
        ('web_pages/ariane_2010s_wiki_20210608.html', ArianeParser),
        ('web_pages/ariane_2020s_wiki_20220207.html', ArianeParser),
      ] if '*' in to_parse or 'ariane5' in to_parse else []
    ) + (
      [
        ('web_pages/vega_wiki_20220207.html', VegaParser),
      ] if '*' in to_parse or 'vega' in to_parse else []
    ) + (
      [
        ('web_pages/soyuz_guiana_wiki_20220601.html', SoyuzGuianaParser),
      ] if '*' in to_parse or 'soyuz_guiana' in to_parse else []
    ) + (
      [
        ('web_pages/soyuz2_wiki_20220207.html', Soyuz2Parser),
      ] if '*' in to_parse or 'soyuz2' in to_parse else []
    )
  )
  arianespace_output_filename = 'arianespace_rockets_parsed.js'
  rockets_arianespace = [__ for filename, cls in arianespace_input_filenames for __ in cls.parse_file_wrapper(filename)]
  rockets_arianespace.sort(key=lambda x: x['launch_datetime'])
  with open(arianespace_output_filename, 'w') as f:
    f.write('function getArianespaceLaunches() {\n  return ')
    f.write(json.dumps(rockets_arianespace, indent=2))
    f.write(';\n}\n')

  print('Parsed', ','.join([_[0] for _ in arianespace_input_filenames]), 'to', arianespace_output_filename, ' FOUND', len(rockets_arianespace), 'launches')
  # tallies['Arianespace'] = len(rockets_arianespace)
  get_tallies(tallies, 'Arianespace', rockets_arianespace)


print(json.dumps(tallies, indent=2))

if '*' in to_parse:
  # We have enough data to calculate the frequentist statistics.

  # TODO: Put a Bayesian estimate for the payload mass for classified payloads.
  orbits = set(_['orbit_str'] for _ in all_rockets)
  frequentist_payloads = {}
  print('orbits:', orbits)
  for orbit in orbits:
    # Exclude Starlink launches, since they skew things so much.
    num_payloads = sum(
      int(_['orbit_str'] == orbit) for _ in all_rockets if 'Starlink' not in _['payload_str']
    )
    num_nonzero_payloads = sum(
      int(_['orbit_str'] == orbit) for _ in all_rockets if 'Starlink' not in _['payload_str'] and _['payload_mass_kg']
    )
    total_payload = sum(
      _['payload_mass_kg'] or 0 for _ in all_rockets if 'Starlink' not in _['payload_str'] and _['orbit_str'] == orbit
    )
    ave_payload = 1.0 * total_payload / num_nonzero_payloads if num_nonzero_payloads else 0.0
    print(orbit, num_payloads, total_payload, total_payload * 1.0 / num_payloads, ave_payload)
    frequentist_payloads[orbit] = ave_payload
    print('Average:', orbit, ave_payload)

  # Hot-wire GTO to GEO if nece.
  frequentist_payloads['GEO'] = frequentist_payloads['GEO'] or frequentist_payloads['GTO']
  print(json.dumps(frequentist_payloads, indent=2))
