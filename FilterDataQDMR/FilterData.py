import csv
import os

from GraphQDMR import OperationQDMR as op, OperationQDMR
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

#####################
# Filter base class #
#####################


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


###########################
# OPERATORS list filters  #
###########################
"""filter QDMR queries according to their OPERATORS list"""


class Interesting(Filter):
    """find graphs with interesting operations"""

    def __init__(self, interesting_operations: OperationQDMR,
                 min_len=None, max_len=None, min_interesting_operations=None):
        super(Interesting, self).__init__(min_len, max_len)
        self.name = "interesting"

        if min_interesting_operations:
            self.min_interesting_operations = min_interesting_operations
        else:
            self.min_interesting_operations = 1

        self.interesting_operations = [str(op).lower() for op in interesting_operations]  # convert to string

    def filter(self, decomposition, operators):
        """returns true if graph is a 2 head snake """
        if not self.has_good_len(len(operators)):
            return False

        interesting = 0
        for operator in operators:
            if operator in self.interesting_operations:
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
    """examples of how to use the code above"""

    # example1: save graphs with at least 3 operations from([SELECT, BOOLEAN]), and the len of the graph is <= 7
    interesting = Interesting([op.SELECT, op.BOOLEAN], min_interesting_operations=3, max_len=7)
    FilterData.filter_data_according_to_operatorlist(filter=interesting)

    # example2: save graphs with 'COMPARATIVE' operator vertex which has incoming 'AGGREGATE' and 'FILTER' edges
    with_desiered_incoming_edges = GraphHasNodeWithIncomingEdges(operator=op.COMPARATIVE, incomings=[op.AGGREGATE, op.FILTER])
    FilterData.filter_data_according_to_graph(filter=with_desiered_incoming_edges, output_csv_file="ron.csv")

    # example3: save graphs with chain of FILTERS of len >=2
    graph_path = GraphPath([op.FILTER, op.FILTER])
    FilterData.filter_data_according_to_graph(filter=graph_path)
