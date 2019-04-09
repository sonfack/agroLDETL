import os
import sys
import pprint
import itertools
import pandas as pd
from biomart import BiomartServer
from lxml import etree
import xml.etree.ElementTree as ET

# redirect sys.stdout to a buffer
import sys, io
from datetime import datetime

nowDate = datetime.now()
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
def getDatasetAttributValues(server, dataset, listOfAttributes=['ensembl_gene_id','external_gene_name','description'], folder='./data', savageFile= nowDate.strftime('%Y-%m-%d-%H-%M-%S-%f')):
    if not os.path.exists(folder+'/'+dataset):
        os.mkdir(folder+'/'+dataset)
        print("Directory ", folder+'/'+dataset, " Created ")
    else:
        print("Directory ", folder+'/'+dataset, " already exists")
    datasetName = server.datasets[dataset]
    datasetName.show_attributes()
    response = datasetName.search({'attributes': listOfAttributes})
    if savageFile is not None:
        f = open(os.path.join(folder+'/'+dataset, savageFile), 'w+')
        f.write('==> '+ dataset + ' <==' + os.linesep)
        f.write('\t'.join(listOfAttributes) + os.linesep)
        for line in response.iter_lines():
            line = line.decode('utf-8')
            f.write(line + os.linesep)
        f.close()
    else:
        responseValues = []
        for line in response.iter_lines():
            line = line.decode('utf-8')
            responseValues.append(line)
        return responseValues

'''
Returns a dictionary of pages and their attributes, also returns all the pages existing for the give dataset
'''
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

def chunks(list, n=10):
    for i in range(0, len(list), n):
        yield list[i:i+n]


def getAllValuesOfAllAttributesOfADataset(server, dataset, filter, numberOfChunks=10, folder='./data'):
    if not os.path.exists(folder+'/'+dataset):
        os.mkdir(folder+'/'+dataset)
        print("Directory ", folder+'/'+dataset, " Created ")
    else:
        print("Directory ", folder+'/'+dataset, " already exists")
    listOfSelectedPageAndAttributes, allAttributes = getAllAttributesOfADatasetWithTheirPage(server, dataset)
    for page, listAttributes in listOfSelectedPageAndAttributes.items():
        listOfUseAttributes = []
        responseValues = []
        print(responseValues)
        print('******************************************************')
        print(page)
        print('******************************************************')
        print(listAttributes)
        print('******************************************************')
        if filter is not None:
            filterInListAttributes = [attrib for attrib in filter if attrib in listAttributes]
            chunkListOfAttributes = list(chunks(filterInListAttributes, numberOfChunks))
            for chunkAttribute in chunkListOfAttributes:
                listOfUseAttributes = itertools.chain(listOfUseAttributes, chunkAttribute)
                resValue = getDatasetAttributValues(server, dataset, listOfAttributes=chunkAttribute)
                if resValue is not None:
                    responseValues.append(resValue)
            f = open(os.path.join(folder+'/'+dataset, page), 'w')
            f.write('\t'.join(listOfUseAttributes))
            f.write('\n')
            if len(responseValues) > 0 :
                print(responseValues)
                for i in range(len(responseValues[0])):
                    for j in range(len(responseValues)):
                        f.write(responseValues[j][i])
                        f.write('\t')
                    f.write('\n')
            f.close()
        else:
            chunkListOfAttributes = list(chunks(listAttributes, numberOfChunks))
            for chunkAttribute in chunkListOfAttributes:
                listOfUseAttributes = itertools.chain(listOfUseAttributes, chunkAttribute)
                responseValues.append(getDatasetAttributValues(server, dataset, listOfAttributes=chunkAttribute))
                print('******************************************************')
                print(listOfUseAttributes)
                print('******************************************************')
                print(responseValues)
                print('******************************************************')
            #exit(0)

    return responseValues, filter


def createDataFrameFromFilterAndResponseValues(filter, responseValues, fileName='dataset'):
    print(len(filter))
    print(len(responseValues))
    for i in range(len(responseValues)):
        print(len(responseValues[i]))


    #dicOfData = {attribute:listResponse for attribute, listResponse in zip(filter, responseValues)}
    #print(dicOfData)
    #df = pd.DataFrame(dicOfData)
    #print(df)



#def main():



    #getAllAttributesOfADatasetWithTheirPage(server, dataset)



    #exit(0)
    #getAllAttributesOfADataset(server, dataset)
    #getDatasetAttributValues(server, dataset,savageFile='test.txt')
    #print(getAllDatasets(server))

#if __name__ == '__main__':
#    main()
