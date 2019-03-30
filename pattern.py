from enum import Enum, auto
from typing import Tuple, List, Optional, Dict
from itertools import combinations


class WordType(Enum):
    """基本上是词性"""
    V = auto()
    N = auto()



class FactorRelation(Enum):
    ISTYPE = 0
    ISLITERAL = 1

class DefFactor:
    def __init__(self, factorRelation: FactorRelation, **kargs):
        self.factorRelation = factorRelation

        if factorRelation == FactorRelation.ISTYPE:
            assert "type" in kargs
            self.type = kargs["type"]

        if factorRelation == FactorRelation.ISLITERAL:
            assert "literal" in kargs
            self.literal = kargs['literal']




class CompDef:
    def __init__(self, factors: List[DefFactor]):
        self.factors = factors


class RelationType(Enum):

    # equivalent relation
    vnMatch = 0



class Relation:
    def __init__(self, i1:int, i2:int, relationType: RelationType):
        self.i1 = i1
        self.i2 = i2
        self.relationType = relationType


class SenPattern:

    def __init__(self, name: str, components:List[CompDef]):

        self.name = name
        self._length = len(components)
        self._components = components


    def __len__(self):
        return self._length

    def __getitem__(self, i: int):
        return self._components[i]




class WordCategory:
    name: str

    def __init__(self, name: str):
        self.name = name


class WordUsage:

    segments: Dict[int, WordCategory]

    def __init__(self, segments: Dict[int, WordCategory]):

        self.segments = segments



class WordDef:
    category: Optional[WordCategory]
    usages: List[WordUsage]
    name: str
    types: Optional[List[WordType]]

    def __init__(self, name: str, types: List[WordType] = None):
        self.name = name
        self.types = types
        self.usages = None
        self.category = None

    def expandType(self, t: WordType):

        if self.types:
            self.types.append(t)
        else:
            self.types = [t]


class StrFeatureType(Enum):
    ONLYHAS = 0


class StringFeature:
    args: list

    def __init__(self, featureType: StrFeatureType, featureArgs: List):
        self.type = featureType
        self.args = featureArgs

    def match(self, s: str):
        if self.type is StrFeatureType.ONLYHAS:

            for c in s:
                if c not in self.args:
                    return False
            return True

        else:
            raise Exception("not implemented")




class WordForm:
    """Abstract word patterns that can't be represented by string literals"""
    feature: StringFeature

    def __init__(self, feat: StringFeature):
        self.feature = feat


    def match(self, s:str):
        return self.feature.match(s)



def partitionGen(string: str, partLen: int)->List[List[str]]:
    """
    print(partitionGen("我有毒", 2)) -> [['我', '有毒'], ['我有', '毒']]
    """
    # print("原句： %s"%string)
    # print()

    # print("for partLen %d"%partLen)

    partitions = []
    for r in combinations(range(1,len(string)), partLen-1):
        partition = [0]
        for rr in r:
            partition.append(rr)
        partition.append(len(string))

        onePartition = []

        for i in range(len(partition)-1):
            onePartition.append(string[partition[i]:partition[i+1]])
        partitions.append(onePartition)
    return partitions

        # print(finalRes)
    # print("\n")


vFactor = DefFactor(FactorRelation.ISTYPE, type=WordType.V)
nFactor = DefFactor(FactorRelation.ISTYPE, type=WordType.N)


def getIsLiteralDef(literal: str):
    lFactor = DefFactor(FactorRelation.ISLITERAL, literal= literal)
    return CompDef([lFactor])

vDef = CompDef([vFactor])
nDef = CompDef([nFactor])


# vnImperative = SenPattern("vnImperative", [vDef, nDef], [Relation(0,1, RelationType.vnMatch)])
vnImperative = SenPattern("vnImperative", [vDef, nDef])


if __name__ == "__main__":
    # print(partitionGen("我有毒", 2))
    # print(vnImperative[0])

    pass














