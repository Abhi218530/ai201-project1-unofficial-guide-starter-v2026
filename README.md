# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

The Unofficial Guide answers questions about student life using the
campus_life corpus — 88 short posts covering dining halls, housing, courses,
and admin deadlines. Ask something like "how much does laundry cost in
Fenwick Court?" or "is the housing lottery actually random?" and it retrieves
the most relevant posts, checks whether they're close enough to trust, and
generates an answer that names its sources. If nothing in the corpus is
relevant — tax filing, the weather in Antarctica — it says so instead of
guessing.


## Chunking Strategy


**Chunk size:** 800 characters (unchanged from the starter default)
**Overlap:** 120 characters (unchanged from the starter default)

I kept the starter's numbers rather than changing them, because after reading
several documents in Milestone 1 (admin_dining_dollars, course_cs_210,
dining_kestrel_commons, housing_fenwick_court) I found every post in this
corpus is well under 800 characters on its own — the longest chunk I produced
was 549 characters. Chunk size wasn't the actual constraint here; paragraph
structure was. So instead of changing the number, I changed the *strategy*:
I replaced the fixed-character-window fallback with a paragraph-aware
chunker that keeps a whole post as one chunk when it fits, and only splits
on paragraph boundaries (and sentence-packs within an oversized paragraph)
if a post is genuinely too long. On this corpus that produces the same
88 documents → 88 chunks result as the fallback, which makes sense — the
difference would show up on a corpus with longer documents, not this one.

I also noticed while reading that popular topics (CS 210, Fenwick Court)
have their facts repeated across 2-3 separate posts, sometimes word-for-word.
That's not a chunking problem to fix — it's just how this corpus is written
— but it does mean retrieval often correctly pulls back multiple chunks that
confirm the same fact rather than one chunk from one canonical source.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`
```


```

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`
```
BIOL 160 Cell Biology

I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved.

Expect 9 to 11 hours a week, the heaviest first-year course by reputation.

The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.

```

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`
```
Workload for HIST 118 Modern World History

People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time.

It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.

```

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`
```
Re: Pellew Dining Hall

Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely.

Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.

```

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`
```
Innisfree Hall — what it's actually like

Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms.

The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus.

The bad: no air conditioning, which matters for the first three weeks of September.

Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.

```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->
**Question:** How much does laundry cost in Fenwick Court?

**Answer:** In Fenwick Court, laundry costs $2.00 for a wash and $1.75 for a dry.

```
```

**My relevance cutoff:**

I ran my 5 in-scope test questions and the 5 OUT_OF_SCOPE questions and recorded
the best (lowest) distance for each. The in-scope group topped out at 0.282;
the out-of-scope group bottomed out at 0.574 — a clean gap with no overlap.

The starter's default THRESHOLD of 0.6 technically sits inside that gap, but
right on the edge of the out-of-scope side. My "Antarctica" question scored
0.574 — just under 0.6 — meaning it would have passed the gate and relied on
the model to decline in the prompt rather than being stopped outright. That's
exactly the failure mode Milestone 4 warns about: hoping the model declines
instead of deciding in code.

I set THRESHOLD = 0.4, which sits roughly in the middle of the gap — well
above my worst in-scope case (0.282) and well below my best out-of-scope
case (0.574). Re-running the Antarctica question at 0.4 confirmed the gate
now blocks it before any model call ("0 model calls this session").

| Question | In corpus? | Best distance |
|---|---|---|
| How much does laundry cost in Fenwick Court? | Yes | 0.197 |
| Is the housing lottery actually random? | Yes | 0.248 |
| What are the wait times at Kestrel Commons? | Yes | 0.223 |
| Do dining dollars roll over to the next year? | Yes | 0.233 |
| What's the workload like for CS 210? | Yes | 0.282 |
| What's the weather like in Antarctica? | No | 0.574 |
| How do I file my taxes as an international student? | No | 0.670 |
| What's the best recipe for chocolate chip cookies? | No | 0.886 |
| Who won the World Cup in 2022? | No | 0.850 |
| How do I change a flat tire? | No | 0.837 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I asked Claude to write a replacement chunker for Milestone 3, after
describing what I'd found reading campus_life documents — short, mostly
single-paragraph posts, with popular topics like CS 210 or Fenwick Court
split across 2-3 related files. Claude proposed paragraph-aware chunking
with a sentence-packing fallback for oversized paragraphs. I pasted it in
and verified it against real data by running `python app.py index` — it
produced the same 88 documents → 88 chunks as the original fallback, which
made sense once I understood every post here is already under 800
characters. The strategy changed; the count on this particular corpus
didn't, and I had to actually run it to know that rather than assume it.

**2.** For Milestone 4, I ran my 5 in-scope and 5 out-of-scope questions
myself and shared the resulting distances with Claude. It pointed out that
my initial THRESHOLD of 0.6 was riskily close to my worst out-of-scope case
(0.574, the Antarctica question) — technically inside the gap but with
almost no margin. I changed THRESHOLD to 0.4 based on that, then re-ran the
Antarctica question myself to confirm the gate blocked it before any model
call ("0 model calls this session"), rather than just trusting the
suggested number.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
