import json
import os
import re

# {"capsule": ["filepath"]}


# get ALL Training file
def GetAbstructPath(path):
    RightPath = []
    for root, dirs, files in os.walk(path):
        if len(files) > 0:
            for file in files:
                if "training.6t" in file or "training.bxb" in file:
                    RightPath.append(os.path.join(root, file))

    return RightPath


def GetCapsulePath(path):
    """

    :param path: bixall wenjian path
    :return:  {capsule:[filepath]}
    """
    dict1 = dict()
    for root in os.listdir(path):
        if root not in dict1:
            dict1[root] = []
        dict1[root] = dict1[root] + GetAbstructPath(os.path.join(path, root))
    return dict1


# pattern the utterance return dict  {goal:[utt1,utt2]}
def RegUtterance(utterence):
    #todo
    
    #todo
    # ("\W+[g:(?P<goal>.+?)]((?P<utt1>.+?)[(?P<form>.+?)](?P<utt2>.+?)|(?P<utt1>))")  共找到 1 处匹配："[g:Goal](\W\w+)[r.rr]sada"
    # re.search(r'(go)\s+\1\s+\1', 'go go go').group()
    pass


def GetTrainingUtterence(path):
    """

    :param path: jutiwenjian path
    :return:
    """
    with open(path, 'r', encoding='utf-8') as fp:
        utterence = [line.replace("utterence", "") for line in fp.readlines() if "utterence " in line]
# utterence wei utterence houmian de zifu
    uttDict = RegUtterance(utterence)
    return uttDict  # {goal:[utt1,utt2]}


def RootGoal(dict1, path):
    """"
    path   wei shengcheng wenjian weizhi
    dict1   {capsule:[filepath]}   GetCapsulePath()
    dict11  {goal:[utt1,utt2]}
    """
    dict11 = dict()
    for rootDir, trainpaths in dict1.items():
        capsulepath = os.path.join(path, rootDir)
        if not os.path.exists(capsulepath):
            os.makedirs(capsulepath)  # create capsule dir
        for trainpath in trainpaths:
            uttdict = GetTrainingUtterence(trainpath)
            for goal, utt in uttdict.items():
                if goal not in dict11.keys():
                    dict11[goal] = []
                dict11[goal] = dict11[goal] + utt
        WriteTOFile(dict11, capsulepath=capsulepath)


def WriteTOFile(dict1, capsulepath):
    for goal, utt in dict1:
        writeutt(os.path.join(capsulepath, goal), uttlist=utt)


def writeutt(path, uttlist):
    with open(path, 'a+', encoding="utf-8") as fp:
        for utt in uttlist:
            lin = json.dumps(utt)
            fp.write(lin + "\n")


if __name__ == '__main__':

    bixbyAllpath=""
    targetpath=""
    RootGoal(GetCapsulePath(bixbyAllpath),targetpath)
