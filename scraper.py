import json
import re
from mongodb import UploadToMongoDB

# Path to the input and output JSON files
input_file_path = "./input.json"
output_file_path = "./output.json"

# Regex to check if "city" exists in the location
city_regex = re.compile(r"\b(city)\b", re.IGNORECASE)


# *
# *
# *
# *
# *
# *
# *


# region: Extract Tweet Data
def extract_tweet_data(file_path):
    try:
        # Load the JSON from the file
        with open(file_path, "r") as file:
            data = json.load(file)

        # Navigate the JSON structure
        instructions = (
            data.get("data", {})
            .get("search_by_raw_query", {})
            .get("search_timeline", {})
            .get("timeline", {})
            .get("instructions", [])
        )
        tweets = []

        for instruction in instructions:
            if instruction.get("type") == "TimelineAddEntries":
                entries = instruction.get("entries", [])
                for entry in entries:
                    if (
                        entry.get("content", {}).get("entryType")
                        == "TimelineTimelineItem"
                    ):
                        tweet_result = entry["content"]["itemContent"]["tweet_results"][
                            "result"
                        ]

                        # Extract fields
                        tweet_id = tweet_result.get("rest_id", "")
                        created_at = tweet_result.get("legacy", {}).get(
                            "created_at", ""
                        )
                        profile_image_url = (
                            tweet_result.get("core", {})
                            .get("user_results", {})
                            .get("result", {})
                            .get("legacy", {})
                            .get("profile_image_url_https", "")
                        )
                        screen_name = (
                            tweet_result.get("core", {})
                            .get("user_results", {})
                            .get("result", {})
                            .get("legacy", {})
                            .get("screen_name", "")
                        )
                        source = tweet_result.get("source", "")
                        lang = tweet_result.get("legacy", {}).get("lang", "")
                        location = (
                            tweet_result.get("core", {})
                            .get("user_results", {})
                            .get("result", {})
                            .get("legacy", {})
                            .get("location", "")
                        )
                        full_text = tweet_result.get("legacy", {}).get("full_text", "")
                        user_mentions = [
                            {
                                "screen_name": mention.get("screen_name", ""),
                                "name": mention.get("name", ""),
                                "id_str": mention.get("id_str", ""),
                            }
                            for mention in tweet_result.get("legacy", {})
                            .get("entities", {})
                            .get("user_mentions", [])
                        ]

                        # Exclude tweets without "city" in location
                        if location and not city_regex.search(location):
                            continue

                        # Collect tweet data
                        tweets.append(
                            {
                                "tweet_id": tweet_id,
                                "created_at": created_at,
                                "profile_image_url": profile_image_url,
                                "screen_name": screen_name,
                                "source": source,
                                "lang": lang,
                                "location": location,
                                "full_text": full_text,
                                "user_mentions": user_mentions,
                            }
                        )

        return tweets

    except json.JSONDecodeError as e:
        print("Error parsing JSON:", e)
        return []
    except KeyError as e:
        print("Key error while extracting data:", e)
        return []


# *
# *
# *
# *
# *
# *
# *

ncr_tweets = []
metro_manila_cities = [
    "Manila",
    "Quezon",
    "Caloocan",
    "Taguig",
    "Pasig",
    "Makati",
    "Las Piñas",
    "Parañaque",
    "Marikina",
    "Muntinlupa",
    "Pasay",
    "Valenzuela",
    "Malabon",
    "Navotas",
    "San Juan",
    "Caloocan",
    "Pateros",
]

# *
# *
# *
# *
# *
# *
# *

network_keywords = [
    "lagging",
    "buffering",
    "slow",
    "unstable",
    "connection",
    "poor",
    "performance",
    "dropped",
    "intermittent",
    "service",
    "timeout",
    "low",
    "bandwidth",
    "latency",
    "download",
    "upload",
    "signal",
    "disconnected",
    "unable",
    "to",
    "load",
    "pages",
    "wi-fi",
    "service",
    "disruption",
    "weak",
    "speed",
    "test",
    "results",
    "streaming",
    "browsing",
    "video",
    "quality",
    "choppy",
    "video",
    "calls",
    "network",
    "congestion",
    "issues",
    "internet",
    "frequent",
    "disconnections",
    "packet",
    "loss",
    "high",
    "ping",
    "lag",
    "spikes",
    "technician",
    "networks",
    "sim",
]

# *
# *
# *
# *
# *
# *
# *

general_complaints = [
    "no",
    "to",
    "pages",
    "results",
    "technician",
    "koneksyon",
    "problema",
    "sa",
    "internet",
    "matagal",
    "mag-load",
    "hindi",
    "makapag-browse",
    "hindi",
    "makapag-stream",
]

# *
# *
# *
# *
# *
# *
# *

leaning_network_complaints = [
    "weak",
    "internet",
    "high",
    "ping",
    "mabagal",
    "hindi",
    "makapasok",
    "walang",
    "pabago-bago",
    "koneksyon",
    "matatag",
    "na",
    "koneksyon",
]

# *
# *
# *
# *
# *
# *
# *

keyword_for_slow = ["mabagal", "internet", "slow", "bagal"]
keyword_for_no_internet = ["no internet", "no wifi", "wala", "connection", "what's up"]

# *
# *
# *
# *
# *
# *
# *

regions = [
    {
        "region": "CAR",
        "provinces": [
            "Abra",
            "Apayao",
            "Benguet",
            "Ifugao",
            "Kalinga",
            "Mountain Province",
        ],
    },
    {
        "region": "I",
        "provinces": ["Ilocos Norte", "Ilocos Sur", "La Union", "Pangasinan"],
    },
    {
        "region": "II",
        "provinces": ["Batanes", "Cagayan", "Isabela", "Nueva Vizcaya", "Quirino"],
    },
    {
        "region": "III",
        "provinces": [
            "Aurora",
            "Bataan",
            "Bulacan",
            "Nueva Ecija",
            "Pampanga",
            "Tarlac",
            "Zambales",
        ],
    },
    {
        "region": "IV-A",
        "provinces": ["Batangas", "Cavite", "Laguna", "Quezon", "Rizal"],
    },
    {
        "region": "IV-B",
        "provinces": [
            "Marinduque",
            "Masbate",
            "Romblon",
            "Occidental Mindoro",
            "Oriental Mindoro",
            "Palawan",
        ],
    },
    {
        "region": "V",
        "provinces": [
            "Albay",
            "Camarines Norte",
            "Camarines Sur",
            "Catanduanes",
            "Masbate",
            "Sorsogon",
        ],
    },
    {
        "region": "VI",
        "provinces": ["Aklan", "Antique", "Capiz", "Iloilo", "Negros Occidental"],
    },
    {"region": "VII", "provinces": ["Bohol", "Cebu", "Negros Oriental", "Siquijor"]},
    {
        "region": "VIII",
        "provinces": [
            "Biliran",
            "Eastern Samar",
            "Leyte",
            "Northern Samar",
            "Samar",
            "Southern Leyte",
        ],
    },
    {
        "region": "IX",
        "provinces": ["Zamboanga del Norte", "Zamboanga del Sur", "Zamboanga Sibugay"],
    },
    {
        "region": "X",
        "provinces": [
            "Bukidnon",
            "Camiguin",
            "Lanao del Norte",
            "Misamis Occidental",
            "Misamis Oriental",
        ],
    },
    {
        "region": "XI",
        "provinces": [
            "Davao de Oro",
            "Davao del Norte",
            "Davao del Sur",
            "Davao Occidental",
            "Davao Oriental",
        ],
    },
    {
        "region": "XII",
        "provinces": [
            "Cotabato",
            "Sarangani",
            "South Cotabato",
            "Sultan Kudarat",
            "Tacurong",
        ],
    },
    {
        "region": "CARAGA",
        "provinces": [
            "Agusan del Norte",
            "Agusan del Sur",
            "Surigao del Norte",
            "Surigao del Sur",
            "Dinagat Islands",
        ],
    },
    {
        "region": "BARMM",
        "provinces": ["Basilan", "Lanao del Sur", "Maguindanao", "Sulu", "Tawi-Tawi"],
    },
]


count = 0

# *
# *
# *
# *
# *
# *
# *


# *
# *
# *
# *
# *
# *
# *


# region: Check Region
def check_region(_location: str) -> str:
    current_region: str = ""

    for region in regions:

        current_provinces = region["provinces"]
        pattern = r"\b(?:{}|{})\b".format(
            "|".join(current_provinces), "|".join(current_provinces).lower()
        )

        if re.search(pattern, _location, re.IGNORECASE):
            current_region = region["region"]
            break

    return current_region


# *
# *
# *
# *
# *
# *
# *


# region: Check City
def check_city(_location: str) -> bool:
    # Create the regex pattern to match any of the cities
    pattern = r"\b(?:{}|{})\b".format(
        "|".join(metro_manila_cities), "|".join(metro_manila_cities).lower()
    )

    if re.search(pattern, _location, re.IGNORECASE):
        return True
    return False


# *
# *
# *
# *
# *
# *
# *


# region: Check Network Issue
def check_network_issue(_text):
    split_str = _text.split(" ")
    weight: int = 0

    keyword_category = [
        {"array": network_keywords, "points": 3},
        {"array": leaning_network_complaints, "points": 2},
        {"array": general_complaints, "points": 1},
    ]

    for i in split_str:
        found: bool = False
        current_word_len = len(i)

        for kc in keyword_category:
            current_points: int = kc["points"]
            for word in kc["array"]:
                if (
                    current_word_len >= len(word)
                    and re.match(word, i)
                    and found == False
                ):
                    weight += current_points
                    found = True

    return weight >= 3


# *
# *
# *
# *
# *
# *
# *


print("Hey!")

# region: Extract Tweets
for i in range(42):

    tweets = extract_tweet_data(f"./json/input{i + 1}.json")
    count += len(tweets)
    for t in tweets:
        current_location = t["location"]
        is_ncr: bool = check_city(current_location)

        if is_ncr == True:
            t["ncr"] = is_ncr
            t["region"] = None
        else:
            current_region = check_region(current_location)

            if len(current_region) > 0:
                t["region"] = current_region
            else:
                t["region"] = None
            t["ncr"] = False

        full_text = t["full_text"]
        full_text_split = full_text.split(" ")

        is_network_issue = check_network_issue(full_text)
        t["network_issue"] = is_network_issue
        if is_network_issue == True:
            no_weight: int = 0
            slow_weight: int = 0

            for i in full_text_split:
                for kfs in keyword_for_slow:
                    if i in kfs:
                        slow_weight += 1

                for kfoi in keyword_for_no_internet:
                    if i in kfoi:
                        no_weight += 1

            t["network_issue_type"] = (
                "slow_internet" if slow_weight > no_weight else "no_internet"
            )

        ncr_tweets.append(t)

print("uploading to mongodb...")
# UploadToMongoDB(ncr_tweets)

# with open("output.json", "w") as f:
#     json.dump(ncr_tweets, f, indent=4)
