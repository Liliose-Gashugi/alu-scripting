#!/usr/bin/python3
"""Prints the titles of the first 10 hot posts of a subreddit."""
import requests


def top_ten(subreddit):
    """Print the first 10 hot post titles, or None if the subreddit is invalid."""
    url = "https://www.reddit.com/r/{}/hot.json?limit=10".format(subreddit)
    headers = {"User-Agent": "linux:alu.api_advanced:v1.0 (by /u/alu_student)"}
    try:
        response = requests.get(url, headers=headers, allow_redirects=False,
                                timeout=10)
        if response.status_code != 200:
            print(None)
            return
        posts = response.json().get("data", {}).get("children", [])
        for post in posts[:10]:
            print(post.get("data", {}).get("title"))
    except (requests.RequestException, ValueError):
        print(None)
