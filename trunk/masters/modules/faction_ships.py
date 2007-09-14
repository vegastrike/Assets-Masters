from difficulty import usingDifficulty
import vsrandom
import VS


#use this to allow more interesting weightings than are feasible to manually enter
def weightedlist(tuples):
  rettuple=()
  for i in range(0,len(tuples)):
    for j in range(tuples[i][1]):
      rettuple+=tuples[i][0],
  return rettuple



confed=0
aera=1
rlaan=2
merchant=3
merchant_guild=3
luddites=4
pirates=5
hunter=6
homeland_security=7
ISO=8
unknown=9
andolian=10
highborn=11
shaper=12
unadorned=13
purist=14
forsaken=15
LIHW=16
uln=17
dgn=18
klkk=19
mechanist=20
shmrn=21
rlaan_briin=22


aeran_merchant_marine=23
rlaan_citizen=24
merchant_citizen=25
merchant_guild_citizen=25
andolian_citizen=26
highborn_citizen=27
shaper_citizen=28
unadorned_citizen=29
purist_citizen=30
forsaken_citizen=31
LIHW_citizen=32
uln_citizen=33
dgn_citizen=34
klkk_citizen=35
mechanist_citizen=36
shmrn_citizen=37

fortress_systems={"Crucible/Cephid_17":1-.03625}
invincible_systems={}

max_flightgroups={"Gemini/Troy":25,"Gemini/Penders_Star":15,"Gemini/Junction":12,"Crucible/Cephid_17":22}
min_flightgroups={"Gemini/Troy":22,"Gemini/Penders_Star":10,"Gemini/Junction":4,"Crucible/Cephid_17":22}

factions = ("confed","aera","rlaan","merchant_guild","luddites","pirates","hunter","homeland-security","ISO","unknown","andolian","highborn","shaper","unadorned","purist","forsaken","LIHW","uln","dgn","klkk","mechanist","shmrn","rlaan_briin","aeran_merchant_marine","rlaan_citizen","merchant_guild_citizen","andolian_citizen","highborn_citizen","shaper_citizen","unadorned_citizen","purist_citizen","forsaken_citizen","LIHW_citizen","uln_citizen","dgn_citizen","klkk_citizen","mechanist_citizen","shmrn_citizen")
factiondict={}
for i in range(len(factions)):
    factiondict[factions[i]]=i
factiondict["retro"]=luddites
factiondict["militia"]=homeland_security
factiondict["merchant"]=merchant_guild_citizen

siegingfactions={"confed":10
                ,"andolian":10
                ,"highborn":10
                ,"shaper":10
                ,"unadorned":10
                ,"purist":10
                ,"forsaken":100
                ,"LIHW":50
                ,"aera":10
                ,"rlaan":10
                ,"ISO":40
                ,"luddite":100
                ,"uln":150
                ,"mechanist":9
                }
fightersPerFG=  {"confed":10
                ,"andolian":10
                ,"highborn":10
                ,"shaper":10
                ,"unadorned":10
                ,"purist":10
                ,"forsaken":3
                ,"LIHW":6
                ,"aera":8
                ,"rlaan":11
                ,"ISO":8
                ,"luddite":4
                ,"uln":2
                ,"merchant_guild":3
                ,"pirates":6
                ,"hunter":1
                ,"homeland-security":6
                ,"default":10
                ,"dgn":4
                ,"klkk":4
                ,"mechanist":8
                ,"shmrn":10
                ,"rlaan_briin":2

                ,"andolian_citizen":24*2
                ,"highborn_citizen":24*2
                ,"shaper_citizen":24*2
                ,"unadorned_citizen":24*2
                ,"purist_citizen":24*2
                ,"forsaken_citizen":6*2
                ,"LIHW_citizen":12*2
                ,"aeran_merchant_marine":24*2
                ,"rlaan_citizen":36*2
                ,"uln_citizen":12*2
                ,"merchant_guild_citizen":48*2
                ,"dgn_citizen":12*2
                ,"klkk_citizen":24*2
                ,"mechanist_citizen":12*2
                ,"shmrn_citizen":12*2

                }


capitalsPerFG=  {"confed":1
                ,"andolian":1
                ,"highborn":1
                ,"shaper":1
                ,"unadorned":1
                ,"purist":1
                ,"forsaken":1
                ,"LIHW":1
                ,"aera":1
                ,"rlaan":1
                ,"ISO":1
                ,"luddite":1
                ,"uln":1
                ,"merchant_guild":1
                ,"pirates":1
                ,"hunter":1
                ,"homeland-security":1
                ,"default":1
                ,"dgn":1
                ,"klkk":1
                ,"mechanist":1
                ,"shmrn":1
                ,"rlaan_briin":1
                ,"andolian_citizen":2
                ,"highborn_citizen":1
                ,"shaper_citizen":0
                ,"unadorned_citizen":0
                ,"purist_citizen":0
                ,"forsaken_citizen":0
                ,"LIHW_citizen":0
                ,"aeran_merchant_marine":1
                ,"rlaan_citizen":0
                ,"uln_citizen":0
                ,"merchant_guild_citizen":2
                ,"dgn_citizen":0
                ,"klkk_citizen":0
                ,"mechanist_citizen":0
                ,"shmrn_citizen":0

                }


staticFighterProduction={"luddites":3, "pirates":1}

fighterProductionRate=  {"confed":.01
                        ,"andolian":.1
                        ,"highborn":.15
                        ,"shaper":.1
                        ,"unadorned":.1
                        ,"purist":.1
                        ,"forsaken":.1
                        ,"LIHW":.05
                        ,"aera":.12
                        ,"rlaan":.11
                        ,"ISO":.14
                        ,"luddite":.04
                        ,"uln":.1
                        ,"merchant_guild":.1
                        ,"pirates":.1
                        ,"hunter":.1
                        ,"homeland-security":.05
                        ,"default":.1
                        ,"dgn":.1
                        ,"klkk":.1
                        ,"mechanist":.1
                        ,"shmrn":.08
                        ,"rlaan_briin":.05

                        ,"andolian_citizen":1
                        ,"highborn_citizen":1
                        ,"shaper_citizen":1
                        ,"unadorned_citizen":1
                        ,"purist_citizen":1
                        ,"forsaken_citizen":.3
                        ,"LIHW_citizen":.60
                        ,"aeran_merchant_marine":.80
                        ,"rlaan_citizen":1.10
                        ,"uln_citizen":1.00
                        ,"merchant_guild_citizen":3.00
                        ,"dgn_citizen":.40
                        ,"klkk_citizen":1.00
                        ,"mechanist_citizen":.80
                        ,"shmrn_citizen":.20
                        }

capitalProductionRate=  {"confed":.002
                        ,"andolian":.025
                        ,"highborn":.02
                        ,"shaper":.02
                        ,"unadorned":.02
                        ,"purist":.02
                        ,"forsaken":.02
                        ,"LIHW":.01
                        ,"aera":.024
                        ,"rlaan":.022
                        ,"ISO":.028
                        ,"luddite":.004
                        ,"uln":.02
                        ,"merchant_guild":.02
                        ,"pirates":.02
                        ,"hunter":.02
                        ,"homeland-security":.001
                        ,"default":.02
                        ,"dgn":.02
                        ,"klkk":.02
                        ,"mechanist":.02
                        ,"shmrn":.001
                        ,"rlaan_briin":.001

                        ,"andolian_citizen":.1
                        ,"highborn_citizen":.05
                        ,"shaper_citizen":.01
                        ,"unadorned_citizen":.01
                        ,"purist_citizen":.01
                        ,"forsaken_citizen":.003
                        ,"LIHW_citizen":.0060
                        ,"aeran_merchant_marine":.0080
                        ,"rlaan_citizen":.110
                        ,"uln_citizen":.0100
                        ,"merchant_guild_citizen":.200
                        ,"dgn_citizen":.0040
                        ,"klkk_citizen":.00500
                        ,"mechanist_citizen":.0080
                        ,"shmrn_citizen":.0020
                        }

#FIXME  homeworlds should *exist*
homeworlds={"confed":"Sol/Sol"
                ,"aera":"enigma_sector/shelton"
                ,"rlaan":"enigma_sector/shanha"
                ,"ISO":"enigma_sector/defiance"
                }
production_centers={"confed":["Sol/Sol"]
                ,"aera":["enigma_sector/shelton"]
                ,"rlaan":["enigma_sector/shanha"]
                ,"ISO":["enigma_sector/defiance"]
                }
earnable_upgrades={} #tech tree (new)


def Precache():
	pass#fixme


useStock = (   0    ,  0   ,   0   ,     1    ,   0   ,       0     ,    1   ,         0    ,      0  ,    0,         0    ,    0     ,   0   ,     0      ,   0   ,     1     ,    1 ,  1  ,  0  ,   0 , 0 ,  1 , 1  ,      0,0,0,0,0,0,0,0,0,0,0,0,0,0,0   )#close ones are all civvies


enemies =  ((aera,aera,luddites,pirates,ISO), #confed
            (confed,confed,confed,confed,confed,confed,homeland_security,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan_citizen,rlaan_citizen,rlaan_citizen,rlaan_citizen,rlaan_citizen,pirates,hunter,merchant_guild,merchant_guild_citizen,ISO,andolian,highborn,shaper,unadorned,purist,forsaken_citizen,LIHW,andolian_citizen,highborn_citizen,shaper_citizen,unadorned_citizen,purist_citizen,forsaken_citizen,LIHW_citizen), #aera
            (aera,aera,aera,aera,aera,aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,luddites,luddites,luddites,luddites,luddites,hunter,highborn,highborn_citizen),#rlaan
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,aeran_merchant_marine,luddites,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,forsaken,forsaken_citizen), #merchant_guild
            (confed,confed,confed,homeland_security,rlaan,rlaan_citizen,rlaan_citizen,pirates,hunter,merchant_guild,merchant_guild,merchant_guild,merchant_guild,merchant_guild,merchant_guild,merchant_guild,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,ISO,ISO,ISO,ISO,hunter,hunter,hunter,hunter,hunter), #luddites
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,rlaan,rlaan,rlaan,rlaan_citizen,rlaan_citizen,rlaan_citizen,luddites,aera,aera,aera,aeran_merchant_marine,aeran_merchant_marine,aeran_merchant_marine,merchant_guild,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild_citizen,ISO,andolian,highborn,shaper,unadorned,purist,andolian_citizen,highborn_citizen,shaper_citizen,unadorned_citizen,purist_citizen), #pirates
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,aeran_merchant_marine,aeran_merchant_marine,luddites,luddites,luddites,rlaan,rlaan_citizen,pirates,pirates,ISO), #hunter
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,pirates,ISO,forsaken,forsaken_citizen), #homeland_security
            (confed,confed,confed,confed,confed,confed,confed,homeland_security,homeland_security,homeland_security,aera,aera,aera,pirates,luddites,luddites,luddites,hunter,highborn,highborn_citizen,shaper,shaper_citizen,purist,purist_citizen), #ISO
            (confed,aera,rlaan,merchant_guild,luddites,pirates,hunter,homeland_security,ISO,andolian,highborn,shaper,unadorned,purist,forsaken,LIHW,uln,dgn,aeran_merchant_marine,rlaan_citizen,merchant_guild_citizen,andolian_citizen,highborn_citizen,shaper_citizen,unadorned_citizen,purist_citizen,forsaken_citizen,LIHW_citizen,uln_citizen,dgn_citizen), #unknown
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,luddites,pirates), #andolian
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,pirates,ISO,ISO), #highborn
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,luddites,luddites,ISO), #shaper
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,luddites,luddites), #unadorned
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,ISO,ISO), #purist
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,homeland_security), #forsaken
            (aera,aera,aeran_merchant_marine,luddites), #LIHW
            (aera,rlaan,aeran_merchant_marine,rlaan_citizen,confed), #uln
            (aera,aeran_merchant_marine,pirates), #dgn
            (aera,aeran_merchant_marine,luddites,luddites,pirates), #klkk
            (luddites,luddites,pirates,aera,aera,pirates),#mechanist
            (aera,aeran_merchant_marine,rlaan,rlaan_citizen,confed), #shmrn
            (aera,aeran_merchant_marine,luddites,pirates), #rlaan_briin


            (confed,confed,confed,confed,confed,confed,homeland_security,rlaan,rlaan,rlaan,rlaan,rlaan,rlaan_citizen,rlaan_citizen,rlaan_citizen,rlaan_citizen,rlaan_citizen,pirates,hunter,merchant_guild,merchant_guild_citizen,ISO,andolian,highborn,shaper,unadorned,purist,forsaken_citizen,LIHW,andolian_citizen,highborn_citizen,shaper_citizen,unadorned_citizen,purist_citizen,forsaken_citizen,LIHW_citizen), #aeran_merchant_marine
            (aera,aera,aera,aera,aera,aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,luddites,luddites,luddites,luddites,luddites,hunter,highborn,highborn_citizen),#rlaan_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,aeran_merchant_marine,luddites,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,pirates,forsaken,forsaken_citizen), #merchant_guild_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,luddites,pirates), #andolian_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,pirates,ISO,ISO), #highborn_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,luddites,luddites,ISO), #shaper_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,luddites,luddites), #unadorned_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,pirates,ISO,ISO), #purist_citizen
            (aera,aera,aeran_merchant_marine,aeran_merchant_marine,luddites,homeland_security), #forsaken_citizen
            (aera,aera,aeran_merchant_marine,luddites), #LIHW_citizen
            (aera,rlaan,aeran_merchant_marine,rlaan_citizen,confed), #uln_citizen
            (aera,aeran_merchant_marine,pirates), #dgn_citizen
            (aera,aeran_merchant_marine,luddites,luddites,pirates), #klkk_citizen
            (luddites,luddites,pirates,aera,aera,pirates),#mechanist_citizen
            (aera,aeran_merchant_marine,rlaan,rlaan_citizen,confed) #shmrn_citizen
           )


rabble  =  ((luddites,pirates,ISO,pirates,ISO,pirates,ISO,pirates,pirates,pirates,pirates,ISO,forsaken,forsaken_citizen), #confed
            (pirates,pirates,pirates,hunter,hunter,pirates,pirates,pirates,hunter,hunter,confed,andolian,rlaan,uln,uln_citizen,uln_citizen), #aera
            (pirates,pirates,pirates,pirates,aera,aera,aeran_merchant_marine,confed,hunter,hunter,hunter,uln,uln_citizen,uln_citizen),#rlaan
            (pirates,luddites,pirates,luddites), #merchant_guild
            (homeland_security,homeland_security,ISO,hunter,pirates), #luddites
            (hunter,luddites,ISO,homeland_security), #pirates
            (pirates,luddites,ISO), #hunter
            (luddites,pirates,ISO,forsaken,forsaken_citizen), #homeland_security
            (homeland_security,homeland_security,homeland_security,pirates,luddites,luddites,luddites,hunter), #ISO
            (pirates,pirates,pirates,pirates,luddites,ISO,forsaken,forsaken_citizen,aera,aera,aeran_merchant_marine,rlaan,confed,uln,uln_citizen,uln_citizen,dgn), #unknown
                        (luddites,luddites,pirates,luddites,pirates,pirates,pirates,aera,aera,aeran_merchant_marine,rlaan), #andolian
            (luddites,pirates,ISO,ISO,pirates,ISO,ISO,luddites,aera,aera,aeran_merchant_marine,rlaan), #highborn
            (pirates,luddites,luddites,ISO,pirates,luddites,luddites,ISO,aera,aera,aeran_merchant_marine,rlaan), #shaper
            (pirates,luddites,luddites,pirates,luddites,luddites,ISO,aera,aera,aeran_merchant_marine,rlaan), #unadorned
            (pirates,ISO,ISO,pirates,ISO,ISO,aera,aera,aeran_merchant_marine,rlaan), #purist
            (luddites,homeland_security), #forsaken
            (luddites,luddites,luddites,aera,aera,aeran_merchant_marine,rlaan), #LIHW
            (hunter,hunter,hunter,aera,aera,aeran_merchant_marine,rlaan,confed), #uln
            (pirates,pirates,pirates,), #dgn,dgn_citizen
            (luddites,luddites,pirates), #klkk
            (pirates,luddites,luddites,ISO,pirates,luddites,luddites,ISO,aera,aera,aeran_merchant_marine,rlaan), #mechanist
            (hunter,hunter,hunter,aera,aera,aeran_merchant_marine,rlaan), #shmrn
            (pirates,pirates,pirates,pirates,aera,aera,aeran_merchant_marine,confed,hunter,hunter,hunter,uln,uln_citizen,uln_citizen),#rlaan_briin
            (pirates,pirates,pirates,hunter,hunter,pirates,pirates,pirates,hunter,hunter,confed,andolian,rlaan,uln,uln_citizen,uln_citizen), #aeran_merchant_marine
            (pirates,pirates,pirates,pirates,aera,aera,aeran_merchant_marine,confed,hunter,hunter,hunter,uln,uln_citizen,uln_citizen),#rlaan_citizen
            (pirates,luddites,pirates,luddites), #merchant_guild_citizen
                        (luddites,luddites,pirates,luddites,pirates,pirates,pirates,aera,aera,aeran_merchant_marine,rlaan), #andolian_citizen
            (luddites,pirates,ISO,ISO,pirates,ISO,ISO,luddites,aera,aera,aeran_merchant_marine,rlaan), #highborn_citizen
            (pirates,luddites,luddites,ISO,pirates,luddites,luddites,ISO,aera,aera,aeran_merchant_marine,rlaan), #shaper_citizen
            (pirates,luddites,luddites,pirates,luddites,luddites,ISO,aera,aera,aeran_merchant_marine,rlaan), #unadorned_citizen
            (pirates,ISO,ISO,pirates,ISO,ISO,aera,aera,aeran_merchant_marine,rlaan), #purist_citizen
            (luddites,homeland_security), #forsaken_citizen
            (luddites,luddites,luddites,aera,aera,aeran_merchant_marine,rlaan), #LIHW_citizen
            (hunter,hunter,hunter,aera,aera,aeran_merchant_marine,rlaan,confed), #uln_citizen
            (pirates,pirates,pirates,), #dgn_citizen
            (luddites,luddites,pirates), #klkk_citizen
            (pirates,luddites,luddites,ISO,pirates,luddites,luddites,ISO,aera,aera,aeran_merchant_marine,rlaan), #mechanist_citizen
            (hunter,hunter,hunter,aera,aera,aeran_merchant_marine,rlaan), #shmrn_citizen
           )




insysenemies  =  enemies






friendlies=((confed,confed,confed,confed,confed,confed,confed,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,highborn,highborn_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,purist,purist_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen), #confed
            (aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,uln,uln_citizen,uln_citizen), #aera
            (uln,uln_citizen,uln_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen), #rlaan
            (ISO,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,hunter,rlaan,rlaan_citizen,andolian,andolian_citizen,highborn,highborn_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,purist,purist_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen), #merchant_guild
            (luddites,luddites,luddites), #luddites
            (forsaken,forsaken_citizen,uln,uln_citizen,uln_citizen,LIHW,LIHW_citizen,pirates,pirates,pirates,pirates,pirates), #pirates
            (confed,confed,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,hunter,hunter,hunter,hunter,hunter,merchant_guild_citizen,merchant_guild_citizen,merchant_guild), #hunter
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,highborn,highborn_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,purist,purist_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen), #homeland_security
            (ISO,ISO,ISO,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,ISO,ISO,ISO,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,ISO,ISO,ISO,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild), #ISO
            (merchant_guild_citizen,merchant_guild_citizen,merchant_guild,), #unknown
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,unadorned,unadorned_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #andolian
            (confed,confed,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,shaper,shaper_citizen,purist,purist_citizen,unadorned,unadorned_citizen,shaper,shaper_citizen,purist,purist_citizen,unadorned,unadorned_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #highborn
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,shaper,shaper_citizen,shaper,shaper_citizen,highborn,highborn_citizen,highborn,highborn_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #shaper
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #unadorned
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,highborn,highborn_citizen,purist,purist_citizen,highborn,highborn_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #purist
            (forsaken,forsaken_citizen,forsaken,forsaken_citizen,pirates,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen), #forsaken
            (forsaken,forsaken_citizen,forsaken,forsaken_citizen,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen), #LIHW
            (uln,uln_citizen,uln_citizen,uln,uln_citizen,uln_citizen,uln,uln_citizen,uln_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,pirates,rlaan,rlaan_citizen,forsaken,forsaken_citizen), #uln
            (dgn,dgn_citizen,dgn,dgn_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen), #dgn
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,unadorned,unadorned_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,klkk,klkk_citizen,klkk,klkk_citizen),  #klkk
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,uln,uln_citizen,uln_citizen),  #mechanist
            (uln,uln_citizen,uln_citizen,shmrn,shmrn_citizen,shmrn,shmrn_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,pirates,rlaan,rlaan_citizen,forsaken,forsaken_citizen), #shmrn
            (confed,confed,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,hunter,rlaan_briin,rlaan_briin,rlaan_briin), #rlaan_briin
            (aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,aera,aera,aeran_merchant_marine,uln,uln_citizen,uln_citizen), #aeran_merchant_marine
            (uln,uln_citizen,uln_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen,rlaan,rlaan_citizen), #rlaan_citizen
            (ISO,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,hunter,rlaan,rlaan_citizen,andolian,andolian_citizen,highborn,highborn_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,purist,purist_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen), #merchant_guild_citizen
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,unadorned,unadorned_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #andolian_citizen
            (confed,confed,confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,shaper,shaper_citizen,purist,purist_citizen,unadorned,unadorned_citizen,shaper,shaper_citizen,purist,purist_citizen,unadorned,unadorned_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #highborn_citizen
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,shaper,shaper_citizen,shaper,shaper_citizen,highborn,highborn_citizen,highborn,highborn_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #shaper_citizen
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,unadorned,unadorned_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #unadorned_citizen
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,highborn,highborn_citizen,purist,purist_citizen,highborn,highborn_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,purist,purist_citizen,dgn,dgn_citizen,uln,uln_citizen,uln_citizen),  #purist_citizen
            (forsaken,forsaken_citizen,forsaken,forsaken_citizen,pirates,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen), #forsaken_citizen
            (forsaken,forsaken_citizen,forsaken,forsaken_citizen,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen,LIHW,LIHW_citizen), #LIHW_citizen
            (uln,uln_citizen,uln_citizen,uln,uln_citizen,uln_citizen,uln,uln_citizen,uln_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,pirates,rlaan,rlaan_citizen,forsaken,forsaken_citizen), #uln_citizen
            (dgn,dgn_citizen,dgn,dgn_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen), #dgn_citizen
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,andolian,andolian_citizen,unadorned,unadorned_citizen,forsaken,forsaken_citizen,LIHW,LIHW_citizen,klkk,klkk_citizen,klkk,klkk_citizen),  #klkk_citizen
            (confed,confed,confed,homeland_security,homeland_security,homeland_security,homeland_security,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,LIHW,LIHW_citizen,highborn,highborn_citizen,highborn,highborn_citizen,highborn,highborn_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,mechanist,mechanist_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,shaper,shaper_citizen,unadorned,unadorned_citizen,uln,uln_citizen,uln_citizen),  #mechanist_citizen
            (uln,uln_citizen,uln_citizen,shmrn,shmrn_citizen,shmrn,shmrn_citizen,merchant_guild_citizen,merchant_guild_citizen,merchant_guild,pirates,rlaan,rlaan_citizen,forsaken,forsaken_citizen), #shmrn_citizen


           )

fighters = (("Lancelot","Lancelot","Gawain","Lancelot","Gawain","Progeny","Progeny","Pacifier","Schroedinger","Pacifier","Schroedinger","Derivative","Convolution","Derivative","Convolution","Goddard","Franklin","Quicksilver"), #confed
                        ("Nicander","Ariston","Areus"), #aera
                        ("Shizu","Zhuangzong","Taizong"), #rlaan
                        ("Mule","Plowshare"), #merchant_guild
                        ("Redeemer",), #luddites
                        ("Hyena","Plowshare"), #pirates
                        ("Hyena","Robin","Hyena","Robin","Sickle","Hammer"), #hunter
                        ("Admonisher",), #homeland_security
                        ("Hammer","Sickle","Hammer","Sickle","Hammer","Sickle","Hammer","Sickle","Hammer","Sickle","Sickle","Sickle","Franklin"), #ISO
                        ("Beholder",), #unknown
                        ("Schroedinger","Schroedinger","Schroedinger","Schroedinger","Schroedinger","Goddard","Goddard","Franklin","Kierkegaard"),#andolian
                        ("Gawain","Lancelot"),#highborn
                        ("Ancestor","Progeny","Progeny"),#shaper
                        ("Derivative","Determinant","Convolution","Derivative","Determinant","Convolution","Franklin"),#unadorned
                        ("Pacifier","Admonisher","Plowshare"),#purist
                        ("Hyena",),#forsaken
                        ("Sickle","Robin","Robin","Robin","Robin","Robin","Hammer"),#LIHW
                        ("Ancestor","Llama","Hyena"),#uln
                        ("Dodo","Dodo","Dodo","Quicksilver"), #dgn
                        ("Dostoevsky","Dostoevsky","Dostoevsky","Dostoevsky","Dostoevsky","Kierkegaard"), #klkk
                        ("Llama","Convolution"),#mechanist
                        ("Dirge",),#shmrn
                        ("Zhuangzong",), #rlaan_briin
                        ("Nicander","Ariston"), #aeran_merchant_marine
                        ("Shizu.civvie",), #rlaan_citizen
                        ("Mule.civvie","Plowshare.civvie","Llama.civvie","Quicksilver.civvie"), #merchant_guild_citizen
                        ("Franklin.civvie","Sartre.civvie","Sartre.civvie","Kafka.civvie","Kafka.civvie","Llama.civvie","Quicksilver.civvie"),#andolian_citizen
                        ("Hidalgo.civvie","GTIO.civvie","GTIO.civvie"),#highborn_citizen
                        ("Mule.civvie","Plowshare.civvie","Llama.civvie","Quicksilver.civvie"),#shaper_citizen
                        ("Mule.civvie","Plowshare.civvie","Llama.civvie"),#unadorned_citizen
                        ("Mule.civvie","Llama.civvie","Plowshare.civvie","Mule.civvie","Llama.civvie","Plowshare.civvie","GTIO.civvie","Quicksilver.civvie"),#purist_citizen
                        ("Hyena.civvie","Llama.civvie",),#forsaken_citizen
                        ("Llama.civvie","Llama.civvie","Llama.civvie","Quicksilver.civvie"),#LIHW_citizen
                        ("Dodo.civvie","Llama.civvie"),#uln_citizen
                        ("Dodo.civvie","Quicksilver.civvie"), #dgn_citizen
                        ("Kafka.civvie","Kafka.civvie","Sartre.civvie","Llama.civvie",), #klkk_citizen
                        ("Kafka.civvie","Llama.civvie"),#mechanist_citizen
                        ("Kafka.civvie","Kafka.civvie","Kafka.civvie","Sartre.civvie"),#shmrn_citizen

           )
isBomber = {"Areus":6,"Taizong":8,"Pacifier":5,"Goddard":4,"Hammer":16,"Admonisher":10,"Areus.blank":6,"Taizong.blank":8,"Pacifier.blank":5,"Goddard.blank":4,"Hammer.blank":16,"Admonisher.blank":10}
unescortable = {"tesla":"Ox",
	"kahan":"Mule",
	"Clydesdale":"Ox",
	"shundi":"Zhuangzong",
	"huldra":"Taizong",
	"vitik":"vark",
	"watson":"Mule",
	"yavok":"vark",
	"yrilan":"vark"}

capitals = (("Clydesdale","watson","archimedes","kahan","tesla"), #confed
            ("vark","vitik","yavok","yrilan"), #aera
            ("huldra","shundi"), #rlaan
            ("Ox","Clydesdale"), #merchant_guild
            ("Mule",), #luddites
            ("Corvette",), #pirates
            ("Mule",), #hunter
            ("Clydesdale",), #homeland_security
            ("Corvette","Mule"), #ISO
            ("Beholder",), #unknown
            ("kahan","watson","archimedes","tesla"),#andolian
            ("Clydesdale",),#highborn
            ("Clydesdale",),#shaper
            ("watson","kahan"),#unadorned
            ("Clydesdale",),#purist
            ("Corvette",),#forsaken
            ("Ox",),#LIHW
            ("Mule",),#uln
            ("Dodo",), #dgn
            ("kahan",), #klk
            ("watson",),#mechanist
            ("Dodo",), #shmrn
            ("huldra",), #rlaan_briin
            ("Ox","Clydesdale"), #aeran_merchant_marine FIXME
            ("Mule","Ox","Clydesdale"), #rlaan_citizen FIXME
            ("Mule","Ox","Clydesdale"), #merchant_guild_citizen
            ("Ox","Mule"), #andolian_citizen #FIXME - all citizens a bit b0rken
            ("Ox","Mule"), #highborn_citizen
            ("Ox","Mule"), #shaper_citizen
            ("Ox","Mule"), #unadorned_citizen
            ("Ox","Mule"), #purist_citizen
            ("Ox","Mule"), #forsaken_citizen
            ("Ox","Mule"), #LIHW_citizen
            ("Ox","Mule"), #uln_citizen
            ("Ox","Mule"), #dgn_citizen
            ("Ox","Mule"), #klk_citizen
            ("Ox","Mule"), #mechanist_citizen
            ("Ox","Mule"), #shmrn_citizen
           )
stattableexp={
        #SHIPNAME:(CHANCE_TO_HIT,CHANCE_TO_DODGE,DAMAGE,SHIELDS,ORDINANCE_DAMAGE),
        "Redeemer":(0.38,0.38,180,290,200),
        "Dirge":(0.38,0.38,180,290,200),
        "Ancestor":(0.48,0.58,160,410,400),
        "Gawain":(0.67,0.7,500,400,400),
        "Dostoevsky":(0.6,0.68,200,540,2000),
        "Robin":(0.44,0.48,300,350,200),
        "Hyena":(0.44,0.52,150,300,200),
        "Beholder":(1,1,5000,6940,0),
        "Determinant":(0.5,0.62,300,590,400),
        "Sickle":(0.34,0.34,480,390,800),
        "Shizu":(0.52,0.52,40,320,0),
        "Quicksilver":(0.52,0.52,40,320,0),
        "Convolution":(0.54,0.7,500,620,50000),
        "Progeny":(0.68,0.86,200,470,400),
        "Zhuangzong":(0.52,0.5,440,450,0),
        "Schroedinger":(0.8,0.91,120,790,400),
        "Hammer":(0.36,0.28,600,550,50000),
        "Nicander":(0.52,0.46,300,910,300),
        "Derivative":(0.5,0.46,500,1030,400),
        "Lancelot":(0.5,0.44,540,1250,600),
        "Ariston":(0.54,0.32,500,1190,800),
        "Areus":(0.64,0.34,400,1300,300000),
        "Taizong":(0.78,0.42,440,1150,100000),
        "Admonisher":(0.38,0.32,100,1410,2000),
        "Pacifier":(0.3,0.2,400,1890,100000),
        "Plowshare":(0.3,0.2,100,1380,400),
        "Sartre":(0.3,0.2,100,1380,400),
        "Franklin":(0.76,0.78,200,2590,2000),
        "Dodo":(0.4,0.16,10,2500,0),
        "Kafka":(0.4,0.16,10,2500,0),
        "GTIO":(0.4,0.16,10,2500,0),
        "Goddard":(0.86,0.24,800,5200,500000),
        "Llama":(0.34,0.22,200,4630,400),
        "Mule":(0.52,0.14,200,18720,400),
        "Hidalgo":(0.52,0.14,200,18720,400),
        "Corvette":(0.32,0.02,1000,10000,10000),
        "watson":(1,0.16,2000,269400,3210),
        "Ox":(0.68,0.16,300,286770,0),
        "MiningBase":(1,0,100,715750,0),
        "vark":(1,0.22,20000,1366420,600000),
        "huldra":(1,0.2,25000,1408430,3210),
        "AsteroidFighterBase":(0.52,0,200,1512400,3210),
        "nietzsche":(1,0.18,20000,1564400,100000),
        "Clydesdale":(1,0.14,40000,1683740,300000),
        "tesla":(1,0.22,100000,1887640,0),
        "shundi":(1,0.18,50000,2017640,3210),
        "medical":(1,0,0,2230130,0),
        "archimedes":(1,0.18,60000,2292530,1000000),
        "yrilan":(1,0.24,50000,2495160,1000000),
        "relay":(0.24,0,10,3228510,0),
        "research":(0.12,0,0,5497290,0),
        "vitik":(1,0.16,50000,5738710,3210),
        "yavok":(1,0.12,300000,8138400,2000000),
        "fighter_barracks":(0.12,0,100,9050760,3210),
        "outpost":(0.12,0,100,9050760,3210), #same stats as fighter_barracks...  fixme?
        "Shipyard":(0.12,0,100,9050760,3210), #same stats as fighter_barracks...  fixme?
        "factory":(.02,0.02,10,13987040,0),
        "commerce_center":(1,0,10,21841060,0),
        "refinery":(0.4,0,10,33071210,0),
        "starfortress":(1,0,750000,475993990,4000000),
        "kahan":(1,0.18,25000,1400000,500000)
        }

# stattable is generated by adding your ship/base to stattableexp, and then running log_faction_ships.py ('python log_factions_ships.py')
stattable={'archimedes': (1, 0.17999999999999999, 15.872698924987583, 21.128509811647834,19.931570012018494), 'Lancelot.blank': (0.5, 0.22, 4.5397423919134079, 5.1444330370829103, 4.6156105903555931), 'Sickle': (0.34000000000000002, 0.34000000000000002, 8.9098930837700419, 8.611024797307353, 9.6456584324087107), 'factory.blank': (0.02, 0.01, 1.7297158093186489, 11.86879372628966, 0.0), 'vark': (1, 0.22, 14.287784512498186, 20.38197062179206, 19.194605379647701), 'Progeny': (0.68000000000000005, 0.85999999999999999, 7.651051691178929, 8.879583249612784, 8.6474584264549215), 'neitzsche': (1, 0.17999999999999999, 14.287784512498186, 20.577178932710801, 16.609654901315089), 'Derivative': (0.5, 0.46000000000000002, 8.968666793195208, 10.009828617368109, 8.6474584264549215), 'Shizu.blank': (0.52000000000000002, 0.26000000000000001, 2.6787760023090419, 4.1632147435611513, 0.0), 'Determinant.blank': (0.5, 0.31, 4.1168098383798508, 4.6035071600887667, 4.3237292132274607), 'Ox.blank': (0.68000000000000005, 0.080000000000000002, 4.1168098383798508, 9.0647698059475612, 0.0), 'watson': (1, 0.16, 10.966505451905741, 18.039395680442535, 11.64880694972577), 'yrilan': (1, 0.23999999999999999, 15.609669328049096, 21.250701477635289, 19.931570012018494), 'Llama': (0.34000000000000002, 0.22, 7.651051691178929, 12.177108041703693, 8.6474584264549215), 'Plowshare': (0.29999999999999999, 0.20000000000000001, 6.6582114827517955, 10.431497604258052, 8.6474584264549215), 'shundi.blank': (1, 0.089999999999999997, 7.8048346640245478, 10.472119033530774, 5.8244034748628852), 'Ariston.blank': (0.54000000000000004, 0.16, 4.484333396597604, 5.1089788489320567, 4.8228292162043553), 'Shipyard': (0.12, 0, 6.6582114827517955, 23.109607670334245, 11.64880694972577), 'Ancestor.blank': (0.47999999999999998, 0.28999999999999998, 3.6654584390573088, 4.3414972918408417, 4.3237292132274607), 'vark.blank': (1, 0.11, 7.1438922562490932, 10.19098531089603, 9.5973026898238505), 'Taizong': (0.78000000000000003, 0.41999999999999998, 8.7846348455575214, 10.16867211813223, 16.609654901315089), 'Progeny.blank': (0.68000000000000005, 0.42999999999999999, 3.8255258455894645, 4.439791624806392, 4.3237292132274607), 'starfortress.blank': (1, 0.0, 9.7582664968187185, 14.413184060003852, 10.965784464998945), 'Corvette': (0.32000000000000001, 0.02, 9.9672262588359928, 13.287856641840545, 13.287856641840545), 'Clydesdale': (1, 0.14000000000000001, 15.287748446474637, 20.683238803480901, 18.194607784133421), 'Robin.blank': (0.44, 0.23999999999999999, 4.1168098383798508, 4.2276636101522804, 3.8255258455894645), 'fighter_barracks.blank': (0.12, 0.0, 3.3291057413758978,11.554803835167123, 5.8244034748628852), 'Hammer': (0.35999999999999999, 0.28000000000000003, 9.2312211807111861, 9.105908508571158, 15.609669328049096), 'Goddard': (0.85999999999999999, 0.23999999999999999, 9.6456584324087107, 12.344573322596201, 18.931571454711371), 'Franklin.blank': (0.76000000000000001, 0.39000000000000001, 3.8255258455894645, 5.6696466500900469, 5.4832527259528705), 'factory': (0.02, 0.02, 3.4594316186372978, 23.737587452579319, 0.0), 'research': (0.12,0, 0.0, 22.390289420019656, 0.0), 'huldra.blank': (1, 0.10000000000000001, 7.3048490905421612, 10.212828728074706, 5.8244034748628852), 'Mule': (0.52000000000000002, 0.14000000000000001, 7.651051691178929, 14.192369879455208, 8.6474584264549215), 'Shizu': (0.52000000000000002, 0.52000000000000002, 5.3575520046180838, 8.3264294871223026, 0.0), 'Gawain': (0.67000000000000004, 0.69999999999999996, 8.968666793195208, 8.6474584264549215, 8.6474584264549215), 'research.blank': (0.12, 0.0, 0.0, 11.195144710009828, 0.0), 'Redeemer.blank': (0.38, 0.19, 3.7499229435416028, 4.0924376714541424, 3.8255258455894645), 'Nicander': (0.52000000000000002,0.46000000000000002, 8.2336196767597016, 9.8313072438020512, 8.2336196767597016), 'commerce_center.blank': (1, 0.0, 1.7297158093186489, 12.190269802868773, 0.0), 'Ariston': (0.54000000000000004, 0.32000000000000001, 8.968666793195208, 10.217957697864113, 9.6456584324087107), 'MiningBase.blank': (1, 0.0, 3.3291057413758978, 9.7245491276505138, 0.0), 'Goddard.blank': (0.85999999999999999, 0.12, 4.8228292162043553, 6.1722866612981004, 9.4657857273556854), 'Lancelot': (0.5, 0.44, 9.0794847838268158, 10.288866074165821, 9.2312211807111861), 'watson.blank': (1,0.080000000000000002, 5.4832527259528705, 9.0196978402212675, 5.8244034748628852), 'Franklin': (0.76000000000000001, 0.78000000000000003, 7.651051691178929, 11.339293300180094, 10.966505451905741), 'Ox': (0.68000000000000005, 0.16, 8.2336196767597016, 18.129539611895122, 0.0), 'Mule.blank': (0.52000000000000002, 0.070000000000000007, 3.8255258455894645, 7.0961849397276042, 4.3237292132274607), 'Schroedinger': (0.80000000000000004, 0.91000000000000003, 6.9188632372745955, 9.6275338844727933, 8.6474584264549215), 'Hammer.blank': (0.35999999999999999, 0.14000000000000001, 4.6156105903555931, 4.552954254285579, 7.8048346640245478), 'Convolution': (0.54000000000000004, 0.69999999999999996, 8.968666793195208, 9.2784494582204822, 15.609669328049096), 'AsteroidFighterBase.blank': (0.52000000000000002, 0.0, 3.8255258455894645, 10.264204638836336, 5.8244034748628852), 'Pacifier': (0.29999999999999999, 0.20000000000000001, 8.6474584264549215, 10.884933647949762, 16.609654901315089), 'Zhuangzong': (0.52000000000000002, 0.5, 8.7846348455575214, 8.816983623255382, 0.0), 'Gawain.blank': (0.67000000000000004, 0.34999999999999998, 4.484333396597604, 4.3237292132274607, 4.3237292132274607), 'Admonisher.blank': (0.38, 0.16, 3.3291057413758978, 5.2312511362986323, 5.4832527259528705), 'Admonisher': (0.38, 0.32000000000000001, 6.6582114827517955, 10.462502272597265, 10.966505451905741), 'starfortress': (1, 0, 19.516532993637437, 28.826368120007704, 21.931568929997891), 'outpost.blank': (0.12, 0.0, 3.3291057413758978, 11.554803835167123, 5.8244034748628852), 'relay.blank': (0.23999999999999999, 0.0,1.7297158093186489, 10.811218755943361, 0.0), 'Pacifier.blank': (0.29999999999999999, 0.10000000000000001, 4.3237292132274607, 5.4424668239748808, 8.3048274506575446), 'Determinant': (0.5, 0.62, 8.2336196767597016, 9.2070143201775334, 8.6474584264549215), 'yavok.blank': (1, 0.059999999999999998, 9.0973038920667104, 11.478156968395703, 10.465784645335757), 'relay': (0.23999999999999999, 0, 3.4594316186372978, 21.622437511886723, 0.0), 'Beholder': (1, 1, 12.288000889707574, 12.760927813619848, 0.0), 'Clydesdale.blank': (1, 0.070000000000000007, 7.6438742232373187, 10.34161940174045, 9.0973038920667104), 'Corvette.blank': (0.32000000000000001, 0.01, 4.9836131294179964, 6.6439283209202724, 6.6439283209202724), 'huldra': (1, 0.20000000000000001, 14.609698181084322, 20.425657456149413, 11.64880694972577), 'Areus.blank': (0.64000000000000001, 0.17000000000000001, 4.3237292132274607, 5.172702623358898, 9.0973038920667104), 'MiningBase': (1, 0, 6.6582114827517955, 19.449098255301028, 0.0), 'outpost': (0.12, 0, 6.6582114827517955, 23.109607670334245, 11.64880694972577), 'Llama.blank': (0.34000000000000002, 0.11, 3.8255258455894645, 6.0885540208518467, 4.3237292132274607), 'Beholder.blank':(1, 0.5, 6.1440004448537868, 6.3804639068099238, 0.0), 'Areus': (0.64000000000000001, 0.34000000000000002, 8.6474584264549215, 10.345405246717796, 18.194607784133421), 'Zhuangzong.blank': (0.52000000000000002, 0.25, 4.3923174227787607, 4.408491811627691, 0.0), 'yavok': (1, 0.12, 18.194607784133421, 22.956313936791407, 20.931569290671515), 'Dodo': (0.40000000000000002, 0.16, 3.4594316186372978, 11.28828934218097, 0.0), 'Redeemer': (0.38, 0.38, 7.4998458870832057, 8.1848753429082848, 7.651051691178929), 'shundi': (1, 0.17999999999999999, 15.609669328049096, 20.944238067061548, 11.64880694972577), 'Robin': (0.44, 0.47999999999999998, 8.2336196767597016, 8.4553272203045609, 7.651051691178929), 'Convolution.blank': (0.54000000000000004, 0.34999999999999998, 4.484333396597604, 4.6392247291102411, 7.8048346640245478), 'kahan': (1, 0.17999999999999999, 14.609698181084322, 20.416996426990508, 18.931571454711371), 'archimedes.blank': (1, 0.089999999999999997, 7.9363494624937916, 10.564254905823917, 9.9657850060092468), 'Dodo.blank': (0.40000000000000002, 0.080000000000000002, 1.7297158093186489, 5.6441446710904852, 0.0), 'Derivative.blank': (0.5, 0.23000000000000001, 4.484333396597604, 5.0049143086840546, 4.3237292132274607), 'tesla': (1, 0.22, 16.609654901315089, 20.848152981922532, 0.0), 'Schroedinger.blank': (0.80000000000000004, 0.45500000000000002, 3.4594316186372978, 4.8137669422363967, 4.3237292132274607), 'refinery': (0.40000000000000002, 0, 3.4594316186372978, 24.979072539244839, 0.0), 'Dostoevsky': (0.59999999999999998, 0.68000000000000005, 7.651051691178929, 9.0794847838268158, 10.966505451905741), 'Taizong.blank': (0.78000000000000003, 0.20999999999999999,4.3923174227787607, 5.0843360590661151, 8.3048274506575446), 'Plowshare.blank':(0.29999999999999999, 0.10000000000000001, 3.3291057413758978, 5.2157488021290259, 4.3237292132274607), 'yrilan.blank': (1, 0.12, 7.8048346640245478, 10.625350738817644, 9.9657850060092468), 'AsteroidFighterBase': (0.52000000000000002, 0, 7.651051691178929, 20.528409277672672, 11.64880694972577), 'neitzsche.blank': (1, 0.089999999999999997, 7.1438922562490932, 10.288589466355401, 8.3048274506575446), 'Nicander.blank': (0.52000000000000002, 0.23000000000000001, 4.1168098383798508, 4.9156536219010256, 4.1168098383798508), 'vitik': (1, 0.16, 15.609669328049096, 22.452295291810014, 11.64880694972577), 'refinery.blank': (0.40000000000000002, 0.0, 1.7297158093186489, 12.48953626962242, 0.0), 'vitik.blank': (1, 0.080000000000000002, 7.8048346640245478, 11.226147645905007, 5.8244034748628852), 'Ancestor': (0.47999999999999998, 0.57999999999999996, 7.3309168781146177, 8.6829945836816833, 8.6474584264549215), 'Sickle.blank': (0.34000000000000002, 0.17000000000000001, 4.4549465418850209, 4.3055123986536765, 4.8228292162043553), 'commerce_center': (1, 0, 3.4594316186372978, 24.380539605737546, 0.0), 'fighter_barracks': (0.12, 0, 6.6582114827517955, 23.109607670334245, 11.64880694972577), 'medical.blank': (1, 0.0, 0.0, 10.544348513613674, 0.0), 'Hyena.blank': (0.44, 0.26000000000000001, 3.6192023696625397, 4.1168098383798508, 3.8255258455894645), 'Shipyard.blank': (0.12, 0.0, 3.3291057413758978, 11.554803835167123, 5.8244034748628852), 'kahan.blank': (1, 0.089999999999999997, 7.3048490905421612, 10.208498213495254, 9.4657857273556854), 'medical': (1, 0, 0.0, 21.088697027227347, 0.0), 'Hyena': (0.44, 0.52000000000000002, 7.2384047393250794, 8.2336196767597016, 7.651051691178929), 'Dostoevsky.blank': (0.59999999999999998, 0.34000000000000002, 3.8255258455894645, 4.5397423919134079, 5.4832527259528705), 'tesla.blank': (1, 0.11,8.3048274506575446, 10.424076490961266, 0.0)}



def GetStats ( name):
    try:
        return stattable[name]
    except:
        import debug
        debug.error( 'cannot find '+name)
        return (.5,.5,1,1,1)


capitols=capitals
capitaldict={}
for i in capitols:
    for j in i:
        capitaldict[j]=1
for i in capitols:
    for j in i:
        capitaldict[j+'.blank']=1

def isCapital(type):
    return type in capitaldict

generic_bases = ("starfortress","starfortress",
                                 "research","research",
                                 "medical","medical","medical",
                                 "commerce_center","commerce_center","commerce_center",
                                 "factory","factory","factory",
                                 "outpost","outpost","outpost","outpost",
                                 "fighter_barracks","fighter_barracks","fighter_barracks","fighter_barracks",
                                 "relay","relay","relay","relay","relay",
                                 "refinery","refinery","refinery","refinery","refinery",
                                 "MiningBase","MiningBase","MiningBase","MiningBase","MiningBase","MiningBase")
                                 
bases = (generic_bases,
                 generic_bases, #aera
                 generic_bases, #rlaan
                 generic_bases, #merchant_guild
                 generic_bases, #luddites
                 generic_bases, #pirates
                 generic_bases, #hunter
                 generic_bases, #homeland_security
                 generic_bases, #ISO
                 generic_bases, #unknown
                 generic_bases,#andolian
                 generic_bases,#highborn
                 generic_bases,#shaper
                 generic_bases,#unadorned
                 generic_bases,#purist
                 generic_bases,#forsaken
                 generic_bases,#LIHW
                 generic_bases,#uln
                 generic_bases, #dgn
                 generic_bases, #klkk
                 generic_bases, #mechanist
                 generic_bases, #shmrn
                 generic_bases, #rlaan_briin
                 generic_bases, #aeran_merchant_marine
                 generic_bases, #rlaan_citizen
                 generic_bases, #merchant_guild_citizen
                 generic_bases,#andolian_citizen
                 generic_bases,#highborn_citizen
                 generic_bases,#shaper_citizen
                 generic_bases,#unadorned_citizen
                 generic_bases,#purist_citizen
                 generic_bases,#forsaken_citizen
                 generic_bases,#LIHW_citizen
                 generic_bases,#uln_citizen
                 generic_bases, #dgn_citizen
                 generic_bases, #klkk_citizen
                 generic_bases, #mechanist_citizen
                 generic_bases, #shmrn_citizen

                 )
basedict={}
for i in bases:
    for j in i:
        basedict[j]=1

def appendName(faction):
    if (useStock[faction] and usingDifficulty()):
	# DON'T USE .blanks directly if possible-- preserve as templates. Use .stock where possible
        return ".stock"
    else:
        return ""

def factionToInt  (faction):
    try:
        return factiondict[faction]
    except:
        return 0
    return 0

def intToFaction (faction):
    return factions[faction]

def getMaxFactions ():
    return len(factions)



    

def get_non_citizen_X_of (mylist, index):
    enemylist = mylist[index]
    newindex = vsrandom.randrange(0,len(enemylist))
    rez=intToFaction(enemylist[newindex])
    if VS.isCitizen(rez):
        while (newindex>0):
          newindex-=1
          rez=intToFaction(enemylist[newindex])          
          if not VS.isCitizen(rez):
              return rez
        while (newindex+1<len(enemylist)):
          newindex+=1
          rez=intToFaction(enemylist[newindex])          
          if not VS.isCitizen(rez):
              return rez
    return rez
def get_X_of (mylist, index):
    enemylist = mylist[index]
    newindex = vsrandom.randrange(0,len(enemylist))
    return intToFaction(enemylist[newindex])


def get_enemy_of (factionname):
    return get_X_of (enemies, factionToInt(factionname))

def get_insys_enemy_of (factionname):
    return get_X_of (insysenemies, factionToInt(factionname))

def get_friend_of (factionname):
    return get_X_of (friendlies, factionToInt(factionname))

def get_rabble_of (factionname):
    return get_X_of (rabble, factionToInt(factionname))


def get_enemy_of_no_citizen (factionname):
    return get_X_of (enemies, factionToInt(factionname))
    #return get_non_citizen_X_of (enemies, factionToInt(factionname))

def get_insys_enemy_of_no_citizen (factionname):
    return get_X_of (insysenemies, factionToInt(factionname))
    #return get_non_citizen_X_of (insysenemies, factionToInt(factionname))

def get_friend_of_no_citizen (factionname):
    return get_X_of (friendlies, factionToInt(factionname))
    #return get_non_citizen_X_of (friendlies, factionToInt(factionname))

def get_rabble_of_no_citizen (factionname):
    return get_X_of (rabble, factionToInt(factionname))
    #return get_non_citizen_X_of (rabble, factionToInt(factionname))

def getRandomShipType(ship_list):
    index=vsrandom.randrange(0,len(ship_list))
    return ship_list[index]

def getFigher(confed_aera_or_rlaan, fighter):
    fighterlist = fighters[confed_aera_or_rlaan]
    fighterlist = fighterlist[fighter]
    return fighterlist+appendName(confed_aera_or_rlaan)

def getRandomFighterInt(confed_aera_or_rlaan):
    return getRandomShipType(fighters[confed_aera_or_rlaan])+appendName(confed_aera_or_rlaan)

def getNumCapitol (confed_aera_or_rlaan):
    return len(capitols[confed_aera_or_rlaan])

def getNumFighters (confed_aera_or_rlaan):
    lst = fighters[confed_aera_or_rlaan]
    return len(lst)

def getCapitol(confed_aera_or_rlaan, fighter):
    caplist = capitols[confed_aera_or_rlaan]
    caplist = caplist[fighter]
    return caplist

def getRandomCapitolInt(confed_aera_or_rlaan):
    lst = capitols[confed_aera_or_rlaan]
    return getRandomShipType(lst)

def getRandomFighter(faction):
    return getRandomFighterInt (factionToInt (faction))

def getRandomCapitol (faction):
    return getRandomCapitolInt (factionToInt (faction))

launch_distance_factor=1
max_radius=10000
min_forward_distance=100000 
min_distance=10000 
#print len(fightersPerFG)
#print len (fighterProductionRate)
#print len(capitalProductionRate)
#print len(enemies)
#print len(rabble)
#print len (friendlies)
#print len(fighters)
#print len(capitals)
#print len(bases)
#print len(useStock)




