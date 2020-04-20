class StringGraphMatcherQDMR:
    @staticmethod
    def check(prediction_graph_qdmr, gold_graph_qdmr):
        return str(prediction_graph_qdmr) == str(gold_graph_qdmr)
    