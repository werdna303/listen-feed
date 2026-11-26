"""Make an episode script safe for the public feed.
Usage: python3 tools/scrub.py in.txt out.txt
Swaps private names for generic words, and prints HOLD lines for anything that needs a human look.
Edit NAMES / HOLD_WORDS below as needed."""
import re, sys
NAMES = {  # exact word -> replacement (case-sensitive, whole words)
    "Liz's": "your wife's", "Liz": "your wife", "Leamington": "your hometown",
    "your Shifting Gears": "your program", "Shifting Gears": "your program", "DSBN": "your school board",
    "Kara-Lee": "a colleague", "Katie": "a colleague", "Melinda": "a colleague",
    "Mel's": "a colleague's", "Mel": "a colleague", "EC": "a classmate", "XC": "a student",
}
HOLD_WORDS = ["Winston"]  # identifying words: flagged for a human look, not changed
src, dst = sys.argv[1], sys.argv[2]
t = open(src).read()
for k, v in NAMES.items():
    t = re.sub(r'\b' + re.escape(k) + r'(?!\w)', v, t)
# "your" at a sentence start becomes "Your"
t = re.sub(r'(^|[.!?]\s+)your\b', lambda m: m.group(1) + 'Your', t, flags=re.M)
# Two capital letters on their own look like a student's initials. Anything not on this
# list holds the episode (exit 3) so a human can look before it goes public.
ALLOW = set("AI OK TV PD IO AQ MC US UK UN EU TO UP IT IN OR AM PM CO MP PE IQ GP ER ID OT NT BC ON QC NO SO DO GO".split())
# All-caps heading lines ("SECTION TWO: SUNK COST") become sentence case with a period,
# so they read naturally and don't look like initials.
def _heading(m):
    s = m.group(0).strip().rstrip('.:').lower()
    return s[0].upper() + s[1:] + '.'
t = re.sub(r'(?m)^(?=.*[A-Z]{3})[A-Z0-9 ,.:\'"!?&-]{8,}$', _heading, t)
holds = sorted(set(re.findall(r'\b[A-Z]{2}\b', t)) - ALLOW) + [w for w in HOLD_WORDS if w in t]
open(dst, 'w').write(t)
if holds:
    print("HOLD: " + ", ".join(holds))
    sys.exit(3)
