
from GraphQDMR.CanonicalizerQDMR.CanonicalizerQDMR import CanonicalizerQDMR

# TODO : TaBaLiZe!
class PropotionalGraphMatcherQDMR:
    
    @staticmethod
    def match_vertices(lPrediction, lGold):
        return (lPrediction.operation == lGold.operation) and \
               (CanonicalizerQDMR.canonicalize(lPrediction.step_desc) == CanonicalizerQDMR.canonicalize(lGold.step_desc))
    
    def match_vertices_lists(self, prediction_leafs, gold_leafs, with_child=False):
        matched_leafs = []
        for lPrediction in prediction_leafs:
            for lGold in gold_leafs:                
                if lPrediction.vid in self.sMatched:
                    continue 
                if not PropotionalGraphMatcherQDMR.match_vertices(lPrediction, lGold):
                    continue
                if with_child:
                    matched_childs = self.match_vertices_lists(lPrediction.outgoing, lGold.outgoing)
                    if len(matched_childs) != len(lPrediction.outgoing): 
                        continue
                matched_leafs.append((lPrediction, lGold))                
        return matched_leafs
    
    def _find_strain_matches(self, lPrediction, lGold):
        self.sMatched.add(lPrediction.vid)                 
        matched_childs =                                        \
            self.match_vertices_lists(                          \
                lPrediction.outgoing,                           \
                lGold.outgoing)
        for lPrediction, lGold in matched_childs:                    
            self._find_strain_matches(lPrediction, lGold)            
                
    def check(self, prediction_graph_qdmr, gold_graph_qdmr):
        # Create sets for matched vertices in prediction graph
        self.sMatched       = set()
        self.sUnMatched     = set()
        # Get leafs of prediction and gold
        lPredicionLeafs     = prediction_graph_qdmr.get_leafs()
        lGoldLeafs          = gold_graph_qdmr.get_leafs()
        # Get matched leafs
        matched_leafs       = self.match_vertices_lists(lPredicionLeafs, lGoldLeafs, True)
        # Find matching vertices
        for lPrediction, lGold in matched_leafs:            
            self._find_strain_matches(lPrediction, lGold)  
        # Loss is matched vertices proportion to gold vertices number
        return len(self.sMatched) / len(gold_graph_qdmr.vertices)
    