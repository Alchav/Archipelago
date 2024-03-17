from . import SMMRTestBase

class TestGoals(SMMRTestBase):
    options = {}

    def testBosses(self):
        self.collect_all_but(["f_DefeatedKraid", "f_DefeatedPhantoon", "f_DefeatedDraygon", "f_DefeatedRidley"])
        self.assertBeatable(True)

    def testMiniBosses(self):
        self.collect_all_but(["f_DefeatedBotwoon", "f_DefeatedCrocomire", "f_DefeatedSporeSpawn", "f_DefeatedGoldenTorizo"])
        self.assertBeatable(True)

    def testMetroids(self):
        self.collect_all_but(["f_KilledMetroidRoom1", "f_KilledMetroidRoom2", "f_KilledMetroidRoom3", "f_KilledMetroidRoom4"])
        self.assertBeatable(True)
