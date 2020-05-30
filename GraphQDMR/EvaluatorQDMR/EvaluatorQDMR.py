
from GraphQDMR.UnifyGraphQDMR import UnifyGraphQDMR

from GraphQDMR.EvaluatorQDMR.GraphMatcherQDMR.StringGraphMatcherQDMR import StringGraphMatcherQDMR
from GraphQDMR.EvaluatorQDMR.GraphMatcherQDMR.NormalStringReprGraphMatcherQDMR import NormalStringGraphMatcherQDMR

class EvaluatorQDMR:
    
    SIMPLE_GRAPH_MATCHER    = StringGraphMatcherQDMR
    ADVANCED_GRAPH_MATCHER  = NormalStringGraphMatcherQDMR

    # TODO : Move to 'GraphMatcherQDMR' package
    @staticmethod
    def get_operation_match_score(prediction_graph_qdmr, gold_graph_qdmr):
        prediction_graph_set = prediction_graph_qdmr.get_operators_set()
        gold_graph_set = gold_graph_qdmr.get_operators_set()

        loss_score = 0
        for operation in gold_graph_set.keys():
            if operation in prediction_graph_set:
                loss_score += abs(gold_graph_set[operation] - prediction_graph_set[operation])
            else:
                loss_score += gold_graph_set[operation]

        for operation in prediction_graph_set.keys():
            if operation not in gold_graph_set:
                loss_score += prediction_graph_set[operation]

        return loss_score
    
    @staticmethod
    def evaluate(prediction_graph_qdmr, gold_graph_qdmr, advanced_matcher = ADVANCED_GRAPH_MATCHER):
        unifyer = UnifyGraphQDMR.UnifyGraphQDMR()
        unifyer.apply_vertices_actions(prediction_graph_qdmr)
        if EvaluatorQDMR.SIMPLE_GRAPH_MATCHER.check(prediction_graph_qdmr, gold_graph_qdmr):
            return True
        unifyer.apply_structure_actions(prediction_graph_qdmr)        
        return advanced_matcher.check(prediction_graph_qdmr, gold_graph_qdmr)
