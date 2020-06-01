import textwrap

from GraphQDMR import GraphQDMR, VertexQDMR
from GraphQDMR.CanonicalizerQDMR.CanonicalizerQDMR import CanonicalizerQDMR


class NormalStringReprBuilderQDMR:
    def __init__(self, qdmr: GraphQDMR, multiline=False):
        self.qdmr = qdmr
        self.refs = {}

        self.multiline = multiline

    def _get_root(self) -> VertexQDMR:
        return self.qdmr.vertices[max(self.qdmr.get_vids())]

        """root = None

        for v in self.qdmr.vertices_gen():
            outgoing = list(v.outgoing_gen())

            if len(outgoing) == 0:
                if root is not None:  # already found one
                    raise Exception("Logical Error: QDMR contains more than one root"
                                    " - More than one vertex in QDMR has 0 outgoing edges")
                root = v

        if root is None:
            raise Exception("Logical Error: QDMR contains zero roots"
                            " - No vertex in QDMR has 0 outgoing edges")
        return root"""

    def indent(self, s):
        if not self.multiline:
            return s

        return textwrap.indent(s, '  ')

    def next(self):
        if not self.multiline:
            return " "

        return "\n"

    def _build_arg(self, u: VertexQDMR):
        if u in self.refs:
            return "{ " + str(self.refs[u]) + " }"

        arg = "{" + self.next()
        arg += self.indent(self._build(u))
        arg += self.next() + "}"

        return arg

    def _build_descs(self, v: VertexQDMR):
        formatted_descs = []

        for desc in v.step_desc:
            desc = CanonicalizerQDMR.canonicalize(desc, remove_references=False, remove_stopwords=True)  # canonicalize desc
            args = (self._build_arg(u) for u in v.incoming)
            formatted_desc = desc.replace(" {", self.next() + "{").replace("} ", "}" + self.next()) \
                .format(*args)

            formatted_descs.append(formatted_desc)

        return ", ".join(formatted_descs)

    def _build(self, v: VertexQDMR):
        self.refs[v] = len(self.refs)

        s = f'{v.operation} ({self.refs[v]}) [' + self.next()
        s += self.indent(self._build_descs(v))
        s += self.next() + ']'

        return s

    def build(self):
        root = self._get_root()
        s = self._build(root)
        self.refs = {}  # reset refs for additional uses

        return s


class NormalStringGraphMatcherQDMR:
    @staticmethod
    def check(prediction_graph_qdmr, gold_graph_qdmr):
        return NormalStringReprBuilderQDMR(prediction_graph_qdmr, multiline=False).build() \
               == NormalStringReprBuilderQDMR(gold_graph_qdmr, multiline=False).build()
