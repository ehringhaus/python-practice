from itertools import groupby
from operator import itemgetter

counted = [(char, len(list(group))) for (char, group) in groupby(''.join(sorted(iter('aabbbccde'))))]
ordered = [ele for ele in sorted(list(counted), key=itemgetter(1), reverse=True)[:3]]
print(ordered)
