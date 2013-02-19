import os
from lucene import IndexWriter, StandardAnalyzer, Document, Field, LimitTokenCountAnalyzer
from lucene import SimpleFSDirectory, File, initVM, Version
from lucene import IndexSearcher, QueryParser
from preprocess.utils_email import parse_plain_text_email 
from file_utils import find_files_in_folder


def index_files(input_dir, writer):
    
    for root, _, filenames in os.walk(input_dir):
        for filename in filenames:

            path = os.path.join(root, filename)
            print "  File: ", filename

            fp = open(path)
            contents = unicode(fp.read(), 'iso-8859-1')
            fp.close()
            doc = Document()
            doc.add(Field("name", filename, Field.Store.YES, Field.Index.NOT_ANALYZED, Field.TermVector.YES))
            doc.add(Field("path", path, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
            if len(contents) > 0:
                doc.add(Field("contents", contents, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.YES))
            else:
                print "warning: no content in %s" % filename

            writer.addDocument(doc)




def index_plain_text_emails(input_dir, writer, store_dir):
    
    file_tuples = find_files_in_folder(input_dir)
    file_paths = os.path.join(store_dir, 'index.file_paths')
    # Stores the email paths into a text 
    # file for future reference 
    with open(file_paths, 'w') as fw:
        for idx, ft in enumerate(file_tuples): 
            root, file_name = ft
            print >>fw, idx, root, file_name
    
    for idx, ft in enumerate(file_tuples): 
        root, file_name = ft

        file_path = os.path.join(root, file_name)
        print "  File: ", file_name
        
        # parses the emails in plain text format 
        receiver, sender, cc, subject, message_text = parse_plain_text_email(file_path)

        doc = Document()
        doc.add(Field("file_name", file_name, Field.Store.YES, Field.Index.NOT_ANALYZED, Field.TermVector.YES))
        doc.add(Field("file_path", file_path, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(Field("message_receiver", receiver, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(Field("message_sender", sender, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(Field("message_cc", cc, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        doc.add(Field("message_subject", subject, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.WITH_POSITIONS_OFFSETS))
        if len(message_text) > 0:
            doc.add(Field("message_body", message_text, Field.Store.YES, Field.Index.ANALYZED, Field.TermVector.YES))
        else:
            print "warning: no content in %s" % file_name

        writer.addDocument(doc)



if __name__ == '__main__':

#    if len(sys.argv) != 3:
#        print "Usage: python lucene_index_dir.py <input dir> <store dir>"
#
#    else:
        
    input_dir = '/home/cgeorge/ediscovey/enron_mail_20110402/maildir' # sys.argv[1]
    store_dir = '/home/cgeorge/ediscovey/enron_mail_20110402/lucene_index'# sys.argv[2]
    
    if not os.path.exists(store_dir): 
        os.mkdir(store_dir)
    
    initVM()
    store = SimpleFSDirectory(File(store_dir))
    analyzer = LimitTokenCountAnalyzer(StandardAnalyzer(Version.LUCENE_CURRENT), 1048576)
        
        
    # Index emails  
    
    writer = IndexWriter(store, analyzer, True, IndexWriter.MaxFieldLength.LIMITED)
    index_plain_text_emails(input_dir, writer, store_dir)
    writer.commit()
    writer.close()



#        searcher = IndexSearcher(store, True)
#        parser = QueryParser(Version.LUCENE_CURRENT, "keywords", analyzer)
#        parser.setDefaultOperator(QueryParser.Operator.AND)
#        query = parser.parse('profit fraud terminate enron')
#        start = datetime.now()
#        scoreDocs = searcher.search(query, 50).scoreDocs
#        duration = datetime.now() - start
#
#        print "Found %d document(s) (in %s) that matched query '%s':" %(len(scoreDocs), duration, query)
#        
#        for scoreDoc in scoreDocs:
#            doc = searcher.doc(scoreDoc.doc)
#            table = dict((field.name(), field.stringValue())
#                         for field in doc.getFields())
#            print template.substitute(table)






