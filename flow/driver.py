import ast
import base64
import os
import pickle


def slurp(path):
    with open(path) as fh:
        return fh.read().strip()


source = ast.parse(slurp('in/file'))
context = {}
eval(compile(source, '<string>', 'exec'), context)

inputs = []
try:
    inputs = sorted(os.listdir('in/inputs'))
except FileNotFoundError:
    pass

call = slurp('in/fn')
call += '('
for i, infile in enumerate(inputs):
    if i != 0:
        call += ', '
    var = infile.split('-', 1)[-1]
    context[var] = pickle.loads(base64.b64decode(slurp(f'in/inputs/{infile}')))
    # XXX type?
    # call += slurp(f'in/inputs/{infile}')
    call += var
call += ')'
# XXX
# result = eval(compile(expr, '<string>', 'eval'), context)
result = eval(call, context)

outputs = [o.split(':') for o in slurp('in/outputs').split(';')]
# XXX empty outputs
if outputs == [['']] and result is None:
    outputs = []
    result = []
if len(outputs) == 1:
    result = [result]
for output, value in zip(outputs, result):
    with open(f'out/{output[0]}', 'w') as fh:
        # XXX write bytes?
        fh.write(base64.b64encode(pickle.dumps(value)).decode('ascii'))
