def visible():
    return [{'in': {'board': ['O  ', '   ', '   ']}}, {'in': {'board': ['XOX', ' X ', '   ']}}, {'in': {'board': ['XOX', 'O O', 'XOX']}}]

def hidden():
    return [{'in': {'board': ['   ', '   ', '   ']}}, {'in': {'board': ['XXX', '   ', 'OOO']}}, {'in': {'board': ['XXX', 'OO ', '   ']}}, {'in': {'board': ['XXX', 'OO ', 'O  ']}}, {'in': {'board': ['OOO', 'XX ', 'X  ']}}, {'in': {'board': ['OOO', 'XX ', 'XX ']}}, {'in': {'board': ['XXX', 'XOO', 'OO ']}}, {'in': {'board': ['XOX', 'OXO', 'XOX']}}, {'in': {'board': ['OXX', 'XOX', 'OXO']}}]
