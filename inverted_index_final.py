import json
import argparse
import sys


def load_document(filepath):
    wiki_db = {}
    with open(filepath, encoding="utf8", mode="r") as f:
        for line in f.readlines():
            (article_id, article_name_content) = line.split(maxsplit=1)
            article_name_content = article_name_content.lstrip().rstrip()
            wiki_db[int(article_id)] = article_name_content
    return wiki_db


def build_inverted_index(articles):
    inverted_db = {}
    for key, value in articles.items():
        for word in value.split():
            if inverted_db.get(word) is None and word.strip():
                inverted_db[word] = {key}
            elif word.strip():
                inverted_db[word].add(key)
    return InvertedIndex(inverted_db)


def build(args_obj):
    build_inverted_index(load_document(args_obj.build_infile)).dump(args_obj.build_outfile)
    return None


def print_query(args_obj):
    obj = InvertedIndex.load(args_obj.query_infile)
    with open(args_obj.query_file, 'r') as f:
        for line in f:
            article_ids = sorted(obj.query(line))
            print(*article_ids, sep=',', file=sys.stdout)    # Sending output to screen
    return None


class InvertedIndex:
    def __init__(self, word_to_docs_mapping):
        self.db = word_to_docs_mapping

    def query(self, words):
        article_ids = set()
        if isinstance(words, str):
            words = words.split()
        itr = None
        for itr, word in enumerate(words):
            if not (self.db.get(word) is None):
                article_ids |= self.db[word]
                break
        for word in words[itr + 1:]:
            if not (self.db.get(word) is None):
                article_ids &= self.db[word]
            else:
                article_ids &= set()
        return article_ids

    def dump(self, filepath):
        database = {}
        with open(filepath, mode="w") as f:
            for key, value in self.db.items():
                database[key] = list(value)
            json.dump(database, f)              # Writing json file to disk
        return None

    @classmethod
    def load(cls, filepath):
        with open(filepath, mode="r") as f:
            line = f.readline()
            inverted_db = json.loads(line)
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
