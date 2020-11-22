#!/usr/bin/env python


from datetime import datetime
import html
import json
import re
from string import Template
import sys

import requests
from tinydb import TinyDB, Query


POST_URL_API = Template("https://hacker-news.firebaseio.com/v0/item/$id_.json")
POST_URL_WEB = Template("https://news.ycombinator.com/item?id=$id_")

THREAD_ID = 24969524  # November 2020
DB_FILE = "posts.json"


db = TinyDB(DB_FILE)


def hn_fetch(url):
    return json.loads(requests.get(url).content)


def db_all():
    return db.all()


def db_visible():
    return db.search(Query().visible == True)


def format_text(text):
    # remove explicit newlines in source
    text = text.replace("\n", " ")

    # unescape all HTML
    text = html.unescape(text)

    # remove i tags
    text = text.replace("<i>", "")
    text = text.replace("</i>", "")

    # remove b tags
    text = text.replace("<b>", "")
    text = text.replace("</b>", "")

    # remove pre tags
    text = text.replace("<pre>", "")
    text = text.replace("</pre>", "")

    # remove code tags
    text = text.replace("<code>", "")
    text = text.replace("</code>", "")

    # replace p tags with carriage returns
    text = text.replace("<p>", "\n\n")
    text = text.replace("</p>", "\n\n")

    # remove a tags
    text = text.replace('<a href="', "")
    text = re.sub(r'" rel="nofollow">[^>]*<\/a>', "", text)

    return text


def db_insert(hn_id, visible, author, text):
    return db.insert(
        {
            "hn_id": hn_id,
            "visible": visible,
            "author": author,
            "text": text,
        }
    )


def db_hide(doc_ids):
    db.update({"visible": False}, doc_ids=doc_ids)


def cmd_update():
    # fetch all child post IDs
    thread_data = hn_fetch(POST_URL_API.substitute(id_=THREAD_ID))
    all_ids = thread_data["kids"]
    print(f"Found {len(all_ids)} posts via API.")

    # open DB with existing ones
    known_ids = [post["hn_id"] for post in db_all()]
    print(f"Found {len(known_ids)} posts in DB.")

    for post_id in all_ids:
        print(f"Checking post {post_id}.")
        if post_id not in known_ids:
            print(f"Post {post_id} is new.")
            post_data = hn_fetch(POST_URL_API.substitute(id_=post_id))

            # only snek matters
            visible = False
            if "python" in post_data.get("text", "").lower():
                print(f"Post {post_id} is relevant.")
                visible = True

            doc_id = db_insert(
                hn_id=post_id,
                visible=visible,
                author=post_data.get("by"),
                text=post_data.get("text"),
            )

            print(f"Post {post_id} has a doc_id of {doc_id}.")


def print_report(visible_count: int, total_count: int, posts: list):
    print("----------")
    print()
    print(f"Visible: {visible_count} | Total: {total_count}")
    print()
    print("----------")

    for idx, post in enumerate(posts):
        print()
        print(
            f"{post.doc_id}"
            " | "
            f"{post['hn_id']}"
            " | "
            f"{post['author']}"
            " | "
            f"{POST_URL_WEB.substitute(id_=post['hn_id'])}"
        )
        print()
        print(format_text(post["text"]))
        print()
        print("----------")


def cmd_report():
    total_count = len(db_all())

    posts = db_visible()
    visible_count = len(posts)

    print_report(visible_count, total_count, posts)


def cmd_hide():
    doc_ids = [int(id_str) for id_str in sys.argv[2].split(",")]
    db_hide(doc_ids)


if __name__ == "__main__":
    try:
        command = sys.argv[1]

    # probably encountered when running python -i wihparse.py
    except IndexError:
        print("No command found, entering interactive mode.")

    else:
        function_name = f"cmd_{command}"
        function = locals()[function_name]
        function()
