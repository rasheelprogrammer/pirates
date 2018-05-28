# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: otp.distributed.PotentialShard


class PotentialShard:
    __module__ = __name__

    def __init__(self, id):
        self.id = id
        self.name = None
        self.population = 0
        self.welcomeValleyPopulation = 0
        self.active = 1
        self.available = 1
        return