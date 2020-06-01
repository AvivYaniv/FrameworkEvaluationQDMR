import re
import ast

from GraphQDMR.GraphQDMR import GraphQDMR
from GraphQDMR.VertexQDMR import VertexQDMR
from GraphQDMR.OperationQDMR import OperationQDMR

class GoldParserQDMR:
    GOLD_TOKEN_SPLITTER     =   ';'
    
    REFERACE_PREFIX         =   '#'
    REFERACE_PREFIX_LENGTH  =   len(REFERACE_PREFIX)
    
    REFERENCE_REGEXP        =   REFERACE_PREFIX + r'\d+'
    
    TARGET_REFERENCE        =   '{}'
    
    @staticmethod
    def operators_to_list(operators):
        return ast.literal_eval(operators)
    
    @staticmethod
    def decomposition_to_list(decomposition):
        return decomposition.split(GoldParserQDMR.GOLD_TOKEN_SPLITTER)
    
    @staticmethod
    def parse_decomposition(raw_decomposition):
        return re.sub(GoldParserQDMR.REFERENCE_REGEXP, GoldParserQDMR.TARGET_REFERENCE, raw_decomposition)
    
    @staticmethod
    def parse_operator(raw_operator):
        return OperationQDMR[raw_operator.upper()]
    
    @staticmethod
    def parse_incoming(raw_decomposition):
        return [int(m[GoldParserQDMR.REFERACE_PREFIX_LENGTH:]) for m in re.findall(GoldParserQDMR.REFERENCE_REGEXP, raw_decomposition)]
        
    @staticmethod
    def parse(decomposition, operators, i=None):
        operators_list      = GoldParserQDMR.operators_to_list(operators)
        decomposition_list  = GoldParserQDMR.decomposition_to_list(decomposition)
        # If decompositions and operators lengths are not the same
        if len(decomposition_list) != len(operators_list):
            print('Error! decomposition and operators mismatch')
        # Create the QDMR graph
        graph = GraphQDMR()
        # Building the QDMR graph according to input
        for raw_decomposition, operator in zip(decomposition_list, operators_list):
            v = VertexQDMR(                                             \
                GoldParserQDMR.parse_operator(operator),                \
                GoldParserQDMR.parse_decomposition(raw_decomposition))
            vid_out = graph.add_vertex(v)
            for vid_in in GoldParserQDMR.parse_incoming(raw_decomposition):
                graph.add_edge(vid_in, vid_out)
        return graph
        