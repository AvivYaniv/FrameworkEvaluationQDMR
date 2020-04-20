import uuid

class GraphQDMR:
    def __init__(self):
        self.vertices   =   {}
    
    def get_vids(self):
        return self.vertices.keys()
    
    def get_operations(self):
        return [v.operation for v in self.vertices]
    
    def get_operations_histogram(self):
        operations_histogram = {}
        for v in self.vertices.values():
            if v.operation not in operations_histogram.keys():
                operations_histogram[v.operation] = 0
            operations_histogram[v.operation] += 1
        return operations_histogram
        
    def add_vertex(self, v):
        v.vid                   = 1 + len(self.vertices.keys()) # uuid.uuid4()
        self.vertices[v.vid]    = v
        return v.vid
        
    def add_edge(self, vid_in, vid_out):
        v_in        =   self.vertices.get(vid_in,   None)
        v_out       =   self.vertices.get(vid_out,  None)
        # If either vertex not found
        if None in [v_in, v_out]:
            return False
        v_in.add_outgoining(v_out)
        v_out.add_incoming(v_in)
        return True
    
    def swap_vertices_step_decs(self, vid_1, vid_2):
        v_1         =   self.vertices.get(vid_1,    None)
        v_2         =   self.vertices.get(vid_2,    None)
        # If either vertex not found
        if None in [v_1, v_2]:
            return False        
        temp_desc       = v_1.step_desc
        v_1.step_desc   = v_2.step_desc
        v_2.step_desc   = temp_desc
        return True
    
    def adj_list_str(self):
        graph_str = ''
        for v_id, v in self.vertices.items():
            graph_str += f'Adjacency list of vertex {v_id}\n' 
            for n in v.outgoing_gen(): 
                graph_str += f' -> {n.vid}'                
            graph_str += '\n'
        return graph_str
    
    def __str__(self):
        graph_str = ''
        for v in self.vertices.values():
            graph_str += f'{v.vid} : {v.operation} [{v}]\n'
        return graph_str
    