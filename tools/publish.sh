#!/bin/bash
# Turn inbox/*.txt into published episodes: scrub, voice, add to feed, push.
set -e
cd "$(dirname "$0")/.."
BASE=https://werdna303.github.io/listen-feed/
for f in inbox/*.txt; do
  [ -e "$f" ] || { echo "inbox empty"; exit 0; }
  title=$(head -1 "$f" | sed 's/^Listen\. *//; s/[.?!]*$//')
  slug=$(echo "$title" | tr 'A-Z' 'a-z' | sed 's/[^a-z0-9]\+/-/g; s/^-//; s/-$//' | cut -c1-70 | sed 's/-$//')
  if [ -e "episodes/$slug.mp3" ]; then echo "skip (exists): $slug"; rm "$f"; continue; fi
  # scrub exits 3 when it sees possible initials or a hold word: park it for a human look
  # work in inbox/work (gitignored) so nothing sits untracked in the repo while it records
  W=inbox/work; mkdir -p "$W"
  rc=0; python3 tools/scrub.py "$f" "$W/$slug.txt" || rc=$?
  if [ $rc -ne 0 ]; then
    rm -f "$W/$slug.txt"; mkdir -p inbox/held; mv "$f" inbox/held/
    echo "held: $title"; continue
  fi
  python3 -I tools/tts.py "$W/$slug.txt" "$W/$slug.mp3" </dev/null
  mv "$W/$slug.txt" "$W/$slug.mp3" episodes/
  python3 build_feed.py "$BASE"
  git add "episodes/$slug.txt" "episodes/$slug.mp3" feed.xml published.json
  git commit -q -m "Add episode: $title"
  for i in 1 2 3 4; do git -c push.negotiate=true push -q origin main 2>/dev/null && break || sleep $((2**i)); done
  rm "$f"; echo "published: $title"
done
