import json
import os

with open('db/people_db') as f:
    db = json.load(f)

sample = {0: [], 1: [], 2: [], 3: [], 4: []}


def min_grade(hb):
    grade = 2100
    for univ in hb['universities']:
        if univ.get('graduation'):
            if univ.get('graduation') < grade:
                grade = univ.get('graduation')
    if grade == 2000:
        return None
    else:
        return grade


k = 0
for hb in db:
    date = int(hb['bdate'][-4:])
    group = None
    k += 1
    print(k, hb)
    print(hb.get('universities'))

    if hb['user_comments']:
        if date > 1998:
            group = 1
        elif date > 1996 and not hb.get('universities'):
            group = 2
        elif not hb.get('universities'):
            group = 3
        elif min_grade(hb):
            if min_grade(hb) >= 2016:
                group = 4
            elif min_grade(hb) < 2016:
                group = 5
        if group:
            sample[group - 1].append(hb['user_comments'])

os.remove('db/people_sample')
with open('db/people_sample', 'w') as f:
    json.dump(sample, f)
