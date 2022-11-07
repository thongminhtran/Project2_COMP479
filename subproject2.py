
import json
import re
import sys

index = json.load(open('indexes/index.json', 'r'))

def GettingDocumentByID(doc_id):
    file_number = int(doc_id) // 1000
    file_number_str = str(file_number) if file_number > 9 else '0' + str(file_number)
    file_path = 'reuters21578/reut2-0' + file_number_str + '.sgm'          # Creating path files
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        file_content = f.read()     # Reading content of the file

        doc_regex = r'<REUTERS.* NEWID="' + doc_id + r'">(.*?)</REUTERS>'
        document = re.findall(doc_regex, file_content, flags=re.DOTALL)[0]

        body_regex = r"<BODY>(.*?)</BODY>"
        document_body = re.findall(body_regex, document, flags=re.DOTALL)[0]
        return document_body


def ValidatingQuery(query):
    processedQuery = QueryProcesssing(query)

    if processedQuery is None:
        return None
    freq, DOCIDS = processedQuery
    for doc_id in DOCIDS:
        CheckingQueryByID(query, doc_id)
    return processedQuery


def QueryProcesssing(query):

    if query not in index:
        print('The query is not in the index!')
        return None
    return index[query]



def ValidatingAllQueries():
    all_queries = json.load(open('Queries_List/queries_to_validate.json', 'r'))    # Reading Queries_List
    for query in all_queries:               # Using for loop to validate each query
        print(f' {query} query is being validated...')
        result = ValidatingQuery(query)
        if result is None:
            print(f'"{query}" query cannot be found in the index!!!')
        else:
            count, documents = result            # Initialize docs as 'result'
            print(f'There are "{query}" that be found in {count} documents:')
            print(documents)
    return f'Every {all_queries} has been validated successfully.'


def CheckingQueryByID(query, doc_id):
    document = GettingDocumentByID(doc_id)
    assert query in document, "The Query cannot be found!!!"


if __name__ == '__main__':

    if len(sys.argv) == 1:
        sys.exit('Please enter the query term: ')
    arg = sys.argv[1]
    if arg == 'doc':
        doc_id = sys.argv[2]
        if doc_id is None:
            print('Please enter the docID: ')
            sys.exit(0)
        sys.exit(GettingDocumentByID(doc_id))
    elif arg == 'qval':
        sys.exit(ValidatingAllQueries())
    else:
        query = arg
        result = ValidatingQuery(query)
        if result:
            count, DOCIDS = result
            print(f'The query has been found in {count} documents')
            print(DOCIDS)
    sys.exit(0)