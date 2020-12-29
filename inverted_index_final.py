# Uses python3
##################################################
## For detail refer README.md in the main folder
##################################################
## GNU General Public License v3.0
##################################################
## Author: ANURAG GARG
## Copyright: Copyright 2020, Inverted Index.

## Credits: HSE University.

## License: GNU GPL v3.0
## Version: 1.1.0
## Mmaintainer: ANURAG GARG
## Email: mranuraggarg@yahoo.com
## Status: stable
####################################################################################################
import json
import argparse


def load_document(filepath):
    wiki_db = {}
    with open(filepath, encoding="utf8", mode="r") as f:
        for line in f.readlines():
            article_id, article_name_content = line.split(maxsplit=1)
            wiki_db[int(article_id)] = article_name_content.strip()
    return wiki_db


def build_inverted_index(articles):
    inverted_db = {}
    for key, value in articles.items():
        for word in value.split():
            inverted_db.setdefault(word, set()).add(key)
    return InvertedIndex(inverted_db)


def build(args_obj):
    """

    :type args_obj: file
    """
    build_inverted_index(load_document(args_obj.build_infile)).dump(args_obj.build_outfile)
    return None


def print_query(args_obj):
    """

    :type args_obj: file
    """
    inverted_obj = InvertedIndex.load(args_obj.query_infile)
    with open(args_obj.query_file, 'r') as f:
        for line in f:
            article_ids = sorted(inverted_obj.query(line))
            print(*article_ids, sep=',')  # Sending output to screen
    return None


class InvertedIndex:
    def __init__(self, word_to_docs_mapping) -> dict:
        self.db = word_to_docs_mapping

    def query(self, words):
        result = self.db.get(words[0], set()).copy()
        for word in words:
            result &= self.db.get(word, set())
        return result

    def dump(self, filepath):
        """

        :rtype: None
        """
        database = {key: list(value) for key, value in self.db.items()}
        with open(filepath, mode="w") as f:
            json.dump(database, f)  # Writing json file to disk
        return None

    @classmethod
    def load(cls, filepath):
        with open(filepath, mode="r") as f:
            inverted_db = json.loads(f)
            for key, value in inverted_db.items():
                inverted_db[key] = set(value)
        return cls(inverted_db)


# Build Parser
parser = argparse.ArgumentParser()

# Add subparser
subparsers = parser.add_subparsers(help="commands")

# parser "build"
parser_build = subparsers.add_parser('build',
                                     help='dataset help')

parser_build.add_argument('--dataset',
                          dest='build_infile',
                          type=str,
                          action='store',
                          default=True,
                          help='Read the txt file and create inverse index')

parser_build.add_argument('--index',
                          dest='build_outfile',
                          type=str,
                          action='store',
                          help='index help')

# Run function - "build"
parser_build.set_defaults(func=build)

# parser "query"
parser_query = subparsers.add_parser('query',
                                     help='dataset help')

parser_query.add_argument('--index',
                          dest='query_infile',
                          type=str,
                          action='store',
                          help='Read the txt file and create inverse index',
                          default=True)

parser_query.add_argument('--query_file',
                          dest='query_file',
                          type=str,
                          action='store',
                          help='index help')

# Run function - "print_query"
parser_query.set_defaults(func=print_query)

# Parse
args = parser.parse_args()
args.func(args)
