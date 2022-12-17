
import sys
from dataclasses import dataclass

@dataclass
class Node:
  name: str
  nbor_names: list[str]
  rate: int
  nbors: list[object] = None

"""
order of opening doesn't matter
you can open at most 15 valves

one possible soln: find the 15 best valves - determine if possible to open all in time (can assume 15 minutes remaining)
hmm nah, it's not necessarily true that you need to open 15 valves for max release..maybe opening the best 10 is the best you can do under time
"""

@dataclass
class SearchState:
  opened: list[Node]
  path: list[Node]
  def curr_node(self): return self.path[-1]
  def get_time(self):
    return len(self.path) - 1 + len(self.opened)
  def get_score(self):
    return sum([node.rate for node in self.opened])
  def clone(self):
    return SearchState(opened=list(self.opened), path=list(self.path))

@dataclass
class SearchAction:
  start_state: SearchState
  type: str # 'move' to dest or 'open' current valve
  move_dest: Node = None

def find_max_release(name2node:dict[str, Node]):
  init_node = name2node['AA']
  init_state = SearchState(opened=[], path=[init_node])
  action_stack:list[SearchAction] = []

  def push_actions_from(state:SearchState):
    node = state.path[-1]
    if not state.curr_node() in state.opened:
      open_action = SearchAction(start_state=state, type='open')
      action_stack.append(open_action)
    for nbor in node.nbors:
      # Note we need to allow moving to previously visited nodes. For the dead-end case.
      move_action = SearchAction(start_state=state, type='move', move_dest=nbor)
      action_stack.append(move_action)

  push_actions_from(init_state)
  best_score = None
  while action_stack:
    # Apply the action to get the new state. If we're out of time, update best_score. If not, generate further actions.
    action = action_stack.pop(-1)
    new_state = action.start_state.clone()
    if action.type == 'open':
      new_state.opened.append(new_state.curr_node())
    else:
      assert action.type == 'move' and action.move_dest
      new_state.path.append(action.move_dest)

    if new_state.get_time() >= 30:
      if best_score is None or new_state.get_score() > best_score:
        best_score = new_state.get_score()
    else:
      push_actions_from(new_state)

  print(best_score)
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