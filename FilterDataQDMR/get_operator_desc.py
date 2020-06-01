from copy import copy

from FilterDataQDMR.FilterData import save_csv_file, get_file_location_at_parent_folder, GraphPath, FilterData
from GraphQDMR import *
from GraphQDMR.UnifyGraphQDMR.SemanticPreservativeStructureAction import *
from GraphQDMR.EvaluatorQDMR.GraphMatcherQDMR.NormalStringReprGraphMatcherQDMR import *
from GraphQDMR.UnifyGraphQDMR.UnifyGraphQDMR import UnifyGraphQDMR
from VisualizerQDMR import *
from ParserQDMR import *
from ReaderQDMR.GoldReader import GoldReader
from GraphQDMR.EvaluatorQDMR.GraphMatcherQDMR.PropotionalGraphMatcherQDMR import PropotionalGraphMatcherQDMR


def get_operator_desc(op : OperationQDMR):
    """
    creates a csv file, with the questions that corresponds to the operator
    creates a csv file, with the steps the corresponds to the operator
    """

    operator = str.lower(op.name)
    input_csv_file = "questions_with_operator_" + operator + ".csv"  # a file, that each row contains the operator
    output_csv_file = "steps_with_operator_" + operator + ".csv"

    # create temp file that contains all the questions with the operator
    graph_path = GraphPath([op])
    FilterData.filter_data_according_to_graph(filter=graph_path, output_csv_file=input_csv_file)

    rows = GoldReader.read_file_rows(input_csv_file)
    q = rows[0]
    INDEX_QUESTION = q.index("question_text")
    INDEX_DECOMPOSITION = q.index("decomposition")
    INDEX_OPERATORS = q.index("operators")
    filtered_rows = [["question_id", "step_decomposition"]]

    print("start filtering")
    for r in rows[1:]:
        decomposition = r[INDEX_DECOMPOSITION]
        operators = r[INDEX_OPERATORS]
        if not decomposition or not operators:
            continue
        operator_list = GoldParserQDMR.operators_to_list(operators)

        operator_indices = [i for i, step_operator in enumerate(operator_list) if operator == step_operator]
        operator_decompositions = [decomposition.split(";")[i] for i in operator_indices]
        for operator_decomposition in operator_decompositions:
            operator_decomposition = operator_decomposition.replace("  ", " ")
            r = copy(r)
            r[1] = operator_decomposition
            r = r[0:2]
            filtered_rows.append(r)

    save_csv_file(filtered_rows, output_csv_file=output_csv_file)
    print(f"{len(filtered_rows)} steps survived the filter")

if '__main__' == __name__:
    # active on all possible operators:
    # for op in OperationQDMR:
    #     get_operator_desc(op)

    # active on a single operator:
    op = OperationQDMR.AGGREGATE
    get_operator_desc(op)


