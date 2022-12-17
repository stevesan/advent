
import sys
from dataclasses import dataclass

@dataclass
class Node:
  name: str
  nbor_names: list[str]
  rate: int
  nbors: list[object] = None

def find_max_release(name2node:dict[str, Node]):
  pass

name2node:dict[str, Node] = {}

with open(sys.argv[1]) as f:
  for line in f:
    line = line.strip()
    """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB"""
    # print(line)
    parts = line.split(' ')
    assert parts[0] == 'Valve'
    name = parts[1]

    ratestr = parts[4]
    assert ratestr[-1] == ';'
    rate = int(ratestr[len('rate='):-1])
    
    assert parts[8] in ['valves', 'valve']
    tunnelstrs = parts[9:]
    nbor_names = [s.replace(',', '') for s in tunnelstrs]

    node = Node(name=name, nbor_names=nbor_names, rate=rate)
    # print(node)
    name2node[name] = node

# hook up nbors
for node in name2node.values():
  nbors = [name2node[name] for name in node.nbor_names]
  node.nbors = nbors

find_max_release(name2node)