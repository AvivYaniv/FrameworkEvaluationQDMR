
from GraphQDMR.EvaluatorQDMR.GraphMatcherQDMR.StringGraphMatcherQDMR import StringGraphMatcherQDMR
from GraphQDMR.UnifyGraphQDMR import UnifyGraphQDMR

class EvaluatorQDR:
    @staticmethod
    def evaluate(prediction_graph_qdmr, gold_graph_qdmr):
        unifyer = UnifyGraphQDMR() 
        unifyer.apply_vertices_actions(prediction_graph_qdmr)
        # If string match return true
        if StringGraphMatcherQDMR.check(prediction_graph_qdmr, gold_graph_qdmr):
            return True
        unifyer.apply_structure_actions(prediction_graph_qdmr)
        # TODO : Check graph structure, by going on each vertex and check if all incoming vertex descriptions are the same (without comparing numbers, "as-is")
        # More about; switch edges direction, then, go in BFS and check as decribed above