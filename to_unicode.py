import json, re

unicode_mappings = json.load(open('unicode_mappings.json', 'r', encoding='utf8'))
mappings = []

# Make each mapping an escaped global regex
for exp, sub in  unicode_mappings.items():
    mappings.append([re.escape(exp), sub])

# Replacement rules for converting Gurmukhi ASCII to unicode.
replacements = [
  [ r'i(.)', r'\1i' ], # Switch around sihari position
  [ r'®', r'R' ], # Use only one type of pair R-sound
  [ r'([iMµyY])([R®H§ÍÏçœ˜†])', r'\2\1' ], # Switch around position of pair R, y etc sounds
  [ r'([MµyY])([uU])', r'\2\1' ], # Switch around lava/dulava/tipee with aunkar/dulankar
  [ r'`([wWIoOyYR®H§´ÍÏçœ˜†uU])', r'\1`' ], # Place adhak at end when vowels are either side
  [ r'i([´Î])', r'\1i' ], # Swap i with ´ or Î
  [ r'uo', r'ou' ], # Swap aunkarh+hora for unicode compliant hora+aunakarh
]

# Precompute the replacements and mappings
final_replacements = replacements + mappings

"""
 * Converts ASCII text used in the GurmukhiAkhar font to Unicode.
 * @param {string} text The ASCII text to convert.
 * @return {string} A unicode representation of the provided ASCII Gurmukhi string.
 * @example
 * to_unicode('kul jn mDy imil´o swrg pwn ry ]') // => ਕੁਲ ਜਨ ਮਧੇ ਮਿਲੵੋਿ ਸਾਰਗ ਪਾਨ ਰੇ ॥
 * to_unicode('su bYiT iekMqR ]578]') // => ਸੁ ਬੈਠਿ ਇਕੰਤ੍ਰ ॥੫੭੮॥
"""
def to_unicode(text):
    for exp, sub in dict(final_replacements).items():
        text = re.sub(exp, sub, text)
    return text

