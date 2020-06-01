from collections import Counter
from copy import copy

from FilterDataQDMR.FilterData import save_csv_file, get_file_location_at_parent_folder
from ParserQDMR import *
from ReaderQDMR.GoldReader import GoldReader


def get_word_operators(word, create_csv_file=True, input_csv_file=None):
    """1. print operators histogram on steps that contain the word
       2. create a csv file, with steps that contains the word """

    if input_csv_file is None:
        input_csv_file = get_file_location_at_parent_folder(GoldReader.TRAIN_QUESTIONS_FILE_NAME)
    output_csv_file = word + ".csv"

    rows = GoldReader.read_file_rows(input_csv_file)
    q = rows[0]
    INDEX_DECOMPOSITION = q.index("decomposition")
    INDEX_OPERATORS = q.index("operators")
    filtered_rows = [q]

    # init operator counter
    operators_counter = Counter([])

    print("start filtering")
    for r in rows[1:]:
        decomposition = r[INDEX_DECOMPOSITION]
        operators = r[INDEX_OPERATORS]
        if not decomposition or not operators:
            continue
        operator_list = GoldParserQDMR.operators_to_list(operators)

        steps = decomposition.split(";")
        word_indices = [i for i, step in enumerate(steps) if word in step]
        steps_with_word = [step for i, step in enumerate(steps) if word in step]
        word_operators = [operator_list[i] for i in word_indices]

        for step, operator in zip(steps_with_word, word_operators):
            r = copy(r)
            r = [r[0]]  # keep only the question_id
            r.append(operator)
            r.append(step.replace("  ", " "))
            filtered_rows.append(r)

        # update operators_counter
        for step, operator in zip(steps_with_word, word_operators):
            operators_counter.update([operator])

    # print operators_counter:
    print(f"===== {word} =====\nall step types: {len(filtered_rows)}:")
    for op_name, op_count in operators_counter.items():
        print(f"  {op_name} : {op_count}")

    if create_csv_file:
        save_csv_file(filtered_rows, output_csv_file=output_csv_file)

if '__main__' == __name__:
    interesting_word = "the"
    get_word_operators(interesting_word)

