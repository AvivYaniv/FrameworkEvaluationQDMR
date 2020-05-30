from .OperationQDMR import OperationQDMR

from GraphQDMR.CanonicalizerQDMR.CanonicalizerQDMR import CanonicalizerQDMR

class VertexQDMR:
    def __init__(self, operation: OperationQDMR, step_desc=None):
        self.step_desc  =   [step_desc] if step_desc else ['']  # list, to allow multi-operation vertices
        self.operation  =   operation
        self.incoming   =   []
        self.outgoing   =   []

        self.vid = -1  # Would be updated after adding to the graph

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

    def merge_step_desc(self, new_step_desc):
        self.step_desc.extend(new_step_desc)
        self.step_desc.sort()

    # TODO : Add comparator to sort INcoming vertices list to unify form
    # i.e. Lexicographic comparator
    @staticmethod
    def get_key_for_lexicographic_comparator(vertex):
        return vertex.step_desc[0]

    @staticmethod
    def compare(v1, v2):
        """
        Comparision by canonicalized form, to avoid considering stop-words prefixes
        i.e. Non-canonicalized comparision would fail to determine the following as equal on
        'the sabich' Vs. 'sabich'
        ...thus non-canonicalized comparision is errounous
        """
        v1_desc = CanonicalizerQDMR.canonicalize(v1.step_desc[0])
        v2_desc = CanonicalizerQDMR.canonicalize(v2.step_desc[0])
        if v1_desc < v2_desc:
            return -1
        if v1_desc > v2_desc:
            return 1
        else:
            len_incoming1 = len(v1.incoming)
            len_incoming2 = len(v2.incoming)
            if len_incoming1 != len_incoming2:
                return len_incoming1 - len_incoming2
            else:
                if len_incoming1 == 0 and len_incoming2 == 0:
                    return 0
                else:
                    incoming_copy1 = list(v1.incoming)
                    incoming_copy2 = list(v2.incoming)
                    incoming_copy1.sort(key = VertexQDMR.get_key_for_lexicographic_comparator)
                    incoming_copy2.sort(key = VertexQDMR.get_key_for_lexicographic_comparator)
                    return VertexQDMR.compare(incoming_copy1[0], incoming_copy2[0])

    def __repr__(self):
        return self.__str__()

    def decomposition_for_train(self):
        """ vertice representation for train_data_converter.py"""
        v_str           = f'{self.step_desc}'
        incoming_vids   = [ v.vid for v in self.incoming_gen() ]

        if len(self.step_desc) > 1:
            incoming_vids = incoming_vids * len(self.step_desc)

        if incoming_vids:
            incoming_vids = [f'#{vid}' for vid in incoming_vids]
            v_str = v_str.format(*incoming_vids)
        return v_str.replace("[", "").replace("]", "").replace("'", "")


    def __str__(self):
        v_str           = f'{self.vid} : {self.operation} {self.step_desc}'
        incoming_vids   = [ v.vid for v in self.incoming_gen() ]

        if len(self.step_desc) > 1:
            incoming_vids = incoming_vids * len(self.step_desc)

        if incoming_vids:
            try:
                v_str = v_str.format(*incoming_vids)
            except IndexError:
                v_str = v_str.format(*incoming_vids + [self.vid])
        return v_str
        