from .. import OperationQDMR as op

from .SemanticPreservativeVertexAction import SortVertexAttributes
from .SemanticPreservativeStructureAction import UnifyFilterChains


class UnifyGraphQDMR:
    HOOK_NAME_AFTER_VERTICES_ACTIONS    = 'after_vertices_actions_hook'
    HOOK_NAME_AFTER_STRUCTURE_ACTIONS   = 'after_structure_actions_hook'
    
    VERTICES_ACTIONS    = [ SortVertexAttributes() ]
    STRUCTURE_ACTIONS   = [ UnifyFilterChains() ]

    def __init__(self, hooks={}):
        self.hooks = hooks

    def invoke_hook(self, hook_name):
        if self.hooks.get(hook_name):
            self.hooks[hook_name]()

    def convert(self, graph_qdmr):
        # TODO : Check if graph is a LIST therefore no vertex action is possible (commutative action requires more than one argument)
        self.apply_vertices_actions(graph_qdmr)
        self.invoke_hook(UnifyGraphQDMR.HOOK_NAME_AFTER_VERTICES_ACTIONS)
        # TODO : Check if graph is a LIST therefore no structure action is possible (SOME CASES)
        self.apply_structure_actions(graph_qdmr)
        self.invoke_hook(UnifyGraphQDMR.HOOK_NAME_AFTER_STRUCTURE_ACTIONS)

    def apply_vertices_actions(self, graph_qdmr):
        for vertice_action in UnifyGraphQDMR.VERTICES_ACTIONS:
            vertice_action.apply(graph_qdmr)
    
    def apply_structure_actions(self, graph_qdmr):
        for structure_action in UnifyGraphQDMR.STRUCTURE_ACTIONS:
            structure_action.apply(graph_qdmr)
