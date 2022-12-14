
import sys
from dataclasses import dataclass
import time
from datetime import datetime

@dataclass
class Node:
  name: str
  nbor_names: list[str]
  rate: int
  nbors: list[object] = None
  id: int = None

  def __hash__(self): return hash(self.name)

"""
order of opening doesn't matter
you can open at most 15 valves

one possible soln: find the 15 best valves - determine if possible to open all in time (can assume 15 minutes remaining)
hmm nah, it's not necessarily true that you need to open 15 valves for max release..maybe opening the best 10 is the best you can do under time
"""

@dataclass
class SearchState:
  opened: set[Node]
  my_node: Node
  el_node: Node
  actions: list[str]
  pressure_released:int = 0
  time:int = 0
  total_rate:int = 0

  def clone(self):
    return SearchState(
      opened=set(self.opened),
      my_node=self.my_node,
      el_node=self.el_node,
      actions=list(self.actions),
      pressure_released=self.pressure_released,
      time=self.time,
      total_rate=self.total_rate,
      )

  def __str__(self):
    return ';'.join(self.actions) + ' opened=[' + ",".join(self.opened_names()) + "] t=" + str(self.time) + " p=" + str(self.pressure_released)

  def opened_names(self):
    return [node.name for node in self.opened]

def state_is_worse_or_equal(a:SearchState, b:SearchState):
  """ Only returns true if a is definitely NOT better than b """

  # Can't really say which is worse if they're at different nodes
  # This is actually quite slow, surprisingly.
  # assert a.curr_node() == b.curr_node()

  return a.time >= b.time and a.pressure_released <= b.pressure_released and a.total_rate <= b.total_rate

OPEN = 0
MOVE = 1

def ordpair(a:str, b:str):
  if a <= b:
    return (a, b)
  else:
    return (b, a)

assert ordpair('a', 'b') == ('a', 'b')
assert ordpair('b', 'a') == ('a', 'b')
assert ordpair('a', 'a') == ('a', 'a')

def find_max_release(name2node:dict[str, Node], timing_csvf):
  init_node = name2node['AA']
  init_state = SearchState(opened=set(), my_node=init_node, el_node=init_node, actions=[], time=0)
  states_to_explore:list[SearchState] = [init_state]

  nonzero_valve_names = [node.name for node in name2node.values() if node.rate > 0]

  # Position is an ordered pair of the nodes that the elephant and i are at
  pos2states:dict[(str, str), list[SearchState]] = {}

  best_score = None
  iters = 0
  t0 = time.time()
  total_compares = 0
  while states_to_explore:
    iters += 1
    state:SearchState = states_to_explore.pop(0)

    if iters % 10000 == 0:
      elapsed = time.time() - t0
      print(f'dt={elapsed} iter={iters} stack#={len(states_to_explore)}, state={state}')

      numpasts = 0
      for _, paststates in pos2states.items():
        numpasts += len(paststates)
      avg = numpasts/len(pos2states)
      print(f'  average past states per node: {avg:.2f} for {len(pos2states)} nodes, avg compares per iter: {total_compares/iters:.2f}')

      if timing_csvf:
        timing_csvf.write(f'{elapsed},{iters},{avg}\n')

    # For every other state we've tried at the current node, compare them. If this state is definitely worse than any, no need to explore.
    # Otherwise, explore, and add it to the node's list.

    pos = ordpair(state.my_node.name, state.el_node.name)
    if pos not in pos2states:
      pos2states[pos] = []
    is_pruned = False
    # may be pruned - have to do exhaustive search
    for other in pos2states[pos]:
      # print(f'comparing to {other}')
      total_compares += 1
      if state_is_worse_or_equal(state, other):
        # print(f'pruned!')
        is_pruned = True
        break
    if is_pruned:
      continue

    # Rebuild states, but remove ones which are definitely worse than the new one.
    new_states = [state]
    for other in pos2states[pos]:
      total_compares += 1
      if not state_is_worse_or_equal(other, state):
        new_states.append(other)
    pos2states[pos] = new_states

    if state.time >= 26:
      # Can't explore further.
      if best_score is None or state.pressure_released > best_score:
        best_score = state.pressure_released
        print(f'  improved to {best_score}\n  end state: {state}')
      continue

    # PRUNE: If no more non-zero valves left to open, then just release pressure for remaining time
    if len(state.opened) == len(nonzero_valve_names):
      remain_minutes = 26 - state.time
      extrapolated_pressure = state.pressure_released + state.total_rate * remain_minutes
      if best_score is None or extrapolated_pressure > best_score:
        best_score = extrapolated_pressure
        print(f'  ffwd improved to {best_score} \n  end state: {state}')
      continue

    # Keep exploring from this state

    my_node = state.my_node
    my_actions = [(MOVE, nbor) for nbor in my_node.nbors]
    if my_node.rate > 0 and my_node not in state.opened:
      my_actions.append((OPEN, None))

    for my_action in my_actions:
      # If I do this, what can the elephant do?
      el_node = state.el_node
      el_actions = [(MOVE, nbor) for nbor in el_node.nbors]
      if el_node.rate > 0 and el_node not in state.opened:
        if my_node == el_node and my_action[0] == OPEN:
          # I'm opening this node - elephant cannot
          pass
        else:
          # Elephant can also open its current node
          el_actions.append((OPEN, None))
        
      for el_action in el_actions:
        # Ok, for this action pair, create the resulting state and push it
        new_state = state.clone()
        # Important to do this before a update total_rate after applying open actions, since while opening, we can't use that rate yet!
        new_state.pressure_released += new_state.total_rate
        new_state.time += 1

        if my_action[0] == OPEN:
          new_state.opened.add(my_node)
          new_state.total_rate += my_node.rate
          new_state.actions.append(f'i open {my_node.name}')
        else:
          new_state.my_node = my_action[1]
          new_state.actions.append(f'i goto {my_action[1].name}')

        if el_action[0] == OPEN:
          new_state.opened.add(el_node)
          new_state.total_rate += el_node.rate
          new_state.actions.append(f'el open {el_node.name}')
        else:
          new_state.el_node = el_action[1]
          new_state.actions.append(f'el goto {el_action[1].name}')

        states_to_explore.append(new_state)
        

  print(f'done in {iters} iters, best = {best_score}')
  return best_score

def main(inputf):
  print(f'---- doing {inputf}')
  name2node:dict[str, Node] = {}
  with open(inputf) as f:
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

  # assign IDs
  nodes = name2node.values()
  node2id = {node:i for i, node in enumerate(nodes)}
  for node in nodes:
    node.id = node2id[node]

  with open(f'd16timings/{inputf}-timings-{datetime.now().isoformat()}.csv', 'w') as f:
    return find_max_release(name2node, f)


assert main('d16-leftright.txt') == 48
assert main('d16-leftright-2.txt') == 4642
assert main('d16tiny.txt') == 25
assert main('d16-chain.txt') == 22 * 20
assert main('d16-example-where-opening-BB-first-is-worse.txt') == 24 + 23*20
assert main('d16test.txt') == 1707
assert main('d16real.txt') == 2790

import cProfile
# cProfile.run('assert main("d16test.txt") == 1707')

if len(sys.argv) > 1:
  main(sys.argv[1])