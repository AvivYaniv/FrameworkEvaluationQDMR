# FilterDataQDMR
This package helps to filter the data. The following modules are included:
<br />
<br />**1. FilterData.py** - filter the data according to operators list /graph structure. examples:
<br />example1: save graphs with at least 3 operations from([SELECT, BOOLEAN]), and the graph has <= 7 vertices
<br />example2: save graphs with 'COMPARATIVE' operator vertex which has incoming 'AGGREGATE' and 'FILTER' edges
<br />example3: save graphs with chain of FILTERS of len >=2
<br />
<br />**2. get_operator_desc.py** - for any chosen operator:
<br />    - creates a csv file, with the questions that corresponds to the operator
<br />    - creates a csv file, with the steps the corresponds to the operator
<br />
<br />**3. get_word_operators.py** - for any chosen word/string -
<br />    - print operators histogram on steps that contain the word
<br />    - create a csv file, with steps that contains the word """

