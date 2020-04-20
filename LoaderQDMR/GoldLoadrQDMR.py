import re

from GraphQDMR.GraphQDMR import GraphQDMR
from GraphQDMR.VertexQDMR import VertexQDMR
from GraphQDMR.OperationQDMR import OperationQDMR

class GoldLoadrQDMR:
    GOLD_TOKEN_SPLITTER =   ';'
    
    REFERENCE_REGEXP    =   r'#\d+'
    
    TARGET_REFERENCE    =   '{}'
    
    @staticmethod
    def decomposition_to_list(decomposition):
        return decomposition.split(GoldLoadrQDMR.GOLD_TOKEN_SPLITTER)
    
    @staticmethod
    def parse_decomposition(raw_decomposition):
        return re.sub(GoldLoadrQDMR.REFERENCE_REGEXP, GoldLoadrQDMR.TARGET_REFERENCE, raw_decomposition)
    
    @staticmethod
    def parse_operator(raw_operator):
        return OperationQDMR[raw_operator.upper()]
    
    @staticmethod
    def parse_incoming(raw_decomposition):
        return [int(m[1:]) for m in re.findall(GoldLoadrQDMR.REFERENCE_REGEXP, raw_decomposition)]
        
    @staticmethod
    def load(decomposition, operators_list):
        decomposition_list = GoldLoadrQDMR.decomposition_to_list(decomposition)
        # If decompositions and operators lengths are not the same
        if len(decomposition_list) != len(operators_list):
            print('Error! decomposition and operators mismatch')
        # Create the QDMR graph
        graph = GraphQDMR()
        # Building the QDMR graph according to input
        for raw_decomposition, operator in zip(decomposition_list, operators_list):
            v = VertexQDMR(                                             \
                GoldLoadrQDMR.parse_operator(operator),                 \
                GoldLoadrQDMR.parse_decomposition(raw_decomposition))
            vid_out = graph.add_vertex(v)
            for vid_in in GoldLoadrQDMR.parse_incoming(raw_decomposition):
                graph.add_edge(vid_in, vid_out)
        return graph
        