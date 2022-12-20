from enum import Enum

class Resource(Enum):
  ORE = 1
  CLAY = 2
  OBSIDIAN = 3
  GEODE = 4

def max_num_geodes_possible(robot_to_costs:dict[Resource, dict[Resource, int]]):
  return 0

def main(filep):
  with open(filep, 'r') as f:
    for line in f:
      header, costs = line.split(':')
      bp, idstr = header.split(' ')
      assert bp == 'Blueprint'
      id = int(idstr)
      botcost_strs = costs.split('.')
      for s in botcost_strs:
        if s.strip() == '': continue
        bottypestr, res_costs = s.split('costs')
        _, eachstr, bottype, robotstr, _ = bottypestr.split(' ')
        assert eachstr == 'Each'
        botres = Resource[bottype.upper()]
        for res_cost in res_costs.split(' and '):
          print(f'|{res_cost}|')
          count, resstr = res_cost.strip().split(' ')
          count = int(count)
          res = Resource[resstr.upper()]
          print(f'{count} x {res}')


assert main('d19sample.txt') == 33