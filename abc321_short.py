# Company Logo - Hacker Rank Challenge: 
# https://allhackerranksolutions.blogspot.com/2019/08/company-logo-hacker-rank-solution.html#:~:text=August%201%2C%202019-,Company%20Logo%20%2D%20Hacker%20Rank%20Solution,logos%20based%20on%20this%20condition.

from itertools import groupby
from operator import itemgetter

counted = [(char, len(list(group))) for (char, group) in groupby(''.join(sorted(iter('aabbbccde'))))]
ordered = [ele for ele in sorted(list(counted), key=itemgetter(1), reverse=True)[:3]]
print(ordered)
