<#
    This script will add $targetTag to Anki cards that have been deemed to be duplicates of learned WK vocab.
    Requires a file called "wanikani_vocab.txt" to exist at ../
    
#>

# --------------------------
#           VARS
# --------------------------
$targetTag = "mm_alreadyKnown"
$deckName = "🗾 Core 2k/6k Japanese"

# --------------------------
#         FUNCTIONS
# --------------------------
function Do-AnkiRequest ($request) {
    $url = 'http://localhost:8765'
    $t = @{
        action = $request.action
        params = $request.params
        version = 6
    } | ConvertTo-Json

    # AnkiConnect wants UTF8, which ConvertTo-Json seemingly doesn't provide
    $body = [System.Text.Encoding]::UTF8.GetBytes($t)

    <#
        Body schema:
        { 
            "action": "test",
            "params": {
                "query": "exampleQuery"
            },
            "version": 6
        }
    #>

    try {
        return irm $url -Body $body -Method POST -ContentType "application/json"
    } catch {
        throw "Error: $_"
    }
}

# --------------------------
#           MAIN
# --------------------------
try {
    $wkVocab = Get-Content "../wanikani_vocab.txt"

    Write-Host "Acquiring cards..." -f cyan
    $cardRequest = @{
        action = "findCards"
        params = @{
            query = "deck:`"$deckName`" is:review -is:suspended"
        }
    }

    # This should return an int[] in $response.result
    $cards = Do-AnkiRequest $cardRequest

    ''; Write-Host "Acquiring notes..." -f cyan
    $noteRequest = @{
        action = "cardsInfo"
        params = @{
            cards = $cards.result
        }
    }

    $notes = (Do-AnkiRequest $noteRequest).result | Select cardId, note, @{N="field";E={$_.fields."Vocabulary-Kanji".value}}

    ''; Write-Host "Comparing with WK..." -f cyan
    $duplicates = @()
    $i = 0; $wkVocab | % {
        $i++; Write-Host "`rRemaining: $($wkVocab.count - $i) [$($duplicates.count)] " -nonewline -f yellow

        $t = $null; $global:t = $notes | ? field -eq $_
        if ($t) {
            $duplicates += @{
                noteId = $t.note
                cardId = $t.cardId
            }
        }
    }

    # Get all notes with tags, cardInfo unfortunately does not return them
    ''; Write-Host "Getting tags of filtered anki cards..." -f cyan
    $notesInfoRequest = @{
        action = "notesInfo"
        params = @{
            notes = $duplicates.noteId
        }
    }

    $notesInfo = (Do-AnkiRequest $notesInfoRequest).result | select noteId, tags, fields
    $notesMissingTag = $notesInfo | ? tags -notcontains $targetTag

    if ($notesMissingTag -le 0) {
        Write-Host "No cards to patch." -f green
        return
    }

    # Write to file
    $outFile = "./notesMissingTag.txt"
    Get-Date > $outFile
    $notesMissingTag | % {
        "$($_.noteId), $($_.fields."Vocabulary-Kanji".value)" >> $outFile
    }

    # Update tags on notes that do not yet have
    ''; Write-Warning "Updating $($notesMissingTag.count) cards, adding '$targetTag'."

    $addTagRequest = @{
        action = "addTags"
        params = @{
            notes = $notesMissingTag.noteId
            tags = $targetTag
        }
    }

    $result = Do-AnkiRequest $addTagRequest

    if ($result.error) {
        throw "Got error; $($result.error)"
    }

    Write-Host "Done" -f green
} catch {
    throw "Error: $_"
}