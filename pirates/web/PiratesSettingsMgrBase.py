# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.web.PiratesSettingsMgrBase
from pirates.pvp import PVPGlobals
from pirates.ship import ShipBalance

class PiratesSettingsMgrBase:
    __module__ = __name__

    def _initSettings(self):
        self._addSettings(PVPGlobals.WantIslandRegen, PVPGlobals.WantShipRepairSpots, PVPGlobals.WantShipRepairKit, PVPGlobals.ShipRegenRadiusScale, PVPGlobals.ShipRegenHps, PVPGlobals.ShipRegenSps, PVPGlobals.ShipRegenPeriod, PVPGlobals.RepairRate, PVPGlobals.RepairRateMultipliers, PVPGlobals.RepairAcceleration, PVPGlobals.RepairAccelerationMultipliers, PVPGlobals.RepairKitHp, PVPGlobals.RepairKitSp, PVPGlobals.MainWorldInvulnerabilityDuration, PVPGlobals.MainWorldInvulnerabilityWantCutoff, PVPGlobals.MainWorldInvulnerabilityCutoffRadiusScale, PVPGlobals.SinkHpBonusPercent, ShipBalance.RepairRate, ShipBalance.RepairPeriod, ShipBalance.FalloffShift, ShipBalance.FalloffMultiplier, ShipBalance.SpeedModifier, ShipBalance.ArmorAbsorb, ShipBalance.ArmorBounce, ShipBalance.NPCArmorModifier, ShipBalance.NPCDamageIn, ShipBalance.NPCDamageOut, PVPGlobals.SinkStreakPeriod, PVPGlobals.MaxPrivateerShipsPerTeam)
        self._addSettings(*PVPGlobals.ShipClass2repairLocators.values())