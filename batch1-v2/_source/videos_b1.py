"""Batch 1 v2: wording + timing. Same helpers/planner approach as batch2-v2/_source/videos.py (extended for 20-30 s)."""
import json,sys
CARDS="Free Parent Script Cards · link in bio"; KIT="Free 5-Minute Homework Start Kit · link in bio"
TAG="Less Reminding. More Ownership."
def L(t,hl=None,strike=False): return {"t":t,"hl":hl,"strike":strike}
def HOOK(label,lines,strike=False): return {"type":"hook","label":label,"lines":[l if isinstance(l,dict) else {"t":l} for l in lines],"strike":strike}
def S(*lines): return {"type":"statement","lines":[l if isinstance(l,dict) else {"t":l} for l in lines]}
def T(note,label="TRY",pre=None): return {"type":"try","label":label,"note":note,"pre":pre or [],"post":[]}
SIX=["START","PLAN","TIME","FOCUS","ORGANIZE","FINISH"]
def CH(): return {"type":"chips","skills":SIX}
V={}
def add(key,file,skill,cta,focus,*beats): V[key]=dict(file=file,skills=[skill],cta=cta,focus=focus,beats=list(beats))
add("PS2","JuliaRedmond_B1v2_PS2_Whats_On_Your_List","PLAN",CARDS,.50,
 HOOK("PARENT SCRIPT #2",["Instead of listing",L("their tasks","their tasks"),"for them…"]),
 T("What's on your list tonight?",label="ASK"),
 S("When they say the plan out loud,",L("they own the plan.","own the plan.")))
add("HR2","JuliaRedmond_B1v2_HR2_List_Comes_First","PLAN","Save this for tonight",.42,
 HOOK("HOMEWORK RULE #2",["The list",L("comes first.","comes first.")]),
 S(L("When your child writes the plan…","writes the plan…")),
 S("…they stop asking you",L('"What\'s next?"',strike=True)))
add("PS3","JuliaRedmond_B1v2_PS3_How_Many_Minutes","TIME",CARDS,.36,
 HOOK("PARENT SCRIPT #3",["Trade",'"Hurry up!"…'],strike=[1]),
 T("How many minutes do you think this will take?",label="",pre=["…for"]),
 S(L("A guess turns rushing into a plan.","turns rushing into a plan.")),
 S(L("The timer does the reminding.","timer")))
add("HR3","JuliaRedmond_B1v2_HR3_Guess_Then_Check","TIME",KIT,.60,
 HOOK("HOMEWORK RULE #3",["Guess,",L("then check.","then check.")]),
 S("Most kids have no idea how long",L('"20 problems" takes.','"20 problems"')),
 S("A week of guessing and timing",L("teaches them faster than any reminder.","faster than any reminder.")))
add("PS4","JuliaRedmond_B1v2_PS4_Move_It_Out_Of_The_Way","FOCUS",CARDS,.55,
 HOOK("PARENT SCRIPT #4",["Instead of",'"Stop getting','distracted!"…'],strike=[1,2]),
 T("What do you need to move out of the way?",label="TRY"),
 S(L("Your child spots the distraction…","spots the distraction…")),
 S(L("…and learns to clear it next time.","learns to clear it")))
add("HR4","JuliaRedmond_B1v2_HR4_Change_The_Room","FOCUS",KIT,.45,
 HOOK("HOMEWORK RULE #4",[L("Change the room,","Change the room,"),"not the lecture."]),
 S('"Focus!" works for',L("about 30 seconds.","about 30 seconds.")),
 S("Clearing the desk and moving the phone",L("works all evening.","works all evening.")))
add("PS5","JuliaRedmond_B1v2_PS5_Where_Does_It_Live","ORGANIZE",CARDS,.30,
 HOOK("PARENT SCRIPT #5",["Swap",'"Where did you','leave it?"…'],strike=[1,2]),
 T("Where does it live?",label="",pre=["…for"]),
 S("One question points to the home,",L("not the mess.","not the mess.")))
add("HR5","JuliaRedmond_B1v2_HR5_Home_Use_Return","ORGANIZE",KIT,.35,
 HOOK("HOMEWORK RULE #5",[L("Home.","Home."),L("Use.","Use."),L("Return.","Return.")]),
 S("Three words that end the nightly",L("hunt for the missing worksheet.","missing worksheet.")),
 S("Which item goes missing",L("most at your house?","most at your house?")))
add("PS6","JuliaRedmond_B1v2_PS6_Show_Me_Your_Done_Check","FINISH",CARDS,.50,
 HOOK("PARENT SCRIPT #6",["Instead of",'"Are you done?"…'],strike=[1]),
 T("Show me your Done Check.",label="SAY"),
 S(L("You stop being the checker.","the checker.")),
 S(L("They start checking their own work.","their own work.")))
add("HR6","JuliaRedmond_B1v2_HR6_Done_Means_Checked","FINISH",KIT,.40,
 HOOK("HOMEWORK RULE #6",['"Done"',L("means checked.","means checked.")]),
 S("A three-box Done Check moves the final",L("check from you to your child.","from you to your child.")),
 CH())
HOOKD,END,HOLD,TARGET,MIN,MAXD=4.4,2.6,1.5,23.0,20.0,30.0
def last_event(b):
    if b["type"]=="statement":
        return max(.1+i*1.2+(1.4 if l.get("strike") else (1.05 if l.get("hl") else 0)) for i,l in enumerate(b["lines"]))
    if b["type"]=="try":
        return (.7 if not b["label"] else (.95 if b["pre"] else .3))+.7
    if b["type"]=="chips": return .2+5*.35+.45
def plan(sp):
    mids=sp["beats"][1:]; fixed=HOOKD+END+HOLD*len(mids); E=sum(last_event(b) for b in mids)
    s=max(1.07,min(2.0,(TARGET-fixed)/E)); total=fixed+s*E
    w_h,w_m,w_e=1,2,.5; extra=max(0,MIN-total); W=w_h+w_m*len(mids)+w_e
    ph=extra*w_h/W; pm=extra*w_m/W; pe=extra*w_e/W; t=0; out=[]
    for k,b in enumerate(sp["beats"]):
        b=dict(b)
        if k==0: d=HOOKD+ph
        else: b["sc"]=round(s,3); d=last_event(b)*s+HOLD+pm
        b["start"]=round(t,3); b["end"]=round(t+d,3); t+=d; out.append(b)
    out.append({"type":"end","start":round(t,3),"end":round(t+END+pe,3),"tagline":TAG,"cta":sp["cta"]}); t+=END+pe
    return out,round(t,2),s
def cfg_for(key):
    sp=V[key]; beats,dur,s=plan(sp)
    return {"id":sp["file"],"skills":sp["skills"],"duration":dur,"focus":sp["focus"],"beats":beats},s
if __name__=="__main__":
    out=sys.argv[1]
    for k in V:
        c,s=cfg_for(k); json.dump(c,open(f"{out}/{k}.json","w"),indent=1,ensure_ascii=False)
        print(k,"dur",c["duration"],"s",round(s,2),[(b["type"][:4],round(b["end"]-b["start"],1)) for b in c["beats"]])
