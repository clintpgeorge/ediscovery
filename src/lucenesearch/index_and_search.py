#!/usr/bin/env python

import argparse
from lucenesearch.lucene_index import lucene_index
from lucenesearch.lucene_search import lucene_search

if __name__ == "__main__":
    

 
    arg_parser = argparse.ArgumentParser(description='Lucene index and search')
    arg_parser.add_argument("-d", dest="input_folder", type=str,
                            help="The root directory to index and search",
                             required=True)
    arg_parser.add_argument("-o", dest="output_folder", type=str, help="Output directory of index",
                         default="/home/abhiramj/code/temp/index",
                         required=False)
    arg_parser.add_argument("-q", dest="query_text", type=str, help="Query to search for")
    arg_parser.add_argument("-l", dest="limit", type=int, help="Maximum number of results")
    
    args = arg_parser.parse_args()
    lucene_index(args.input_folder,args.output_folder)
    responsive = lucene_search(args.output_folder, args.limit, args.query_text)
    