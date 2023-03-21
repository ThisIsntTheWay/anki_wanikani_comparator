import wanikani as wk
import anki

# --------------------------
#           VARS
# --------------------------
api_token = "..."
anki_deck = "🗾 Core 2k/6k Japanese"

# --------------------------
#           FUNCS
# --------------------------

# --------------------------
#           MAIN
# --------------------------
print("### WaniKani ###")
wanikani = wk.get_wk_assignments(api_token)

print("")
print("### Anki ###")
anki = anki.get_learned_cards(anki_deck)

# Compare anki to wanikani
duplicates = []
for anki_entry in anki:
    if anki_entry in wanikani:
        duplicates.append(anki_entry)

print(" ")
print("STATS:")
print(f"> WaniKani vocab : {len(wanikani)}")
print(f"> Anki vocab     : {len(anki)}")
print(f"> Total vocab    : {len(wanikani) + len(anki)}")
print(f"  > Duplicates   : {len(duplicates)}")
print(f"  > Unique       : {(len(wanikani) + len(anki)) - len(duplicates)}")