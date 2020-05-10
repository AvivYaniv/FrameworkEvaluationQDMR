
from GraphQDMR.EvaluatorQDMR.GraphMatcherQDMR.StringGraphMatcherQDMR import StringGraphMatcherQDMR
from GraphQDMR.UnifyGraphQDMR import UnifyGraphQDMR

class EvaluatorQDMR:

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
    def evaluate(prediction_graph_qdmr, gold_graph_qdmr):
        unifyer = UnifyGraphQDMR() 
        unifyer.apply_vertices_actions(prediction_graph_qdmr)
        # If string match return true
        if StringGraphMatcherQDMR.check(prediction_graph_qdmr, gold_graph_qdmr):
            return True
        unifyer.apply_structure_actions(prediction_graph_qdmr)
        # TODO : Check graph structure, by going on each vertex and check if all incoming vertex descriptions are the same (without comparing numbers, "as-is")
        # More about; switch edges direction, then, go in BFS and check as decribed above


