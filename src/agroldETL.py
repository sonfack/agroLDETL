import os
import sys
import pprint
from biomart import BiomartServer
from lxml import etree
import xml.etree.ElementTree as ET

# redirect sys.stdout to a buffer
import sys, io

pp = pprint.PrettyPrinter(indent=4)
def serverConnection(proxy=None, verbose=True):
    server = BiomartServer("http://ensembl.gramene.org/biomart")
    # if you are behind a proxy
    if proxy is not None:
        server.http_proxy = os.environ.get('http_proxy', proxy)
    # set verbose to True to get some messages
    server.verbose = verbose
    return server

# Interact with the biomart server
def getAllDatasets(server):
    stdout = sys.stdout
    sys.stdout = io.StringIO()
    #
    server.show_datasets()
    # get output and restore sys.stdout
    output = sys.stdout.getvalue()
    sys.stdout = stdout
    dumpData = output.split('{')[1]
    print(dumpData)
    print('\n\n')
    dumpDataset = dumpData.split(',')
    dumpDataset = [x.strip("\n") for x in dumpDataset]
    listDataset = []
    for element in dumpDataset:
        listElement = element.split(':')
        listElement = [ element.strip().strip(" \'' ").strip().strip('}') for element in listElement]
        listDataset.append(':'.join(listElement))
    return listDataset

def getAllAttributesOfADataset(server,dataset):
    data = server.datasets[dataset]
    stdout = sys.stdout
    sys.stdout = io.StringIO()
    #
    data.show_attributes()
    # get output and restore sys.stdout
    output = sys.stdout.getvalue()
    sys.stdout = stdout
    print('\n')
    dumpData = output.split('{')[1]
    dumpData = dumpData.split('\n')
    dumpdataset = [x.replace("'","").strip(',').strip('}') for x in dumpData]
    return dumpdataset

# exple of dataset : 'athaliana_eg_gene'
def getDatasetAttributValues(server, dataset, listOfAttributes=['ensembl_gene_id','external_gene_name','description'], folder='../data', savageFile=None):
    datasetName = server.datasets[dataset]
    datasetName.show_attributes()
    #exit(0)
    response = datasetName.search({'attributes': listOfAttributes})
    if savageFile is not None:
        f = open(os.path.join(folder, savageFile), 'w+')
        f.write('==> '+ dataset + ' <==' + os.linesep)
        f.write('\t'.join(listOfAttributes) + os.linesep)
        for line in response.iter_lines():
            line = line.decode('utf-8')
            f.write(line + os.linesep)
        f.close()
    else:
        for line in response.iter_lines():
            line = line.decode('utf-8')
            print(line)


def getAllAttributesOfADatasetWithTheirPage(server, dataset):
    dumpData = getAllAttributesOfADataset(server,dataset)
    listOfSelectedPage = {}
    listOfAttribute = []
    for element in dumpData:
        element = element.split('page:')
        if len(element) >=2:
            attribute = element[0].split(':')
            attribute = attribute[0].strip()
            element = element[1].split(',')
            element = element[0].strip()
            if element not in listOfSelectedPage:
                listOfAttribute.append(element)
                listOfSelectedPage[element] = [attribute]
            else:
                listOfSelectedPage[element].append(attribute)

    return listOfSelectedPage, listOfAttribute

def main():
    server = serverConnection(verbose=True)
    dataset='athaliana_eg_gene'
    getAllAttributesOfADatasetWithTheirPage(server, dataset)
    exit(0)
    #getAllAttributesOfADataset(server, dataset)
    getDatasetAttributValues(server, dataset,savageFile='test.txt')
    #print(getAllDatasets(server))

if __name__ == '__main__':
    main()
