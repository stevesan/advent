from dataclasses import dataclass

@dataclass
class File:
  name: str
  size: int

@dataclass
class Dir:
  name: str
  parent: object
  subdirs: dict
  files: list[File]
  totalsize: int = 0

input = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k'''

root = Dir('/', None, {}, [])
currdir = None

with open('d7a.txt', 'r') as f: input = f.read()

for line in input.split('\n'):
  parts = line.split(' ')
  if parts[0] == '$':
    if parts[1] == 'cd':
      arg = parts[2]
      if arg == '/':
        currdir = root
      elif arg == '..':
        currdir = currdir.parent
      else:
        currdir = currdir.subdirs[arg]
    else:
      assert parts[1] == 'ls'
  else:
    # reading ls results
    if parts[0] == 'dir':
      currdir.subdirs[parts[1]] = Dir(name=parts[1], parent=currdir, subdirs={}, files=[])
    else:
      file = File(parts[1], int(parts[0]))
      currdir.files.append(file)

def compute_total_size(dirr:Dir):
  dirr.totalsize = 0
  for file in dirr.files:
    dirr.totalsize += file.size
  for subdir in dirr.subdirs.values():
    compute_total_size(subdir)
    dirr.totalsize += subdir.totalsize

compute_total_size(root)

def collect_sizes(dirr:Dir, sizes:list[int]):
  if dirr.totalsize <= 100000:
    sizes.append(dirr.totalsize)
  print(f'size({dirr.name} = {dirr.totalsize}')
  for subdir in dirr.subdirs.values():
    collect_sizes(subdir, sizes)

sizes = []
collect_sizes(root, sizes)
sizes.sort()

print(sum(sizes))