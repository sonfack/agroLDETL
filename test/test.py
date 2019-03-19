import unittest

from src.agroldETL import serverConnection

# def getDatasetAttributValues(server, dataset, listOfAttributes=['ensembl_gene_id','external_gene_name','description','chromosome_name','start_position', 'end_position','gene_biotype','tair_locus_model','uniprotswissprot','uniprotsptrembl','po_id','po_namespace_1003'], folder='../data', savageFile=None):
# atauschi = server.datasets['atauschii_eg_gene']
# osativa = server.datasets['osativa_eg_gene']
# pp.pprint(osativa.search())
# pp.pprint(atauschi.show_filters())
#athaliana.show_attributes()

class TestAgroldetl(unittest.TestCase):

    def testServerConnection(self):
        self.assertIsNotNone(serverConnection())


if __name__ == '__main__':
    unittest.main()

