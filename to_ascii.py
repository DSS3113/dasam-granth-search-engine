import json, re

unicode_mappings = json.load(open('unicode_mappings.json', 'r', encoding='utf8'))
mappings = []

# Make each mapping an escaped global regex, and flip around the mappings
for sub, exp in  unicode_mappings.items():
    # Do not include empty sub -> expr mappings
    if exp != '':
        mappings.append([re.escape(exp), sub])
mappings.sort(key=lambda x: x[1].lower())
mappings.reverse()

# Replacement for Akhar + Nutka with single character
nukta_mappings = [
  [ r'sæ', r'S' ],
  [ r'Kæ', r'^' ],
  [ r'gæ', r'Z' ],
  [ r'jæ', r'z' ],
  [ r'Pæ', r'&' ],
  [ r'læ', r'L' ],
]

# Replacement rules for correcting converted unicode.
post_replacements = [
  [ r'(.)i', r'i\1' ], # Switch position of sihari
  [ r'wN', r'W' ], # Replace bindi, khana with single khana with bindi char
  [ r'(.)i([R®H§´ÍÏçœ˜†Î])', r'i\1\2' ], # Switch sihari position when pair akhars exist
  [ r'kR', r'k®' ], # Replace K pair rara with correct rara
  [ r'([nl])M', r'\1µ' ], # Replace tippi with correct tippi char
  [ r'i([nl])µ', r'i\1M' ], # Replace tippi with correct tippi char in sihari case
  [ r'([NMˆµ])I', r'\1ØI' ], # Add spacer char between bindir'tippi and bihari
  [ r'NØI', r'ˆØI' ], # Use bindi on top of spacer char
  [ r'MØI', r'µØI' ], # Use centered tippi on top of spacer char
  [ r'([@R®H´ÍÏçœ˜†])u', r'\1ü' ], # Use lower aunkar when char is pair akhar
  [ r'([@R®H´ÍÏçœ˜†])U', r'\1¨' ], # Use lower dulankaar when char is pair akhar
]

# Precompute the replacements and mappings
final_replacements = [
  [ r'(.)ਿ਼', r'\1਼ਿ' ], # Move nukta from sihari
] + mappings + nukta_mappings + post_replacements

def to_ascii(text):
  """
  Converts Gurmukhi unicode text to ASCII, used GurmukhiAkhar font.

  :param str text: The unicode text to convert.
  :return: An ASCII representation of the provided unicode Gurmukhi string.
  :rtype: str
  
  :example:

  >>> to_ascii('ਹਮਾ ਸਾਇਲਿ ਲੁਤਫ਼ਿ ਹਕ ਪਰਵਰਸ਼ ॥') 
  'hmw swieil luqi& hk prvrS ]'
  >>> to_ascii('ਸੁ ਬੈਠਿ ਇਕੰਤ੍ਰ ॥੫੭੮॥') 
  'su bYiT iekMqR ]578]'
  """
  for exp, sub in dict(final_replacements).items():
      try:
        text = re.sub(exp, sub, text)
      except Exception:
        text = re.sub(exp, re.escape(sub), text)
  return text
