def visible():
    return [{'in': {'expression': '{a,b}{c,{d,e}}'}}, {'in': {'expression': '{{a,z},a{b,c},{ab,z}}'}}, {'in': {'expression': 'pre{x,y}post'}}]

def hidden():
    return [{'in': {'expression': 'a'}}, {'in': {'expression': '{a}'}}, {'in': {'expression': '{a,a,a}'}}, {'in': {'expression': '{a,b}c{d,e}'}}, {'in': {'expression': 'a{b,{c,d}}e'}}, {'in': {'expression': '{a,b}{b,a}'}}, {'in': {'expression': '{{a,b},{b,c}}'}}, {'in': {'expression': 'x{a{b,c},d{e,f}}y'}}, {'in': {'expression': '{a,b,c}{d,{e,f}}{g,h}{i,{j,k}}'}}]
