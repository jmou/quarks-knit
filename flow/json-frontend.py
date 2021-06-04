import base64
import json
import pickle
import sys


nodes = json.load(sys.stdin)

for node in nodes:
    if node['node_type'] == 'ROOT':
        print('_pos=main')
        print(f'_source={node["name"]}')
        print('process=identity')
        # XXX hardcoded terminals
        # for terminal in ['004', '005', '007', '008']:
        for terminal in ['004', '005', '007']:
            print(f'in/{terminal}/=_pos:{terminal}:out/')
    elif node['node_type'] == 'SCRIPT':
        print(f'_pos={node["id"]}')
        print(f'_source={node["name"]}')
        # description

        print('process=command:cp -R in/root/* . && python3 in/driver.py && (cp *.png out || true)')
        print('in/driver.py=file:flow/driver.py')
        print(f'in/file=file:flow/scripts/{node["entryFile"]}')
        print(f'in/fn=inline:{node["entry"]}')

        # XXX hardcoded implicit dependency
        print('in/root/dummy=inline:')
        if node['id'] == '001':
            print('in/root/test.png=file:flow/test.png')
    else:
        raise Exception('Unknown node_type', node['node_type'])

    # requires
    # inquires

    for i, input_ in enumerate(node['inputs']):
        name = input_['name']
        if input_['sourceNode']:
            print(f'in/inputs/{i:03}-{name}=_pos:{input_["sourceNode"]}:out/{input_["sourceName"]}')
        else:
            value = input_['default']
            if value is not None:
                # XXX cast type?
                encoded = base64.b64encode(pickle.dumps(value)).decode('ascii')
                print(f'in/inputs/{i:03}-{name}=inline:{encoded}')

    outputs = ';'.join(f'{o["name"]}:{o["type"]}' for o in node['outputs'])
    print(f'in/outputs=inline:{outputs}')

    # isInputNode
    # isOutputNode

    # nextNode determines the execution path from the root.

    print()
