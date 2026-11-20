#!/usr/bin/python3
"""Recursively counts keywords in the titles of a subreddit's hot posts."""
import requests


def print_counts(counts):
    """Print counts by descending count, then alphabetically."""
    for word, number in sorted(counts.items(), key=lambda i: (-i[1], i[0])):
        print("{}: {}".format(word, number))


def count_words(subreddit, word_list, after=None, counts=None):
    """Print a sorted count of keywords found in hot post titles."""
    if counts is None:
        counts = {}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {"User-Agent": "linux:alu.api_advanced:v1.0 (by /u/alu_student)"}
    params = {"limit": 100, "after": after}
    try:
        response = requests.get(url, headers=headers, params=params,
                                allow_redirects=False, timeout=10)
        if response.status_code != 200:
            data = None
        else:
            data = response.json().get("data", {})
    except (requests.RequestException, ValueError):
        data = None
    if data is None:
        print_counts(counts)
        return
    wanted = {}
    for word in word_list:
        wanted[word.lower()] = wanted.get(word.lower(), 0) + 1
    for post in data.get("children", []):
        title = post.get("data", {}).get("title", "")
        for word in title.lower().split():
            if word in wanted:
                counts[word] = counts.get(word, 0) + wanted[word]
    after = data.get("after")
    if after is None:
        print_counts(counts)
        return
    count_words(subreddit, word_list, after, counts)
