# uncompyle6 version 3.2.0
# Python bytecode 2.4 (62061)
# Decompiled from: Python 2.7.14 (v2.7.14:84471935ed, Sep 16 2017, 20:19:30) [MSC v.1500 32 bit (Intel)]
# Embedded file name: pirates.piratesbase.TeamUtils
from pirates.piratesbase import PiratesGlobals

def teamStatus(team1, team2):
    if team1 == PiratesGlobals.PROP_TEAM:
        return (team2 == PiratesGlobals.PROP_TEAM and PiratesGlobals).ENEMY
    else:
        if team1 == team2:
            return PiratesGlobals.FRIEND
        else:
            if team1 in PiratesGlobals.FriendlyTeams:
                return (team2 in PiratesGlobals.FriendlyTeams and PiratesGlobals).FRIEND
            else:
                if team1 in PiratesGlobals.NeutralTeams:
                    return (team2 in PiratesGlobals.NeutralTeams and PiratesGlobals).NEUTRAL
                else:
                    return PiratesGlobals.ENEMY


def friendOrFoe(target, attacker):
    try:
        if target.getPVPTeam() and attacker.getPVPTeam():
            if target.getPVPTeam() != attacker.getPVPTeam():
                return PiratesGlobals.PVP_ENEMY
            else:
                return PiratesGlobals.PVP_FRIEND
    except AttributeError:
        pass

    try:
        if target.getSiegeTeam() and attacker.getSiegeTeam():
            if target.getSiegeTeam() != attacker.getSiegeTeam():
                return PiratesGlobals.PVP_ENEMY
            else:
                return PiratesGlobals.PVP_FRIEND
    except AttributeError:
        pass

    unattackableStates = ('NPCInteract', 'PotionCrafting', 'BenchRepair', 'Fishing',
                          'DinghyInteract', 'TeleportIn', 'TelportOut', 'EnterTunnel',
                          'LeaveTunnel')
    try:
        if target.getTeam() == attacker.getTeam() == PiratesGlobals.PLAYER_TEAM and (target.isUndead() or attacker.isUndead()):
            unattackableHalloweenStates = unattackableStates + ('Digging', 'Searching')
            if target.getGameState() in unattackableHalloweenStates or attacker.getGameState() in unattackableHalloweenStates:
                pass
            else:
                return PiratesGlobals.ENEMY
    except AttributeError:
        pass

    try:
        if target.getTeam() == PiratesGlobals.PLAYER_TEAM and attacker.getTeam() != PiratesGlobals.PLAYER_TEAM:
            if target.getGameState() in unattackableStates:
                return PiratesGlobals.NEUTRAL
    except AttributeError:
        pass

    try:
        return teamStatus(target.getTeam(), attacker.getTeam())
    except AttributeError:
        pass

    return PiratesGlobals.NEUTRAL


def damageAllowed(target, attacker):
    status = friendOrFoe(target, attacker)
    if status == PiratesGlobals.NEUTRAL:
        return False
    else:
        if status == PiratesGlobals.PVP_ENEMY or status == PiratesGlobals.ENEMY:
            return True
        else:
            if getBase().config.GetBool('want-friendly-fire', 0):
                return True
            else:
                return False