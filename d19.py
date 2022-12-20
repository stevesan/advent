from enum import Enum
from dataclasses import dataclass

class Resource(Enum):
  ORE = 1
  CLAY = 2
  OBSIDIAN = 3
  GEODE = 4

def max_num_geodes_possible(robot_to_costs:dict[Resource, dict[Resource, int]]):
  return 0

@dataclass
class Blueprint(object):
  id: int
  bot2costs: list[list[int]]

  def get_cost(self, bot:Resource, resource:Resource):
    assert resource != Resource.GEODE
    return self.bot2costs[bot.value-1][resource.value-1]

def main(filep):
  blueprints: list[Blueprint] = []
  with open(filep, 'r') as f:
    for line in f:
      header, costs = line.split(':')
      bp, idstr = header.split(' ')
      assert bp == 'Blueprint'
      id = int(idstr)
      botcost_strs = costs.split('.')

      bot2costs: list[list[int]] = [None] * 4
      for s in botcost_strs:
        if s.strip() == '': continue
        bottypestr, res_costs = s.split('costs')
        _, eachstr, bottype, robotstr, _ = bottypestr.split(' ')
        assert eachstr == 'Each'
        botres = Resource[bottype.upper()]
        costs = [0] * 3
        for res_cost in res_costs.split(' and '):
          count, resstr = res_cost.strip().split(' ')
          count = int(count)
          res = Resource[resstr.upper()]
          assert res != Resource.GEODE
          costs[res.value-1] = count
        bot2costs[botres.value-1] = costs

      bp = Blueprint(id, bot2costs)
      blueprints.append(bp)
  for bp in blueprints:
    print(bp)

assert main('d19full.txt') == 33