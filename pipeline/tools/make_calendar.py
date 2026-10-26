"""Writes calendar/content-calendar.csv and .md from the rows below. Run: python3 make_calendar.py"""
import csv, datetime, pathlib
OUT = pathlib.Path(__file__).resolve().parents[2] / "calendar"
P, T = "Parent", "Teen"
CARDS, KIT = "Free Parent Script Cards", "Free 5-Minute Homework Start Kit"
WB = "Executive Functioning Workbook for Teens"   # ALL teen-facing videos end on this
BOOKP = "Executive Function for Kids (book; link TBC)"  # parent-facing launch videos
# week 1 themes: 1 Parent scripts / 2 Everyday routines / 3 Study skills
# week 2 themes: 6 Mindset / 7 Seasonal (Nov crunch, break plan) / Launch (six-skill path + books)
R = [
 # id, aud, theme, topic, hook idea, cta
 ("V01",P,"1 Parent scripts","Homework fight: ask for the first step","Homework turning into a fight? Swap one sentence.",CARDS),
 ("V02",T,"3 Study skills","Self-quizzing beats rereading","Rereading your notes feels like studying.",WB),
 ("V03",P,"2 Routines","After-school transition: a landing before homework","Give them a landing before homework.",KIT),
 ("V04",T,"3 Study skills","Shrink a big project to 3 steps","Big project feels huge?",WB),
 ("V05",P,"1 Parent scripts","'I'm bored': say this, not that","Instead of fixing 'I'm bored'...",CARDS),
 ("V06",T,"2 Routines","Night-before backpack check (2 minutes)","Backpack check takes 2 minutes.",WB),
 ("V07",P,"2 Routines","Mornings: let the checklist do the nagging","Let a list do the nagging.",CARDS),
 ("V08",T,"3 Study skills","Emailing a teacher (3-line template)","Scared to email your teacher? Three lines is enough.",WB),
 ("V09",P,"1 Parent scripts","Stop being the family alarm clock","Hand the wake-up job over, with a plan.",CARDS),
 ("V10",T,"2 Routines","Sleep vs late-night homework","The 11pm homework trap and how to dodge it.",WB),
 ("V11",P,"3 Study skills","Study help: ask them to teach it back","Instead of quizzing them...",CARDS),
 ("V12",T,"3 Study skills","Remember what you read","One-sentence summary after every page.",WB),
 ("V13",P,"2 Routines","Sunday 10-minute family reset","Ten minutes Sunday saves Monday.",CARDS),
 ("V14",T,"2 Routines","Pick your 3 must-dos for the week","Don't plan everything. Pick three.",WB),
 # week 2: early-November launch week
 ("V15",P,"6 Mindset","Procrastination isn't laziness","Stuck isn't lazy. It's usually a starting problem.",CARDS),
 ("V16",T,"Launch: Six-Skill Path","START > PLAN > TIME > FOCUS > ORGANIZE > FINISH","One connected path, six skills.",WB),
 ("V17",P,"7 Seasonal","November end-of-term crunch","What's due before break? Map it with them.",CARDS),
 ("V18",T,"6 Mindset","Smart but scattered","Smart and scattered can both be true: skills are buildable.",WB),
 ("V19",P,"Launch: Executive Function for Kids","What's inside the book (no hype, just the method)","Less reminding. More ownership.",BOOKP),
 ("V20",T,"7 Seasonal","End-of-term crunch plan","Work backward from the due date.",WB),
 ("V21",P,"6 Mindset","Celebrate finishing, not perfect","Finished beats flawless.",CARDS),
 ("V22",T,"Launch: Teen workbook","30 short sessions, 6 skills","Less Stress. More Free Time.",WB),
 ("V23",P,"7 Seasonal","December break plan","Plan the break now: three small rules.",CARDS),
 ("V24",T,"6 Mindset","Procrastinating? Try a 2-minute start","Not lazy. Just stuck at the start line.",WB),
 ("V25",P,"Launch: Six-Skill Path","The path for parents: one connected process","No skill ranks above another.",BOOKP),
 ("V26",T,"4 Phones & focus","Where your phone goes during homework","Where your phone goes during homework.",WB),
 ("V27",P,"6 Mindset","'Smart but scattered' isn't a label","Name the skill, not the kid.",CARDS),
 ("V28",T,"Launch: Teen workbook","Which skill is hardest for you? (comment prompt)","START? PLAN? TIME? Tell us.",WB),
 # week 3: phones & focus / independence by age / story shorts (all characters are made-up, text only)
 ("V29",P,"4 Phones & focus","Give the phone a home","Give the phone a home for the night.",KIT),
 ("V30",T,"8 Story shorts","Story: Marcus and the blank page (fix: one bad sentence)","Marcus has an essay due Friday.",WB),
 ("V31",P,"5 Independence by age","What a 9-year-old can own","What a 9-year-old can own.",KIT),
 ("V32",T,"4 Phones & focus","A phone deal you'll actually keep","Make a phone deal you'll actually keep.",WB),
 ("V33",P,"8 Story shorts","Story: Priya's morning hunt (fix: where does it live?)","Every morning, Priya asks: Where's my...?",CARDS),
 ("V34",T,"5 Independence by age","At 15, own your plan","At 15, you can own your plan.",WB),
 ("V35",P,"5 Independence by age","What a 12-year-old can own","What a 12-year-old can own.",KIT),
 ("V36",T,"8 Story shorts","Story: Diego's missing turn-in (fix: turn it in, then check)","Diego did it. Then forgot to turn it in.",WB),
 ("V37",P,"4 Phones & focus","Parent script: what would be a fair screen deal?","Instead of announcing the screen rule...",CARDS),
 ("V38",T,"5 Independence by age","Chores are planning practice (the chore test)","Chores are planning practice.",WB),
 ("V39",P,"8 Story shorts","Story: Owen's five more minutes (fix: a visible timer)","Owen: Just five more minutes.",KIT),
 ("V40",T,"4 Phones & focus","Silence it before you start","Silence it before you start.",WB),
 ("V41",P,"5 Independence by age","Chores build planning","Chores build planning.",CARDS),
 ("V42",T,"8 Story shorts","Story: Fatima's group project (fix: a name next to every step)","Fatima's group project is due. Who's doing what?",WB),
]
start = datetime.date(2026,10,27)  # Tue
rows=[]
for i,(vid,aud,theme,topic,hook,cta) in enumerate(R):
    d = start + datetime.timedelta(days=i//2)
    rows.append(dict(Date=d.isoformat(), Day=d.strftime("%a"), Slot="AM" if i%2==0 else "PM", ID=vid, Audience=aud, Theme=theme,
        Topic=topic, Hook_idea=hook, CTA=cta, Status="Approved" if int(vid[1:])<=28 else ("BUILT, awaiting approval (week 3)" if int(vid[1:])<=42 else "Planned")))
OUT.mkdir(exist_ok=True)
with open(OUT/"content-calendar.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
md=["# Content calendar: Tue 27 Oct to Mon 16 Nov 2026 (2 videos/day)\n",
"Nothing here is scheduled or posted. Scheduling happens in Metricool after approval.\n",
"- **Week 1 (27 Oct - 2 Nov):** Parent scripts, Everyday routines, Study skills.",
"- **Week 2 (3 - 9 Nov, early-November launch week):** Mindset, Seasonal (November crunch / December break), and the Six-Skill Path / book videos.",
"- **Week 3 (10 - 16 Nov):** Phones & focus, Independence by age, Story shorts (Marcus, Priya, Diego, Owen, Fatima: made-up characters, text only, each ends with the fix).",
"- Daily pattern: AM = parent-facing, PM = teen-facing.",
"- **CTA rule:** parent-facing videos end on the Free Parent Script Cards or the Free 5-Minute Homework Start Kit (both are for parents of kids 9-13). Every teen-facing video ends on **Executive Functioning Workbook for Teens**. Parent launch videos point to *Executive Function for Kids* (link TBC). The renderer refuses a teen video with a parent CTA.",
"- Still unused: January school reset (save for mid-January launch week), plus more seasonal and story ideas.\n",
"| Date | Slot | ID | Audience | Theme | Topic | Hook idea | CTA | Status |","|---|---|---|---|---|---|---|---|---|"]
for r in rows: md.append(f"| {r['Day']} {r['Date'][5:]} | {r['Slot']} | {r['ID']} | {r['Audience']} | {r['Theme']} | {r['Topic']} | {r['Hook_idea']} | {r['CTA']} | {r['Status']} |")
(OUT/"content-calendar.md").write_text("\n".join(md)+"\n")
print(len(rows),"rows")
