import csv
import os

from GraphQDMR import OperationQDMR as op
from ParserQDMR.GoldParserQDMR import GoldParserQDMR
from ReaderQDMR import GoldReader

####################
# csv operations   #
####################


def get_file_location_at_parent_folder(file_name):
    dirname = os.path.dirname(__file__)
    par_dir = os.path.abspath(os.path.join(dirname, os.pardir))
    input_csv_file = os.path.join(par_dir, file_name)
    return input_csv_file



def save_csv_file(rows, output_csv_file):
    print(f"saving csv to {output_csv_file}")
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for r in rows:
            writer.writerow(r)


###########################
# OPERATORS list filters  #
###########################
"""filter QDMR queries according to their OPERATORS list"""


class Filter:
    """basic filter, that save min&max graph len"""
    def __init__(self, min_len=None, max_len=None):
        if min_len is None:
            self.min_len = 0
        else:
            self.min_len = min_len

        if max_len is None:
            self.max_len = 20
        else:
            self.max_len = max_len

    def has_good_len(self, graph_len):
        if self.min_len <= graph_len <= self.max_len:
            return True
        return False

    def filter(self):
        raise NotImplementedError


class ChainFilter(Filter):

    def __init__(self, operator: op, min_len=None, max_len=None):
        super(ChainFilter, self).__init__(min_len, max_len)
        self.operator = str(operator).lower()
        self.name = "chain_of_" + str(operator)

    @staticmethod
    def get_chain_list(operators, operator):
        """return a list of tuples.
        each tuple represent a chain: the 1st element is the start index of the chain,
                                      the 2nd element is the length of this chain
        e.g: for operators=["filter","filter","select",""filter","filter","filter"] and operator=filter,
        the result is [(0,2),(3,3)]"""
        chains = []
        chain_start_index = 0
        chain_len = 0
        for i, temp_operator in enumerate(operators):
            if temp_operator == operator:
                if chain_len == 0:
                    chain_start_index = i
                chain_len += 1
            else:
                if chain_len >= 2:
                    chains.append((chain_start_index, chain_len))
                chain_len = 0

        if temp_operator == operator and chain_len >= 2:
            chains.append((chain_start_index, chain_len))
        return chains

    @staticmethod
    def detect_chain(operators, operator):
        """check if there is a chain with a single operator"""
        chains = ChainFilter.get_chain_list(operators, operator)
        if chains:  # there are chain/s with this operator
            return True
        return False

    def filter(self, decomposition, operators):
        """returns true if there is a chain of operator self.operator """
        if not self.has_good_len(len(operators)):
            return False
        return ChainFilter.detect_chain(operators, self.operator)


class PermutationFilter(Filter):
    def __init__(self, operators, min_len=None, max_len=None):
        super(PermutationFilter, self).__init__(min_len, max_len)
        self.operator_sublist = [str(operator).lower() for operator in operators]
        self.name = "permutation_of_" + '_'.join(self.operator_sublist)

    def filter(self, decomposition, operators):
        """returns true if self.operators_sublist (or a permutation of it) is a sublist of operators"""
        def all_zeros(d):
            """iterate on a dict, and return True <=> all the keys have value=0"""
            for key in d.keys():
                if d[key] != 0:
                    return False
            return True

        if not self.has_good_len(len(operators)):
            return False


        list_len = len(operators)
        sublist_len = len(self.operator_sublist)
        if sublist_len > list_len:
            return False

        # for each operator from sublist, init appearances to 1
        operator_apperances = {}
        for operator in self.operator_sublist:
            operator_apperances[operator] = 0

        for operator in self.operator_sublist:
            operator_apperances[operator] += 1

        # --iterate on 'operators' with a sliding window--
        # create first window:
        for i in range(sublist_len):
            temp_operator = operators[i]
            if temp_operator in operator_apperances.keys():
                operator_apperances[temp_operator] -= 1
        if all_zeros(operator_apperances):
            return True

        # move with sliding window
        for i in range(len(operators) - sublist_len):
            old_oper = operators[i]
            new_oper = operators[i + sublist_len - 1]
            if old_oper in operator_apperances.keys():
                operator_apperances[old_oper] += 1
            if new_oper in operator_apperances.keys():
                operator_apperances[new_oper] -= 1
            if all_zeros(operator_apperances):
                return True
        return False


class Interesting(Filter):
    """find graphs with interesting operations"""
    boring_operations = [str(op.SELECT).lower(), str(op.FILTER).lower(), str(op.PROJECT).lower(),
                         str(op.AGGREGATE).lower()]

    # at reality, those operators can have 1/2 incoming edge/s
    interesting_operations = [str(op.SUPERLATIVE).lower(), str(op.COMPARATIVE).lower(),
                              str(op.UNION).lower(), str(op.INTERSECTION).lower(), str(op.DISCARD).lower(),
                              str(op.SORT).lower(), str(op.BOOLEAN).lower(), str(op.ARITHMETIC).lower(),
                              ]

    def __init__(self, min_len=None, max_len=None):
        super(Interesting, self).__init__(min_len, max_len)
        self.name = "interesting"
        self.min_interesting_operations = 3

    def filter(self, decomposition, operators):
        """returns true if graph is a 2 head snake """
        if not self.has_good_len(len(operators)):
            return False

        interesting = 0
        for operator in operators:
            if operator in Interesting.interesting_operations:
                interesting += 1
        if interesting >= self.min_interesting_operations:
            return True
        return False


####################
#  graph filters   #
####################
"""filter QDMR queries according to the 'GraphQDMR' object which represents them.
enables filter according to input/output edges, neighbors, paths with certain operators and more"""


class GraphPath(Filter):
    """ return true if Graph has path [operators[0]...operators[n-1]]
    e.g: for input operators=["select","filter"], the graph: [select-->select-->filter] is legit(where --> is an edge)"""

    def __init__(self, operators, min_len=None, max_len=None):
        super(GraphPath, self).__init__(min_len, max_len)
        self.operator_sublist = operators
        self.name = "graphPath_of_" + '_'.join([str(operator).lower() for operator in operators])

    def filter(self, graph):
        def filter_rec(vertice, operator_sublist):
            if vertice.operation != operator_sublist[0]:  # bad operation
                return False

            if len(operator_sublist) == 1:
                return True

            for neighbore in vertice.outgoing:
                if filter_rec(neighbore, operator_sublist[1:]):
                    return True
            return False

        if not self.has_good_len(len(graph.vertices)):
            return False

        vertices = graph.vertices
        for vertice_id, vertice in vertices.items():
            if filter_rec(vertice, self.operator_sublist):
                return True
        return False


class GraphHasNodeWithIncomingEdges(Filter):
    """ return true if Graph has vertice with operator 'self.operator', that has all incoming edges 'self.incomings'
    e.g: creating the filter with parameters "operator=op.COMPARATIVE, incomings=[op.FILTER, op.FILTER]"
    and then applying it on the graph below:
    AGGREGATE----
                |
                V
    FILTER ----> COMPARATIVE                         FILTER---> COMPARATIVE
                ^
                |
    FILTER------

    will return True                                will return False
    """
    def __init__(self, operator, incomings, min_len=None, max_len=None):
        super(GraphHasNodeWithIncomingEdges, self).__init__(min_len, max_len)
        self.operator = operator
        self.incomings = incomings
        self.name = f"graph_has_{str(operator).lower()}_with_inputs_" + '_'.join([str(operator).lower() for operator in incomings])

    def filter(self, graph):
        def has_desiered_incoming_edges(vertice):
            # count the required operators to pass as input edges
            input_operators_apperances = {}
            for operator in self.incomings:
                input_operators_apperances[operator.name] = 0

            for operator in self.incomings:
                input_operators_apperances[operator.name] -= 1

            # count the actual operators from input edges
            for neighbore in vertice.incoming:
                if neighbore.operation.name in input_operators_apperances.keys():
                    input_operators_apperances[neighbore.operation.name] += 1

            # check that actual operators are good enough
            for _, value in input_operators_apperances.items():
                if value < 0:
                    return False
            return True

        vertices = graph.vertices
        for _, vertice in vertices.items():
            if vertice.operation == self.operator and has_desiered_incoming_edges(vertice):
                return True
        return False



####################


class FilterData:
    """ load csv file of gold qdmr questions, filter the questions and save to a new csv file.
     This is useful to test new single vertex/structure Actions"""

    @staticmethod
    def filter_data_according_to_operatorlist(filter, output_csv_file="",
                                              input_csv_file=None):
        """ use this function to active  'graph filter'
        :param filter: a class with "filter" function to apply on questions.
        returns True if question is good(we want to save it), else False
        :param output_csv_file: a path save the result csv file
        :param input_csv_file: a path to the input csv file
        """
        if input_csv_file is None:
            input_csv_file = get_file_location_at_parent_folder(GoldReader.TRAIN_QUESTIONS_FILE_NAME)
        rows = GoldReader.read_file_rows(input_csv_file)
        q = rows[0]
        INDEX_QUESTION = q.index("question_text")
        INDEX_DECOMPOSITION = q.index("decomposition")
        INDEX_OPERATORS = q.index("operators")
        filtered_rows = [q]

        print("start filtering")
        for r in rows[1:]:
            decomposition = r[INDEX_DECOMPOSITION]
            operators = r[INDEX_OPERATORS]
            if not decomposition or not operators:
                continue
            operator_list = GoldParserQDMR.operators_to_list(operators)
            if filter.filter(decomposition, operator_list):  # save the question
                filtered_rows.append(r)

        # save rows to csv file
        print(f"{len(filtered_rows) - 1} questions survived the filter")
        if output_csv_file == "":
            output_csv_file = f"filtered_{filter.name}.csv"
        save_csv_file(filtered_rows, output_csv_file=output_csv_file)

    @staticmethod
    def filter_data_according_to_graph(filter, output_csv_file="", input_csv_file=None):
        """ use this function to active  'operatorList filter'
        :param filter: a class with "filter" function to apply on questions.
        returns True if question is good(we want to save it), else False
        :param output_csv_file: a path save the result csv file
        :param input_csv_file: a path to the input csv file
        """
        if input_csv_file is None:
            input_csv_file = get_file_location_at_parent_folder(GoldReader.TRAIN_QUESTIONS_FILE_NAME)
        rows = GoldReader.read_file_rows(input_csv_file)
        graphs = GoldReader.read_file_qdmr_graphs(input_csv_file)
        q = rows[0]
        filtered_rows = [q]
        print("start filtering")
        for r, graph in zip(rows[1:], graphs):
            if filter.filter(graph):
                filtered_rows.append(r)  # save the question

        # save rows to csv file
        print(f"{len(filtered_rows) - 1} questions survived the filter")
        if output_csv_file == "":
            output_csv_file = f"filtered_{filter.name}.csv"
        save_csv_file(filtered_rows, output_csv_file=output_csv_file)


if '__main__' == __name__:
    # permutation_filter = PermutationFilter([op.SELECT, op.SELECT, op.FILTER, op.FILTER])
    # FilterData.filter_data_according_to_operatorlist(filter=permutation_filter)

    # chain_filter = ChainFilter(op.FILTER)
    # FilterData.filter_data_according_to_operatorlist(filter=chain_filter)

    # interesting = Interesting()
    # FilterData.filter_data_according_to_operatorlist(filter=interesting)

    #with_desiered_incoming_edges = GraphHasNodeWithIncomingEdges(operator=op.COMPARATIVE, incomings=[op.AGGREGATE, op.FILTER])
    #FilterData.filter_data_according_to_graph(filter=with_desiered_incoming_edges, output_csv_file="ron.csv")

    graph_path = GraphPath([op.UNION, op.AGGREGATE])
    FilterData.filter_data_according_to_graph(filter=graph_path, output_csv_file="ron_un_agg.csv")
