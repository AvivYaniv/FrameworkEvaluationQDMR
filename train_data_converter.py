from FilterDataQDMR.FilterData import save_csv_file
from GraphQDMR import *
from GraphQDMR.UnifyGraphQDMR.SemanticPreservativeStructureAction import *
from GraphQDMR.EvaluatorQDMR.GraphMatcherQDMR.NormalStringReprGraphMatcherQDMR import *
from GraphQDMR.UnifyGraphQDMR.UnifyGraphQDMR import UnifyGraphQDMR
from VisualizerQDMR import *
from ParserQDMR import *
from ReaderQDMR.GoldReader import GoldReader
from GraphQDMR.EvaluatorQDMR.GraphMatcherQDMR.PropotionalGraphMatcherQDMR import PropotionalGraphMatcherQDMR

if '__main__' == __name__:
    input_csv_file = "train.csv"
    output_csv_file = "train_result.csv"

    DECOMPOSITION_INDEX = 2  # index inside the question
    OPERATOR_INDEX = 3  # index inside the question

    graphs = GoldReader.read_file_qdmr_graphs(input_csv_file)
    rows = GoldReader.read_file_rows(input_csv_file)
    unify = UnifyGraphQDMR()
    [unify.convert(g) for g in graphs]
    for row, graph in zip(rows[1:], graphs):
        row[DECOMPOSITION_INDEX] = graph.decomposition_for_train()
        row[OPERATOR_INDEX] = graph.operators_for_train()

    save_csv_file(rows, output_csv_file)
