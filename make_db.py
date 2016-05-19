import json
import os


def init():
    with open('db/people_db') as f:
        db = json.load(f)  # Все данные о человеке

    sample = {0: [], 1: [], 2: [], 3: []}

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

        if hb['user_comments']:
            if date > 1996 and not hb.get('universities'):
                group = 1
            elif not hb.get('universities'):
                group = 2
            elif min_grade(hb):
                if min_grade(hb) >= 2016:
                    group = 3
                elif min_grade(hb) < 2016:
                    group = 4
            if group:
                sample[group - 1].append(hb['user_comments'])

    sample_names = dict(
        school=sample[0],
        no_university=sample[1],
        on_higher_edu=sample[2],
        graduated=sample[3])

    os.remove('db/sample_class_comm')

    with open('db/sample_class_comm', 'w') as f:
        json.dump(sample_names, f)

    # {'class_name': [comments]}

    ################################################################

    with open('db/sample_class_comm') as f:
        ps = json.load(f)

    print(ps)
    com_class = [{} for el in range(len(ps.keys()))]
    names_dic = {}
    k = 0
    for key in ps:
        names_dic[k] = key
        for meses in ps[key]:
            for mes in meses:
                com_class[k][mes] = k
        k += 1
    dic = {'comments-class': com_class,
           'class_names': names_dic}

    for key in dic:
        print(key, dic[key])

    for el in dic['comments-class']:
        print(el)

    with open('db/sample', 'w') as f:
        json.dump(dic, f)

init()
