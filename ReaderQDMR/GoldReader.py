import csv
from ParserQDMR.GoldParserQDMR import GoldParserQDMR

class GoldReader:
    TRAIN_QUESTIONS_FILE_NAME     = 'train.csv'    
    @staticmethod
    def read_file_rows(fname):
        questions = []
        with open(fname, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                questions.append(row)
        return questions
    
    @staticmethod
    def read_file_qdmr_graphs(fname):
        rows    = GoldReader.read_file_rows(fname)
        graphs  = []
        q = rows[0]
        INDEX_QUESTION              = q.index("question_text")
        INDEX_DECOMPOSITION         = q.index("decomposition")
        INDEX_OPERATORS             = q.index("operators")
        for r in rows[1:]:
            decomposition           = r[INDEX_DECOMPOSITION]
            operators               = r[INDEX_OPERATORS]
            if not decomposition or not operators:
                continue
            qdmr_graph              = GoldParserQDMR.parse(decomposition, operators)
            qdmr_graph.raw_question = r[INDEX_QUESTION]
            graphs.append(qdmr_graph)
        return graphs
