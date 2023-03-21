import requests
from urllib.parse import urljoin

# Private function for performing a GET request against the WK API
def _get_request (api_token, url):
    try:
        headers = {
            'Authorization': f"Bearer {api_token}"
        }

        response = requests.get(url, headers=headers)
        return response.json()

    except Exception as e:
        raise ValueError(f"Error accessing '{url}': {str(e)}")

# Retrieves ACTIVE VOCABULARY assignments in WK.
# Returns their IDs.
def get_wk_assignments (api_token):
    try:
        base_url = "https://api.wanikani.com/v2/"
        endpoint = urljoin(base_url, "assignments?started=true&subject_types=vocabulary")
        response = _get_request(api_token, endpoint)

        assignment_ids = []
        if response["data"] is not None:
            for item in response["data"]:
                assignment_ids.append(item["data"]["subject_id"])

        # Handle pagination
        next_url = response["pages"]["next_url"]

        print("> Assembling assignments...")
        while next_url is not None:
            response = _get_request(api_token, next_url)
            next_url = response["pages"]["next_url"]

            if response["data"] is not None:
                for item in response["data"]:
                    assignment_ids.append(item["data"]["subject_id"])

        print(f"> Got {len(assignment_ids)} entries.")
        #return assignment_ids

        # Get actual vocabulary
        big_ass_array = ",".join(str(i) for i in assignment_ids)
        #print(big_ass_array)

        # We cannot possibly pass our big ass array, we'd get HTTP/412 otherwise
        endpoint = urljoin(base_url, f"subjects?types=vocabulary")
        response = _get_request(api_token, endpoint)

        subjects = []
        print("> Assembling subjects")
        for item in response["data"]:
            # Only include subjects actually learned
            candidate = str(item["id"])
            if candidate in big_ass_array:
                subjects.append(item["data"]["characters"])

        # Once again, pagination
        next_url = response["pages"]["next_url"]
        print("  > Pagination...")
        while next_url is not None:
            response = _get_request(api_token, next_url)
            next_url = response["pages"]["next_url"]
            
            if response["data"] is not None:
                for item in response["data"]:
                    # Only include subjects actually learned
                    candidate = str(item["id"])
                    if candidate in big_ass_array:
                        subjects.append(item["data"]["characters"])

        print("> Writing to file...")
        with open("wanikani_vocab.txt", "w") as f:
            for subject in subjects:
                f.write(f"{subject}\n")
        
    except Exception as e:
        print(f"Failure: {str(e)}")

# --------------------------------------------
# MAIN DEBUG
token = "..."
get_wk_assignments(token)
print("Done")