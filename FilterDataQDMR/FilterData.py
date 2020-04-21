import csv
from abc import abstractmethod, ABC

from GraphQDMR import OperationQDMR
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

    def __init__(self, operator: OperationQDMR):
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
    def __init__(self, operators):  #: [OperationQDMR]
        self.operator_sublist = [str(operator).lower() for operator in operators]
        self.name = "sublist_of_" + '_'.join(self.operator_sublist)

    def filter(self, decomposition, operators):
        """returns true if self.operators_sublist (or a permutation of it) is a sublist of operators"""
        # give each operator from the sublist a unique number
        unique_numbers = {}
        sublist_len = len(self.operator_sublist)
        for i, operator in enumerate(self.operator_sublist):
            unique_numbers[operator] = 2**i

        # calculate the sum of the sublist
        permutation_expected_sum = 2 ** sublist_len - 1

        # convert the 'operators' list to numbers, according to the unique_numbers
        operators_as_numbers = [unique_numbers.get(operator, 0) for operator in operators]

        # for any possible start index, calculate the sum of 'sublist_len' adjacent numbers.
        # this sum will be equal to 'permutation_expected_sum' only if they are permutation of one another.
        for i in range(len(operators) - sublist_len):
            if sum(operators_as_numbers[i:i+sublist_len]) == permutation_expected_sum:
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

    sublist_filter = SublistFilter([OperationQDMR.SELECT, OperationQDMR.AGGREGATE])
    FilterData.filter_data(filter=sublist_filter)

    chain_filter = ChainFilter(OperationQDMR.FILTER)
    FilterData.filter_data(filter=chain_filter)

