import wanikani as wk
import anki

# --------------------------
#           VARS
# --------------------------
api_token = "..."
anki_deck = "🗾 Core 2k/6k Japanese"

class bcolors:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    ENDC = '\033[0m'

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
for wk_entry in wanikani:
    if wk_entry in anki:
        duplicates.append(wk_entry)

print(" ")
print(bcolors.CYAN    + "STATS:")
print(bcolors.MAGENTA + f"> WaniKani vocab : {len(wanikani)}")
print(bcolors.BLUE    + f"> Anki vocab     : {len(anki)}")
print(bcolors.YELLOW  + f"> Total vocab    : {len(wanikani) + len(anki)}")
print(bcolors.RED     + f"  > Duplicates   : {len(duplicates)}")
print(bcolors.GREEN   + f"  > Unique       : {(len(wanikani) + len(anki)) - len(duplicates)}")
print(bcolors.ENDC)