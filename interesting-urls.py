#!/usr/bin/python3
import re
import sys
from argparse import ArgumentParser
from urllib.parse import urlsplit, parse_qs, urlparse, unquote
from pathlib import PurePosixPath


def has_extension(url) -> bool:
    extensions = [".cs",
                  ".vb",
                  ".cgi",
                  ".pl",
                  ".json",
                  ".xml",
                  ".rb",
                  ".py",
                  ".sh",
                  ".yaml",
                  ".yml",
                  ".ini",
                  ".md",
                  ".mkd"
                  ]

    for ext in extensions:
        if url.endswith(ext):
            return True

    return False


def contains_path(url) -> bool:
    paths = [
        "ajax"
        "jsonp",
        "admin",
        "include",
        "src",
        "redirect",
        "proxy",
        "test",
        "debug",
        "tmp",
        "temp",
        "private"]

    url_paths = PurePosixPath(
        unquote(
            urlparse(
                url
            ).path
        )
    ).parts

    for path in paths:
        if path in url_paths:
            return True

    return False


def has_interesting_query_strings(url) -> bool:
    keys = ["redirect",
            "debug",
            "password",
            "passwd",
            "file",
            "fn",
            "template",
            "include",
            "require",
            "url",
            "uri",
            "src",
            "href",
            "func",
            "callback"]

    values = ["http",
              "https",
              "{",
              "[",
              "/",
              "\\",
              "<",
              "("]

    query = urlsplit(url).query
    params = parse_qs(query)

    if params:
        for key, value in params.items():
            if key in keys:
                return True

            for v in value:
                if v in values:
                    return True

    return False


def is_static_file(url) -> bool:
    extensions = [".js",
                  ".html",
                  ".htm",
                  ".svg",
                  ".eot",
                  ".ttf",
                  ".woff",
                  ".woff2",
                  ".png",
                  ".jpg",
                  ".jpeg",
                  ".gif",
                  ".ico"]

    for ext in extensions:
        if url.endswith(ext):
            return True

    return False


def search_urls(urls) -> None:
    for url in urls:

        parsed_url = re.search("(?P<url>https?://[^\s]+)", url).group("url")
        parsed_url = parsed_url.lower().strip('\n')

        if not is_static_file(url):
            if has_extension(parsed_url):
                print(parsed_url)

            if contains_path(parsed_url):
                print(parsed_url)

            if has_interesting_query_strings(parsed_url):
                print(parsed_url)


def main() -> None:
    """
    Main program
    """
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", dest="file", help="File containing list of URLs")

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        exit(1)

    if args.file is not None:
        with open(args.file, "r") as input_file:
            urls = input_file.readlines()

    search_urls(urls)


if __name__ == "__main__":
    main()
