import os
import xml.etree.ElementTree as ET
import pandas as pd

def process(input_path = None,  output_path=None, filename=None):
    if input_path is None:
        input_path = "testcase/"
    if output_path is None:
        output_path = input_path
    if filename is None:
        filename = "export.xml"
    if "xml" not in filename:
        xml_filename = filename + ".xml"
    else:
        xml_filename = filename
    csv_filename = xml_filename[:-4] + '.csv'
    #reformat the paths
    input_path = os.path.abspath(input_path)
    input_path = os.path.join(input_path, xml_filename)

    output_path = os.path.abspath(output_path)
    output_path = os.path.join(output_path, csv_filename)

    if os.path.exists(output_path):
        os.remove(output_path)

    etree = ET.parse(input_path)
    doc_df = pd.DataFrame(list(iter_docs(etree.getroot())))
    # turn off chained_assignment to suppress copy warning
    pd.options.mode.chained_assignment = None
    # get slice
    docdate = doc_df[['sourceName', 'type', 'startDate', 'value', 'unit']]
    # extract date
    docdate['startDate'] = docdate['startDate'].str.split(pat=None, expand=True)[0]
    # transform to numeric to use + operator
    docdate['value'] = pd.to_numeric(docdate['value'], errors='coerce')
    # rename
    docdate = docdate.rename(columns={'sourceName':'User',
                                      'type':'Activity',
                                      'startDate':'Date',
                                      'value':'Count',
                                      'unit':'Unit'})
    # count the count
    docdatesum = docdate.groupby(['User', 'Activity', 'Date', 'Unit'])[['Count']].sum()
    # transform groupby object with multiple index to a new object with 1 index and multiple columns
    docdatesum = docdatesum.reset_index()
    #write to csv
    docdatesum.to_csv(output_path, sep=',',
                      encoding='utf-8', header=True,
                      columns=['User', 'Activity', 'Date', 'Count', 'Unit'])
    return output_path

def iter_docs(docs):
    for doc in docs:
        if doc.tag == 'Record':
            yield doc.attrib
        else:
            continue

if __name__ == "__main__":
    process()
    print("done")
