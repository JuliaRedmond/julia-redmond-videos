"""Source of truth for Batch 2 v2 wording + timing. Wording is exactly as supplied; only layout/timing is computed here."""
import json,os,sys
CARDS="Free Parent Script Cards · link in bio"; KIT="Free 5-Minute Homework Start Kit · link in bio"
TAG="Less Reminding. More Ownership."
def L(t,hl=None): return {"t":t,"hl":hl}
def HOOK(label,lines,strike=False):
    return {"type":"hook","label":label,"lines":[l if isinstance(l,dict) else {"t":l} for l in lines],"strike":strike}
def S(*lines): return {"type":"statement","lines":[l if isinstance(l,dict) else {"t":l} for l in lines]}
def C(items,header=None): return {"type":"checks","header":header or [],"items":[i if isinstance(i,dict) else {"t":i} for i in items]}
def T(note,pre=None,post=None): return {"type":"try","label":"TRY","note":note,"pre":pre or [],"post":post or []}
V={}
def add(n,name,skills,cta,focus,*beats): V[n]=dict(name=name,skills=skills,cta=cta,focus=focus,beats=list(beats))
add(2,"Stop_Planning_For_Them",["PLAN"],KIT,.50,
 HOOK("UNPOPULAR OPINION",[L("Stop planning","Stop planning"),"your child's","homework night",L("for them.","for them.")]),
 S("If you write the list,",L("you're the one who has to remember it.","remember it.")),
 S(L("Let them write it.","write it."),"Even if it's messy. Even if it's slow."),
 T("What's on your list?",pre=["Your job:"],post=["Then wait."]))
add(3,"5_Signs_Time",["TIME"],KIT,.36,
 HOOK("TIME",["5 signs your","child needs help",L("with time,","time,"),L("not motivation","not motivation")]),
 C(['Everything "takes five minutes"',"Big projects start the night before","The evening disappears without warning"]),
 C(["The last task always gets rushed","They can't say what comes next"]),
 S("These are planning skills.",L("And skills can be taught.","can be taught.")))
add(4,"Homework_Spot_Rules",["FOCUS"],KIT,.60,
 HOOK("FOCUS",[L("4 non-negotiables","non-negotiables"),"for the","homework spot"]),
 C(["Phone in another room","Only one assignment on the desk"]),
 C(["Water and supplies before sitting down","A timer for each focus block"]),
 S("Fewer things pulling at them",L("means fewer reminders from you.","fewer reminders")))
add(5,"Lost_And_Found",["ORGANIZE"],CARDS,.30,
 HOOK("STOP DOING THIS",["Stop being","your child's",L("lost-and-found.","lost-and-found.")]),
 S("Every time you find it,",L("they don't have to.","don't have to.")),
 C(["Folder lives in the backpack","Backpack lives by the door","Charger lives at the desk"],header=["Give every school item a home:"]),
 T("Where does it live?",pre=["Then ask:"]))
add(6,"Stop_Checking_First",["FINISH"],KIT,.45,
 HOOK("STOP DOING THIS",[L("Stop checking","Stop checking"),"their homework",L("first.","first.")]),
 S("If you always check first,",L("they learn you're the last step.","last step.")),
 C(["Every question answered?","Name on it?","Back in the folder?"],header=["Teach a Done Check instead:"]),
 S(L("They check first.","check first."),"You look second."))
add(7,"Not_Lazy",["START"],KIT,.55,
 HOOK("START",["Your child",L("isn't lazy.","isn't lazy."),"The first step",L("is too big.","too big.")]),
 S('"Write the essay"',L("is a mountain.","mountain.")),
 S('"Write one sentence about your topic"',L("is a step.","step.")),
 S("Shrink it until it takes",L("five minutes or less.","five minutes or less.")))
add(8,"Two_Minute_Plan",["PLAN"],KIT,.40,
 HOOK("PLAN",[L("The 2-minute","2-minute"),"homework","plan"]),
 C(["List every task","Number them in order","Circle the hardest one","Put it first or second"]),
 S(L("Two minutes of planning","Two minutes of planning"),'saves a lot of "What do I do now?"'))
add(9,"Plenty_Of_Time",["TIME"],CARDS,.35,
 HOOK("STOP SAYING THIS",['"You have','plenty of time."'],strike=True),
 S('To a kid, "plenty"',L('means "later."','"later."')),
 C(["Guess the minutes","Set a timer","Compare when it rings"],header=["Show them the time instead:"]))
add(10,"Breaks_Are_The_Plan",["FOCUS"],KIT,.50,
 HOOK("UNPOPULAR OPINION",[L("Breaks aren't","aren't"),"a reward.","They're part",L("of the plan.","of the plan.")]),
 S("Short focus block.",L("Real break.","Real break."),"Repeat."),
 S("A break with an end time",L("is easier to come back from.","easier to come back from.")))
add(11,"Sunday_Backpack_Reset",["ORGANIZE"],KIT,.30,
 HOOK("ORGANIZE",[L("The 5-minute","5-minute"),"Sunday",L("backpack reset","backpack reset")]),
 C(["Empty everything out","Toss old papers","Finished work stays home"]),
 C(["Refill pencils and paper","Pack for Monday"]),
 S("Five minutes on Sunday",L("means a calmer Monday morning.","calmer Monday morning.")))
add(12,"Six_Skills",["START","PLAN","TIME","FOCUS","ORGANIZE","FINISH"],KIT,.45,
 HOOK("THE SIX SKILLS",["Every finished","homework takes",L("6 skills","6 skills")]),
 C([{"t":"START: take the first step","skill":"START"},{"t":"PLAN: know what comes next","skill":"PLAN"},{"t":"TIME: guess, then check","skill":"TIME"}]),
 C([{"t":"FOCUS: clear what pulls at you","skill":"FOCUS"},{"t":"ORGANIZE: everything has a home","skill":"ORGANIZE"},{"t":'FINISH: check before "done"',"skill":"FINISH"}]),
 S("Teach one at a time.",L("Start with the one that's hardest at your house.","hardest at your house.")))

HOOKD,END,HOLD,TARGET,MAXD=4.4,2.6,1.5,20.3,22.0
def last_event(b):  # unscaled time of the beat's last animation event
    if b["type"]=="statement":
        return max(.1+i*1.2+(.5+.55 if l.get("hl") else 0) for i,l in enumerate(b["lines"]))
    if b["type"]=="checks":
        first=.75 if b["header"] else .35; return first+(len(b["items"])-1)*1.4+.6
    if b["type"]=="try":
        return 2.2+.45 if b["post"] else ((.95 if b["pre"] else .3)+.7)
def plan(spec):
    mids=[b for b in spec["beats"][1:]]
    fixed=HOOKD+END+HOLD*len(mids); E=sum(last_event(b) for b in mids)
    s=max(1.07,min(1.7,(TARGET-fixed)/E))   # 1.07 => item spacing >= 1.5 s
    hold=HOLD
    if fixed+s*E>MAXD: hold=max(1.1,HOLD-(fixed+s*E-MAXD)/len(mids)); fixed=HOOKD+END+hold*len(mids)
    if fixed+s*E>MAXD: s=(MAXD-fixed)/E
    total=fixed+s*E; pad=max(0,(18.6-total)/len(mids)); t=0; out=[]
    for k,b in enumerate(spec["beats"]):
        b=dict(b)
        if k==0: d=HOOKD
        else: b["sc"]=round(s,3); d=last_event(b)*s+hold+pad
        b["start"]=round(t,3); b["end"]=round(t+d,3); t+=d; out.append(b)
    out.append({"type":"end","start":round(t,3),"end":round(t+END,3),"tagline":TAG,"cta":spec["cta"]}); t+=END
    return out,round(t,2),s
def cfg_for(n):
    sp=V[n]; beats,dur,s=plan(sp)
    return {"id":f"{n:02d}_{sp['name']}","skills":sp["skills"],"duration":dur,"focus":sp["focus"],"beats":beats},s
if __name__=="__main__":
    out=sys.argv[1]
    for n in V:
        c,s=cfg_for(n); json.dump(c,open(f"{out}/v{n:02d}.json","w"),indent=1,ensure_ascii=False)
        print(n,c["id"],"dur",c["duration"],"scale",round(s,2),[ (b["type"],round(b["end"]-b["start"],1)) for b in c["beats"]])
