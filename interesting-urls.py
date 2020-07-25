#!/usr/bin/python3
import re
import sys
from argparse import ArgumentParser
from urllib.parse import urlsplit, urlunsplit, parse_qs, urlparse, unquote
from pathlib import PurePosixPath


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
                  ".mkd",
                  ".config",
                  ".conf",
                  ".cfg",
                  ".ps1",
                  ".bat"]

static_extensions = [".js",
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


def remove_query_params_and_fragment(url):
    return urlunsplit(urlsplit(url)._replace(query="", fragment=""))


def has_extension(url) -> bool:
    url = remove_query_params_and_fragment(url)

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
            "callback",
            "secret",
            "hash",
            "java",
            "jdk",
            "sdk"]

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
    url = remove_query_params_and_fragment(url)

    for ext in static_extensions:
        if url.endswith(ext):
            return True

    return False


def is_unknown_extension(url) -> bool:
    url = remove_query_params_and_fragment(url)

    url_paths = PurePosixPath(
        unquote(
            urlparse(
                url
            ).path
        )
    ).parts

    if not url_paths:
        return False

    last_element = url_paths[-1]

    # no extension, ends with path
    if not "." in last_element:
        return False

    for ext in extensions:
        if url.endswith(ext):
            return False
    for ext in static_extensions:
        if url.endswith(ext):
            return False

    return True


def find_unknown_extensions(urls) -> None:
    for url in urls:

        parsed_url = re.search("(?P<url>https?://[^\s]+)", url).group("url")
        parsed_url = parsed_url.lower().strip('\n')

        if is_unknown_extension(parsed_url):
            print(parsed_url)


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
    parser.add_argument("-f", "--file", dest="file", help="File containing list of URLs", required=True)
    parser.add_argument("-u", "--unknown", dest="unknown", help="Print unknown extensions")

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        exit(1)

    with open(args.file, "r") as input_file:
        urls = input_file.readlines()

    if args.unknown is not None:
        find_unknown_extensions(urls)
    else:
        search_urls(urls)


if __name__ == "__main__":
    main()
