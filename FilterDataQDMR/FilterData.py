import csv
from abc import abstractmethod, ABC

from GraphQDMR import OperationQDMR as op
from ParserQDMR.GoldParserQDMR import GoldParserQDMR
from ReaderQDMR import GoldReader


####################
# possible filters #
####################
class Filter(ABC):
    @abstractmethod
    def filter(self):
        raise NotImplementedError


class ChainFilter(Filter):

    def __init__(self, operator: op):
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
        return ChainFilter.detect_chain(operators, self.operator)


class SublistFilter(Filter):
    def __init__(self, operators):
        self.operator_sublist = [str(operator).lower() for operator in operators]
        self.name = "sublist_of_" + '_'.join(self.operator_sublist)

    def filter(self, decomposition, operators):
        """returns true if self.operators_sublist (or a permutation of it) is a sublist of operators"""

        def all_zeros(d):
            """iterate on a dict, and return True <=> all the keys have value=0"""
            for key in d.keys():
                if d[key] != 0:
                    return False
            return True

        list_len = len(operators)
        sublist_len = len(self.operator_sublist)
        if sublist_len > list_len:
            return False

        # for each operator from sublist, init appearances to 1
        operator_apperances = {}
        for operator in self.operator_sublist:
            operator_apperances[operator] = 1

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
            new_oper = operators[i+sublist_len-1]
            if old_oper in operator_apperances.keys():
                operator_apperances[old_oper] += 1
            if new_oper in operator_apperances.keys():
                operator_apperances[new_oper] -= 1
            if all_zeros(operator_apperances):
                return True
        return False


class Interesting(Filter):
    """find interesting graphs - long graphs with interesting operations"""
    boring_operations = [str(op.SELECT).lower(), str(op.FILTER).lower(), str(op.PROJECT).lower(), str(op.AGGREGATE).lower()]

    # at reality, those operators can have 1/2 incoming edge/s
    interesting_operations = [str(op.SUPERLATIVE).lower(), str(op.COMPARATIVE).lower(),
                                   str(op.UNION).lower(), str(op.INTERSECTION).lower(), str(op.DISCARD).lower(),
                                   str(op.SORT).lower(), str(op.BOOLEAN).lower(),  str(op.ARITHMETIC).lower(),
                                   ]

    def __init__(self):
        self.name = "interesting"
        self.max_len = 8
        self.min_len = 4
        self.min_interesting_operations = 3

    def filter(self, decomposition, operators):
        """returns true if graph is a 2 head snake """
        if len(operators) <= self.min_len or len(operators) > self.max_len:
            return False
        interesting = 0
        for operator in operators:
            if operator in Interesting.interesting_operations:
                interesting += 1
        if interesting >= self.min_interesting_operations:
            return True
        return False

####################
class FilterData:
    """ load csv file of gold qdmr questions, filter the questions and save to a new csv file.
     This is useful to test new single vertex/structure Actions"""




    @staticmethod
    def save_csv_file(rows, output_csv_file):
        print(f"saving csv to {output_csv_file}")
        with open(output_csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            for r in rows:
                writer.writerow(r)

    @staticmethod
    def filter_data(filter, input_csv_file=GoldReader.TRAIN_QUESTIONS_FILE_NAME):
        """
        :param filter: a class with "filter" function to apply on questions.
        returns True if question is good(we want to save it), else False
        :param input_csv_file: a path to the input csv file
        """
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
        print(f"{len(filtered_rows)-1} questions survived the filter")
        FilterData.save_csv_file(filtered_rows, output_csv_file=f"filtered_{filter.name}.csv")


if '__main__' == __name__:

    # sublist_filter = SublistFilter([op.SELECT, op.AGGREGATE])
    # FilterData.filter_data(filter=sublist_filter)

    # chain_filter = ChainFilter(op.PROJECT)
    # FilterData.filter_data(filter=chain_filter)

    interesting = Interesting()
    FilterData.filter_data(filter=interesting)


