AUTHOR ABHIRAMJ:
lucene_index_and_search: Driver for running index and search
Input: Output folder for index, limit of number of responsive documents
       and input folder of data
Output:Paths of responsive files

lucene_index: Indexes fresh text data using lucene 3.6. Doesn't support
              updates as of now.
Input: Input folder for text files. output folder for index
Output: void

lucene_search: Search a built index and return upto limit number of responses
Input: Input index folder, limit value, query(as text)
Output: paths of responsive files
