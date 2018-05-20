from apted import APTED, Config


class CustomConfig(Config):
    def rename(self, node1, node2):
        """Compares attribute .value of trees"""
        return 1 if node1.value != node2.value else 0

    def children(self, node):
        """Get left and right children of binary tree"""

        return [x for x in tuple(node.children) if x]


class Node(object):
    def __init__(self, label, value=None):
        """
            Creates a node with the given label.
        """
        self.label = label
        self.value = value
        self.children = list()

    def addkid(self, node, before=False):
        """
            Adds a child node. When the before flag is true, the child node will be inserted at the
            beginning of the list of children, otherwise the child node is appended.
        """
        if before:
            self.children.insert(0, node)
        else:
            self.children.append(node)
        return self


def add_kid(root, items):
    """
        Parses and adds child node to the tree.
    """
    for element in items:
        act = element.__class__.__name__

        try:
            if act is 'FuncCall':
                value = []

                elements = [] if element.args is None else element.args.exprs
                if len(elements) > 0:
                    for arg in elements:
                            value.append(arg.type)
                    node = Node(act, value)
            else:
                node = Node(act)

            root.addkid(node)
        except Exception as e:
            print(e)

        if act is 'FuncDef':
            add_kid(node, element.body.block_items)


def show(tree, counter):
    shift = '    ' * counter

    print(shift, 'Label -->', tree.label)
    print(shift, 'Value -->', tree.value)

    for node in tree.children:
            show(node, counter + 1)


def build_tree(ast):
    """
       Builds more abstract tree. Deletes all vars values. Leaves only code structure.
    """
    tree = Node('root')
    add_kid(tree, ast.ext)

    show(tree, 0)

    return tree


def count_distance(a_ast, b_ast):
    """
       Counts tree edit distance between two ast trees.
    """

    a_ast = build_tree(a_ast)
    b_ast = build_tree(b_ast)

    apted = APTED(a_ast, b_ast, CustomConfig())
    ted = apted.compute_edit_distance()

    return ted

