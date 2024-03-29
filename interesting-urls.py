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
              "config.json",
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
              ".bat",
              ".log",
              ".gem",
              ".txt",
              ".csv",
              ".sql",
              ".bak",
              ".backup",
              ".db",
              ".dump",
              ".old",
              ".tmp",
              ".temp",
              ".access",
              ".aws",
              ".s3cfg",
              ".git",
              ".gitconfig",
              ".github",
              ".docker",
              ".env",
              ".test",
              ".rar",
              ".raw",
              ".zip",
              ".tgz",
              "config.js",
              "configuration.js",
              "constants.js"]

static_extensions = [".html",
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
        "git",
        "svn",
        "cgi-bin",
        "bin",
        "proxy",
        "test",
        "debug",
        "tmp",
        "temp",
        "private",
        "config",
        "configuration",
        "docker",
        "dockerfile"]

    url_paths = PurePosixPath(
        unquote(
            urlparse(
                url.lower()
            ).path
        )
    ).parts

    for path in paths:
        if path in url_paths:
            return True

    return False


def has_interesting_query_strings(url) -> bool:
    keys = ["debug",
            "password",
            "passwd",
            "file",
            "fn",
            "template",
            "include",
            "require",
            "config",
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
                url.lower()
            ).path
        )
    ).parts

    if not url_paths:
        return False

    last_element = url_paths[-1]

    # no extension, ends with path
    if "." not in last_element:
        return False

    for ext in extensions:
        if url.endswith(ext):
            return False
    for ext in static_extensions:
        if url.endswith(ext):
            return False

    return True


def is_js_extension(url) -> bool:
    url = remove_query_params_and_fragment(url)

    url_paths = PurePosixPath(
        unquote(
            urlparse(
                url.lower()
            ).path
        )
    ).parts

    if not url_paths:
        return False

    last_element = url_paths[-1]

    # no extension, ends with path
    if "." not in last_element:
        return False

    if url.endswith(".js"):
        return True

    return False


def find_unknown_extensions(urls) -> None:
    for url in urls:

        parsed_url = re.search("(?P<url>https?://[^\s]+)", url)
        if parsed_url is not None:
            parsed_url = parsed_url.group("url")
        else:
            continue
        parsed_url = parsed_url.lower().strip('\n')

        if is_unknown_extension(parsed_url):
            print(parsed_url)

def find_js_extensions(urls) -> None:
    for url in urls:

        parsed_url = re.search("(?P<url>https?://[^\s]+)", url)
        if parsed_url is not None:
            parsed_url = parsed_url.group("url")
        else:
            continue
        parsed_url = parsed_url.lower().strip('\n')

        if is_js_extension(parsed_url):
            print(parsed_url)


def search_urls(urls) -> None:
    for url in urls:

        parsed_url = re.search("(?P<url>https?://[^\s]+)", url)
        if parsed_url is not None:
            parsed_url = parsed_url.group("url")
        else:
            continue
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
    parser.add_argument("-j", "--js", dest="js", help="Just kidding! I want all js files")
    parser.add_argument("-u", "--unknown", dest="unknown", help="Print unknown extensions")

    args = parser.parse_args()

    if len(sys.argv) < 2:
        parser.print_help()
        exit(1)

    with open(args.file, "r") as input_file:
        urls = input_file.readlines()

    if args.js is not None:
        find_js_extensions(urls)
    elif args.unknown is not None:
        find_unknown_extensions(urls)
    else:
        search_urls(urls)


if __name__ == "__main__":
    main()
