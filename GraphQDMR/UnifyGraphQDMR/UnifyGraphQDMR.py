

class UnifyGraphQDMR:
    HOOK_NAME_AFTER_VERTICES_ACTIONS    = 'after_vertices_actions_hook'
    HOOK_NAME_AFTER_STRUCTURE_ACTIONS   = 'after_structure_actions_hook'
    
    VERTICES_ACTIONS    = []
    STRUCTURE_ACTIONS   = []

    def __init__(self, hooks):
        self.hooks = hooks

    def convert(self, graph_qdmr):
        self.apply_vertices_actions(graph_qdmr)
        if self.hooks.get(UnifyGraphQDMR.HOOK_NAME_AFTER_VERTICES_ACTIONS):
            self.hooks[UnifyGraphQDMR.HOOK_NAME_AFTER_VERTICES_ACTIONS]()
        # TODO : Check if graph is a LIST therefore no structure action is possible (SOME CASES)
        self.apply_structure_actions(graph_qdmr)
        if self.hooks.get(UnifyGraphQDMR.HOOK_NAME_AFTER_STRUCTURE_ACTIONS):
            self.hooks[UnifyGraphQDMR.HOOK_NAME_AFTER_STRUCTURE_ACTIONS]()

    def apply_vertices_actions(self, graph_qdmr):
        for vertice_action in UnifyGraphQDMR.VERTICES_ACTIONS:
            vertice_action.apply(graph_qdmr)
    
    def apply_structure_actions(self, graph_qdmr):
        for structure_action in UnifyGraphQDMR.STRUCTURE_ACTIONS:
            structure_action.apply(graph_qdmr)
