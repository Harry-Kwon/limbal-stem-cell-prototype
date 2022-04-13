from codecs import getincrementaldecoder
from typing import List
from lsc.models.lsc_state import LSCState
from lsc.models.grade_region import GradeRegion

state: LSCState = LSCState()
grade_regions: List[GradeRegion] = []

a = 60
for i in range(int(360/a)):
    grade_regions.append(GradeRegion(a*i, a*(i+1), 0.3, 0.6))

a =30
for i in range(int(360/a)):
    grade_regions.append(GradeRegion(a*i, a*(i+1), 0.6, 1))