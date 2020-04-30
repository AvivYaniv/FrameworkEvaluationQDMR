from .OperationQDMR import OperationQDMR

class VertexQDMR:
    _operation  =   OperationQDMR.NONE
    
    def __init__(self, operation, step_desc=None):
        self.step_desc  =   [step_desc] if step_desc else [''] # list, to allow multi-operation vertices
        self.operation  =   operation
        self.incoming   =   []
        self.outgoing   =   []

    def set_incoming(self, incoming):
        self.incoming   = incoming
        
    def set_outgoining(self, outgoining):
        self.outgoining = outgoining
    
    def add_incoming(self, in_v):
        self.incoming.append(in_v)
        
    def add_outgoining(self, out_v):
        self.outgoing.append(out_v)
            
    def incoming_gen(self):
        for v in self.incoming:
            yield v
            
    def outgoing_gen(self):
        for v in self.outgoing:
            yield v

    # TODO : Add comparator to sort INcoming vertices list to unify form
    # i.e. Lexicographic comparator
    @staticmethod
    def get_key_for_lexicographic_comparator(vertex):
        return vertex.step_desc[0]

    def __str__(self):
        v_str           = f'{self.vid} : {self.operation} {self.step_desc}'
        incoming_vids   = [ v.vid for v in self.incoming_gen() ]

        if len(self.step_desc) > 1:
            incoming_vids = incoming_vids * len(self.step_desc)

        if incoming_vids:
            v_str = v_str.format(*incoming_vids)
        return v_str
        