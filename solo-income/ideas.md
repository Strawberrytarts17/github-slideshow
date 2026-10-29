# Solo Income Ideas

Single source list for the brainstorm. Agents add ideas; the orchestrator merges, dedupes, and shortlists.
Instructions for round agents: [round-agent.md](round-agent.md).

## Status (resume here)

- **Now:** Round 3 (L7, L8, L9) running. Rounds 1–2 merged: I-001–I-048.
- **Next:** Round 4 (L10, L11, L12), then the shortlist: top 3 ideas to test, each with a first silent test.
- **Stop rule:** end rounds early if a round accepts <50% of proposals, or if L12 reports saturation.
- **To resume:** open Claude Code on branch `claude/brainstorm-solo-income-repr78` and say *"Resume the brainstorm from solo-income/ideas.md Status."* The loop is in [round-agent.md](round-agent.md#orchestrator-loop).

## Brief (condensed)

**Goal:** Financial independence from something people pay for, in places others haven't noticed. Be early: money already flows to a bad/outdated solution that AI + data recently made cheap to fix. Solo, start small, first dollar fast.

**Resources (options, not requirements)**
- Time: ~40 hrs/week.
- Tools: Claude (chat, Claude Code, Cowork, sandbox), Notion, Google Drive/Gmail/Calendar, Indeed job search, Anthropic Economic Index, PubMed, local AI models, agent-instruction writing. Methods: Fermi sizing, Bayesian A/B, trend detection, AI-tagged text clustering.
- Library (Lane card): Ohio Web Library (Business Source Premier, Small Business Reference Center, Sanborn Fire Insurance Maps, Lynda.com, Home Improvement / Hobbies & Crafts / Science Reference Centers, Oxford Research Encyclopedias, Chilton Library), Butler County digital history archive, Hamilton Journal-News on PressReader, Kanopy (Great Courses), Libby, Lane Seed Library, Fairfield branch stacks.
- Public data: data.gov, Census, BLS, Federal Register, Ohio + Butler County records, building permits, public bid notices. Public domain: US works from 1931 enter it **Jan 1, 2027** (1930 and earlier already free).
- Skills/builds: solo game dev, chess player + coach, gardener (plant propagation), systems thinker building versioned knowledge catalogs. Reusable builds: chess game-analysis pipeline, garden planning catalog, budgeting app, agent-instruction builder.
- Location: East Hamilton, Ohio (Butler County), between Cincinnati and Dayton.

**Constraints**
- Solo. No interviews, calls, cold email, or DMs. Validate silently: landing pages, listings, pre-orders, small ads, public data.
- Budget: unset, so assume ~$0/month. Current income: unspecified, so don't put it at risk. No-go areas: none listed yet.
- One active bet; at most 3 ideas in test.
- Prefer first dollar within weeks.
- No deception, no ToS-violating scraping, no products built on personal data about individuals; reproduce only public-domain works. Legal review before regulated areas (cannabis, health, finance, legal services, kids).
- Short outputs, explicit decisions.

## Idea card format

```
### I-000 · Short name
- Money now flows to: <who pays what, today, for the bad/outdated solution>
- Why now: <what AI/data/date change made the fix cheap or opened the window>
- Edge: <resource, skill, location, or constraint this exploits>
- Silent test: <no-contact validation + pass/fail threshold>
- First $: <what is sold, price, est. days to first dollar>
- Flags: <legal/ethics/risk, or none>
- Unique: <how it differs from the closest idea already listed>
- Tags: customer=<..> · mechanism=<..> · resource=<..>
- Score (1-5): speed <n> · early <n> · fit <n> · ceiling <n>
```

## Ideas

<!-- Orchestrator appends merged rounds below. Agents never edit this file directly. -->

**Round 1** (L1 stale flows · L2 free assets · L3 skills)

### I-001 · Title II-ready minutes & agendas for small Ohio public bodies
- Money now flows to: Ohio's ~1,300 townships, ~680 villages, library/school boards and special districts pay clerks and fiscal officers 3-6 hrs per meeting to type minutes, agenda-software vendors (CivicPlus/Granicus/BoardDocs-class, ~$3k-$15k/yr), and PDF-remediation shops ($3-$15/page), while most still post untagged scanned PDFs.
- Why now: DOJ's ADA Title II web rule (Federal Register, Apr 24, 2024) requires WCAG 2.1 AA for newly posted web content, PDFs included, by Apr 26, 2027 for public entities under 50k population and all special districts. AI now drafts motion/vote-format minutes from a meeting recording and outputs tagged PDF + accessible HTML for cents.
- Edge: Claude Code pipeline (recording → minutes draft → accessible HTML/PDF with alt text); Federal Register monitoring for any deadline change; local familiarity with Butler County township meetings, many already streamed to YouTube.
- Silent test: (1) Auto-scan 100 SW Ohio township/village/special-district sites; pass if ≥60% of 2026 agenda/minutes PDFs fail basic PDF/UA checks (untagged, no title/language). (2) Publish a free "Title II PDF scan" page + $79/mo plan; pass ≥40 scans and ≥2 paid (card or PO) within 60 days; fail <15 scans or 0 paid.
- First $: $79/mo (4 meetings: minutes draft + accessible agenda/minutes) or $4/page one-off remediation; ~30-60 days.
- Flags: Sell "WCAG 2.1 AA conformance checks," never "ADA compliance guaranteed"; confirm in the Federal Register that DOJ hasn't moved the date before building.
- Unique: No accepted ideas yet; closest in this batch is I-008 (transcription via RFQs). This one is a self-serve subscription for local bodies, driven by a dated federal mandate, not audio work won by bidding.
- Tags: customer=small local governments · mechanism=deadline-driven compliance subscription · resource=Federal Register + Claude Code + public meeting recordings
- Score (1-5): speed 3 · early 4 · fit 3 · ceiling 4

### I-002 · Pre-shredded compliance matrices for open federal solicitations
- Money now flows to: small federal contractors and grant applicants pay proposal consultants $500-$2,500 per "RFP shred" (every Section L/M or NOFO requirement, page limit, format rule and evaluation factor in one matrix) or spend 6-15 staff hours on each. Indeed carries steady "proposal coordinator" postings whose first task on every bid is this. AI proposal platforms charge $500+/mo per seat.
- Why now: LLMs now extract every shall/must, page limit and scoring factor from a 150-page package in minutes. SAM.gov and Grants.gov expose notices and attachments through free public APIs. The 2025-26 FAR overhaul (class deviations) is reshuffling clauses, so even experienced teams re-check.
- Edge: One shred, many buyers: each solicitation draws 5-50 bidders who all need the same matrix. Exact-match pages per solicitation/NOFO number face little competition, and bidders already search those numbers. Agent-instruction writing gives a repeatable extraction spec.
- Silent test: Publish 60 pages for open small-business set-aside RFPs and NOFOs with ≥30 days to deadline (free summary + key dates; $59 Excel matrix). Pass: ≥3 sales within 30 days of indexing. Fail: 0 sales with ≥300 visits (no willingness to pay) or <100 visits (channel dead).
- First $: $59 per solicitation matrix, $19 per amendment update; ~21-35 days.
- Flags: Accuracy disclaimer (buyer verifies against source); public attachments only; Google "scaled content" risk, so every page must carry real analysis.
- Unique: No accepted ideas yet; closest in this batch is I-003 (also mines procurement documents). This one pulls forward-looking requirements from open bids and resells one analysis to every competitor on the same solicitation.
- Tags: customer=small gov contractors & grant writers · mechanism=one-to-many derivative report via exact-match search · resource=SAM.gov/Grants.gov public data + Claude
- Score (1-5): speed 3 · early 3 · fit 4 · ceiling 4

### I-003 · SW Ohio local public-works unit-price book
- Money now flows to: small civil firms, township/village administrators and municipal grant writers price engineer's estimates and OPWC/CDBG/TAP grant applications for paving, curb, sidewalk and waterline jobs. They pay RSMeans (~$400-$1,500/yr) or DOT bid-tab databases, or lean on ODOT statewide averages that run low for small local quantities.
- Why now: Bid tabulations from dozens of SW Ohio cities, townships, county engineers and school districts sit as scanned PDFs in council packets and on bid pages. Vision LLMs now turn a scanned tab into clean rows (item, unit, quantity, every bidder's price) for pennies. ODOT CMS item numbers (e.g., 441 asphalt, 608 walks, 609 curb) give a free key for normalizing items.
- Edge: Local geography (Butler/Hamilton/Warren/Montgomery); the versioned-catalog habit (quarterly editions with change logs); Fermi sizing for regional adjustments.
- Silent test: Pre-check: ≥40 tabs from 2025-26, covering ≥20 jurisdictions, are publicly posted (else stop). Then publish a free 15-item "2026 SW Ohio local unit prices" page and gate the ~150-item Excel at $129. Pass: ≥3 sales or ≥25 next-edition sign-ups within 45 days. Fail: 0 sales and <10 sign-ups.
- First $: $129/yr regional book (single county $39); ~30-45 days.
- Flags: None (bidders are businesses and tabs are public records); fill gaps through Ohio public-records web forms, not calls.
- Unique: No accepted ideas yet; closest in this batch is I-002. This one turns past award prices into cost data for estimators instead of extracting requirements from open bids.
- Tags: customer=civil engineers, small municipalities, grant writers · mechanism=aggregated cost-data product · resource=public bid tabulations + vision extraction
- Score (1-5): speed 3 · early 4 · fit 4 · ceiling 3

### I-004 · PJM peak-hour alerts for Ohio facilities after the capacity-price spike
- Money now flows to: Ohio commercial and industrial sites (manufacturers, cold storage, water/wastewater plants, school districts) pay PJM capacity charges set by their load during the summer's 5 coincident peak hours. Summer 2027's peaks set the tag billed Jun 2028-May 2029. They also give demand-response aggregators and energy brokers a share of savings for peak calls, or simply absorb the charge.
- Why now: PJM capacity prices jumped from ~$29/MW-day (2024/25) to ~$270 (2025/26) and the ~$329 cap (2026/27), driven by data-center load. A 500 kW site that sheds 100 kW in the right hours saves ~$12k/yr. EIA/PJM hourly load data and NOAA forecasts are free, and a Bayesian model of "P(today holds a top-5 hour)" is cheap to run.
- Edge: Bayesian and trend-detection methods from the brief; local zones (AES Ohio/Dayton, Duke Energy Ohio/Cincinnati); a fully silent subscription that needs no client data.
- Silent test: (1) Backtest summers 2021-2025: pass if the model catches ≥4 of 5 actual 5CP days each year with ≤12 alert days per summer; fail if it misses ≥2 in any two years. (2) Publish a "how your capacity tag is set + backtest" page with a $149 Summer-2027 pre-order; pass ≥5 pre-orders or ≥40 waitlist sign-ups by Mar 31, 2027.
- First $: $149/season alert subscription (SMS + email, day-ahead and same-day), pre-sold over the winter; ~45-90 days to the first pre-order.
- Flags: Not energy advice and no savings guarantee; verify each utility's tag method (5CP vs zonal peaks); publish our own forecasts, not redistributed PJM data; load shedding with generators has air-permit limits.
- Unique: No accepted ideas yet; closest in this batch is I-005 (also a recurring subscription). This is the only card that forecasts a cost-setting grid event, and it differs in resource (public grid/weather data), buyer (facility managers) and money flow (capacity charges).
- Tags: customer=Ohio C&I facility managers · mechanism=predictive alert subscription · resource=EIA/PJM/NOAA public data + Bayesian methods
- Score (1-5): speed 2 · early 5 · fit 4 · ceiling 4

### I-005 · SW Ohio contractor-registration & permit-rules tracker
- Money now flows to: HVAC, plumbing, electrical, roofing, fence and sign contractors working across SW Ohio pay office staff or "permit/licensing coordinators" (recurring Indeed postings) to re-learn each building department's annual registration (state license copy, COI, bond, fee) and its per-job permit rules. Multi-state firms pay licensing vendors and permit expediters.
- Why now: Butler County alone splits approvals among several city building departments, township zoning offices and the county building department. AI can now read each department's pages and PDF forms, extract fees, required documents and expiry dates, and flag changes monthly, maintenance that used to take a person. Many registrations run on the calendar year, so renewal searches peak in Dec-Jan.
- Edge: The versioned knowledge-catalog skill (dated, change-logged entries); local geography; Notion/Google Sheets as zero-cost delivery.
- Silent test: Pre-check: ≥25 of 40 Cincinnati-Dayton jurisdictions require annual contractor registration (public pages). Publish 40 "Contractor registration in [jurisdiction], OH: 2027 fee, documents, deadline" pages by Dec 1. Sell a $79/yr tracker (all jurisdictions + renewal calendar + change alerts + pre-filled form packets). Pass: ≥4 sales by Jan 31, 2027. Fail: <1 sale with ≥300 visits.
- First $: $79/yr tracker (single-jurisdiction packet $15); ~30-45 days, riding the December renewal rush.
- Flags: None significant; show "last verified" dates; no legal advice.
- Unique: No accepted ideas yet; closest in this batch is I-003 (SW Ohio public-records catalog). This one is a living requirements catalog, timed to the renewal season and sold to contractors, not cost data.
- Tags: customer=multi-jurisdiction trade contractors · mechanism=versioned requirements-catalog subscription · resource=building-department public info + catalog skill
- Score (1-5): speed 3 · early 3 · fit 4 · ceiling 3

### I-006 · TTB label (COLA) pre-check for craft beverage makers
- Money now flows to: Breweries, wineries and distilleries file well over 100,000 federal label applications (COLAs) a year. They pay label-compliance consultants ~$75-$250 per label, or lose days to weeks per "Needs Correction" return when they miss a Government Warning, class/type, net-contents or type-size rule. Seasonal releases make this weekly work.
- Why now: Vision LLMs can now read label artwork and check it against 27 CFR Parts 4/5/7, reorganized by TTB's 2020 modernization rule. TTB's free Public COLA Registry offers thousands of approved examples to calibrate against. Pending TTB allergen and "Alcohol Facts" proposals (Jan 2025) would force mass relabeling if finalized.
- Edge: A versioned rules catalog that tracks TTB Federal Register changes; agent-instruction writing for consistent checks; the Cincinnati-Dayton craft-beverage cluster (minor).
- Silent test: (1) Run the checker on 300 approved registry labels, sampled slowly; pass if false "fail" flags are ≤10%. (2) Publish a free Government Warning/mandatory-items checker plus a $12 full pre-check; pass ≥5 paid labels within 45 days; fail <2.
- First $: $12/label or $39/mo unlimited; ~21-35 days.
- Flags: Legal review (alcohol labeling); advisory only, with no approval guarantee or legal advice.
- Unique: No accepted ideas yet; closest in this batch is I-002 (AI extraction of federal requirements). This one checks the buyer's own artwork against fixed rules before filing, to avoid rejection, and is sold per label to beverage makers.
- Tags: customer=craft breweries/wineries/distilleries · mechanism=pre-filing compliance check · resource=27 CFR rules + TTB public COLA registry + vision AI
- Score (1-5): speed 3 · early 4 · fit 3 · ceiling 3

### I-007 · Phase I ESA historical-use summaries from public-domain maps
- Money now flows to: Environmental consultants doing lender-required Phase I site assessments (ASTM E1527-21, recognized by EPA's AAI rule) buy historical-source bundles from legacy vendors (EDR/LightBox, ERIS): Sanborn map, city-directory, topo and aerial reports, commonly several hundred dollars per site. They still pay staff hours to turn those into a land-use chronology.
- Why now: LOC's public-domain Sanborn scans, USGS historical topos and aerials, and pre-1931 directories are free. Vision models can read map labels ("Filling Sta.", "Gasoline Tanks", "Foundry") and draft the chronology. On Jan 1, 2027, 1931 editions also enter the public domain and can be reproduced in deliverables.
- Edge: Lane card access to the Sanborn database and the Butler County digital history archive for research (facts only; no licensed images republished); SW Ohio industrial history (Hamilton/Middletown paper mills, foundries); a per-address source catalog.
- Silent test: Publish a free "historical source availability" checker for SW Ohio addresses (which PD Sanborn years/sheets, topo editions and aerial years exist), targeting "Sanborn map [city] Ohio" and "EDR alternative"; upsell a $149 historical-use summary. Pass: ≥30 checks and ≥2 paid summaries within 60 days. Fail: 0 paid.
- First $: $149 per site summary (source table + interpreted chronology + links); ~30-60 days.
- Flags: Confirm the library database license allows commercial research use, and reproduce only PD scans in deliverables. This is not a Phase I; the environmental professional signs. Report residential directory entries without names.
- Unique: No accepted ideas yet; closest in this batch is I-003 (local public-records data). This one replaces a legacy vendor's per-site research package using public-domain historical maps and sells to environmental consultants.
- Tags: customer=environmental consultants · mechanism=per-site research report undercutting a legacy vendor · resource=public-domain maps + library + 1931 wave
- Score (1-5): speed 2 · early 4 · fit 3 · ceiling 3

### I-008 · On-device AI transcription bid into government RFQs
- Money now flows to: Federal agencies (oral histories, research interviews, listening sessions, advisory meetings) and Ohio universities and agencies award transcription and captioning RFQs at human-labor rates (~$1.25-$3.00 per audio minute). These buys often require US-based handling and limit uploading the buyer's audio to third-party AI clouds.
- Why now: Whisper-class local models with speaker separation now reach near-human accuracy on clean audio on a home PC. A solo US-based seller can quote ~$0.85/min with personal QA (~$40-$60/hr effective) and nothing leaves the machine. SAM.gov and OhioBuys registration are free.
- Edge: Local AI models (a brief resource) as the security and price edge; 40 hrs/week for QA; public bid portals as an outreach-free channel.
- Silent test: Register (SAM UEI, OhioBuys supplier). For 30 days, log every transcription/captioning RFQ on SAM.gov, OhioBuys and the Miami U/UC/Wright State bid pages, and quote every eligible one at $0.85/min. Pass: ≥8 eligible RFQs/month and ≥1 award within 75 days. Fail: <4 RFQs/month, or 0 awards after 10 quotes.
- First $: One order (~$500-$3,000), paid net-30 via IPP or state invoice; ~45-75 days.
- Flags: Avoid PHI/CUI work (legal review if pursued); disclose the AI-assisted workflow where solicitations require it; size certifications must be truthful.
- Unique: No accepted ideas yet; closest in this batch is I-001 (minutes drafting for local bodies). This one wins posted purchases by bidding, with on-device processing as the edge, rather than selling a self-serve compliance subscription.
- Tags: customer=federal & state agencies · mechanism=AI-delivered service won via public RFQs · resource=local AI models + SAM.gov/OhioBuys
- Score (1-5): speed 2 · early 3 · fit 3 · ceiling 2

### I-009 · Public-Domain Real Book (annual edition)
- Money now flows to: Musicians pay Hal Leonard ~$40 for The Real Book and ~$5–6 per licensed lead sheet. Arrangers who sell charts of standards go through licensed channels (ArrangeMe pays ~10% on copyrighted titles vs ~50% on PD) or ask publishers for print permission. Band arrangers pay a clearance fee for each tune.
- Why now: On Jan 1, 2027, 1931 compositions become PD in the US, including All of Me, As Time Goes By, Dream a Little Dream of Me, Out of Nowhere, Dancing in the Dark, I Surrender Dear and Between the Devil and the Deep Blue Sea. They join the 1929–30 standards already free (Body and Soul, I Got Rhythm, Embraceable You, Georgia on My Mind, Honeysuckle Rose). The core jazz-standard years now go PD one year at a time. Music OCR plus Claude-written LilyPond/MusicXML turns an original 1931 sheet (melody, lyrics, printed uke chords) into a lead sheet in about an hour.
- Edge: Every page cites the song's first-publication year and renewal record, so arrangers and YouTubers know it's safe to use. That rights check is what buyers pay for. A new edition every Jan 1 (2028 adds 1932) gives a recurring launch that nobody else is timing.
- Silent test: By mid-Nov, post 20 lead sheets of standards that are already PD (1930 or earlier) on ArrangeMe at $4.99; they show up in Sheet Music Plus search. Also publish a 60-tune "2026 Edition" on KDP (US territory only) at $19.99. Pass: ≥25 paid units in 30 days, then publish the 2027 Edition on Jan 1. Fail: <8.
- First $: $4.99 lead sheet or $19.99 book; ~10–20 days (ArrangeMe review takes about a week).
- Flags: legal review. Sell in the US only: many of these writers died after 1955, so the songs are still copyrighted abroad. Check each song's publication vs registration year and its renewal record. Transcribe only the original published melody and harmony, never later recorded versions or publisher re-arrangements.
- Unique: No accepted ideas yet. Nearest in this batch is I-012 (plays), which differs in resource (song sheet music), buyer (musicians/arrangers) and the fee it replaces (print and arrangement licensing, not performance royalties).
- Tags: customer=musicians/arrangers · mechanism=rights-verified PD compilation, annual · resource=1931 PD wave (compositions)
- Score (1-5): speed 4 · early 4 · fit 3 · ceiling 3

### I-010 · US-only bilingual editions of 1931 Simenon & Kästner
- Money now flows to: US learners of French and German pay $12–25 for graded readers and parallel texts (Penguin Parallel Text, Dover Dual-Language, simplified-story series). Most of these are 19th-century classics or stories written for learners. The readable genre fiction intermediate learners want, such as Simenon's Maigret novels and Kästner, has no facing-page editions because it is still under copyright in Europe.
- Why now: Foreign works first published in 1931 leave US copyright on Jan 1, 2027 (95-year term for works restored under URAA) but stay protected in the EU. That includes about 10 Maigret novels from 1931 (Le Chien jaune, La Nuit du carrefour, Monsieur Gallet décédé…) and Kästner's Pünktchen und Anton. AI translation, glossing and text-to-speech audio make a facing-page B1/B2 edition about a week's work.
- Edge: Uses a constraint most PD publishers avoid: rights that apply in one territory only. KDP, Google Play and Apple Books all allow US-only publishing, so the window is open to anyone who works out the URAA dates.
- Silent test: Now: publish Emil und die Detektive (1929, PD in the US since 2025) as a German–English parallel edition with glossary and audio links. List it KDP US-only at $9.99 ebook / $16.99 paperback. Pass: ≥20 sales in 45 days, then line up three 1931 Maigrets for Jan 1. Fail: <5.
- First $: $9.99 ebook (a new translation counts as differentiated, so it qualifies for KDP's 70% royalty); ~10–20 days.
- Flags: legal review. US territory only. Confirm each title's first-publication date (some Maigrets were serialized in 1930, which is still fine in the US). Check US trademark filings on character names before using them in titles. Market to teen and adult learners, not to children.
- Unique: No accepted ideas yet. Nearest in this batch is I-013 (reprints), which uses a different constraint (non-renewal, not the US-vs-EU term split) and a different method (reprinting, not new translation plus learner notes).
- Tags: customer=US language learners · mechanism=AI translation + parallel-text apparatus · resource=1931 PD wave (foreign works, US-only)
- Score (1-5): speed 4 · early 5 · fit 3 · ceiling 4

### I-011 · Clearance-free 1926 sample kits
- Money now flows to: Producers pay $20–40 per sample pack, and clearing a vintage record usually costs four figures. Many electro-swing, lo-fi and boom-bap producers sample 1920s jazz without clearance and get takedowns. Indie game devs pay stock libraries for "1920s jazz" cues.
- Why now: Under the Music Modernization Act's 100-year rule, US records released in 1926 become PD on Jan 1, 2027, following 1923–25. Their compositions are already PD, so both the recording and the song are clean. Free AI stem separation (Demucs) and denoising can now pull usable horn, piano, banjo, guitar and vocal stems out of a 78, which wasn't possible cleanly before.
- Edge: Game-dev audio sense plus local AI models. Each loop gets a provenance sheet (label, matrix number, release date, composer and death year), which is what makes "clearance-free" credible. Prefer composers who died before 1956, such as Blind Lemon Jefferson (1926 Paramount releases) and Jelly Roll Morton, so the kits are clean in most countries, not just the US.
- Silent test: Now: release a free 10-loop sampler and a $19 kit built from 1923–25 releases on BeatStars (sound kits) and itch.io (game audio). Add the 1926 kit on Jan 1. Pass: ≥10 paid kits and ≥50 free downloads in 30 days. Fail: <3 paid.
- First $: $19 sound kit; ~7–14 days.
- Flags: legal review. Use only raw, unrestored transfers or discs you digitize yourself, because commercial remasters may claim new rights. Check the release year (not the recording year) of each side. Tell buyers that reissue labels' Content ID can wrongly claim PD audio.
- Unique: No accepted ideas yet. Nearest in this batch is I-009, which sells written compositions under the 1931 cutoff. This sells processed sound recordings under the separate MMA rule (1926), to producers and game devs.
- Tags: customer=music producers/indie game devs · mechanism=AI stem separation + provenance packaging · resource=PD sound recordings (MMA 1926 cohort)
- Score (1-5): speed 4 · early 4 · fit 4 · ceiling 3

### I-012 · Royalty-free editions of newly-PD stage plays
- Money now flows to: US community theaters, schools and colleges pay licensing houses (Concord Theatricals, Dramatists Play Service) about $75–150 per performance plus $10–14 per acting edition. They pay this even for plays already PD in the US, such as Hay Fever (1925), The Front Page (1928), Journey's End (1929), Street Scene (1929), Private Lives (1930) and Once in a Lifetime (1930).
- Why now: PD status has just reached the late-1920s Broadway and West End plays these groups still stage. Jan 1, 2027 adds plays published in 1931, such as Mourning Becomes Electra and Green Grow the Lilacs (the source of Oklahoma!). Theaters choose their 2027–28 seasons in Jan–Mar, right when the 1931 plays become free. AI cleans up OCR of first editions and produces line counts, cue scripts and 90-minute cuts in hours.
- Edge: Licensing houses have no reason to point out PD status. A one-page US rights memo (publication date and term math) is what makes buyers trust the edition. Buyers are organizations that order 15–30 cast copies at once.
- Silent test: Publish 3 performance editions (wide margins, line numbers, rights memo, suggested cuts) as KDP paperbacks at $8.99, sold on amazon.com only. Pass: ≥25 copies in 45 days, or one bulk order (≥10 copies of one title within a week). Fail: <8 copies.
- First $: $8.99 paperback (~$2–3 royalty each), so one cast set brings in about $40–75; ~14–30 days.
- Flags: legal review. Check each play's first-publication year and edition: later acting editions and revisions can have their own copyright, and production year is not publication year. Market for US performances only, since most of these plays are still protected abroad. Use no text, cover art or stage directions from licensing-house editions.
- Unique: No accepted ideas yet. Nearest in this batch is I-009 (fake book), which differs in resource (play texts), buyer (theater groups buying cast sets) and the fee it replaces (per-performance royalties).
- Tags: customer=community/school theaters · mechanism=PD performance edition + rights memo · resource=PD plays (1925–1931)
- Score (1-5): speed 3 · early 4 · fit 2 · ceiling 3

### I-013 · Reprints of HathiTrust-cleared, never-renewed 1931–63 books
- Money now flows to: Hobbyists pay $40–150 for used copies of out-of-print mid-century US how-to books (woodworking, rug hooking, fly tying, decoy carving, small engines, regional gardening, chess) because nobody reprints them. Yet most of these books never had their copyright renewed, so they are already PD.
- Why now: HathiTrust's Copyright Review Program has checked hundreds of thousands of 1923–63 US books by hand and opened the unrenewed ones as public domain. Its rights data (Hathifiles, with reason codes such as no-renewal or no-notice) is a free bulk download. A Claude Code script can join that data to demand signals. AI cleanup of the OCR plus a new introduction and index makes a KDP edition that counts as differentiated, in days. Attention is on the 1931 wave; this larger pool is getting none.
- Edge: Data-joining skills. HathiTrust's reviewers have already done the rights check. Where scans are poor, physical library copies (SearchOhio/OhioLINK) fill the gaps.
- Silent test: Filter the Hathifiles to US books from 1931–63 marked PD for no renewal or no notice, in hobby and how-to subjects. Check by hand (no scraping) that no edition is in print and used copies sell for ≥$35. Publish the top 5 as KDP paperbacks at $14.99–19.99. Pass: ≥3 of the 5 titles sell ≥5 copies each within 30 days. Fail: <5 copies in total.
- First $: ~$16.99 paperback (~$4–6 royalty); ~21–30 days.
- Flags: legal review (light). Re-check each HathiTrust ruling for separately copyrighted photos or inserts and for later revised editions. Sell titles marked "pdus" (PD in the US only) in the US only. Keep the HathiTrust record and renewal-search notes in case KDP asks for proof of PD status.
- Unique: No accepted ideas yet. Nearest in this batch is I-010, which relies on the 95-year term. This relies on non-renewal under the 1909 Act, uses a different resource (HathiTrust rights data joined to demand signals) and needs no translation.
- Tags: customer=hobbyists/used-book buyers · mechanism=rights × demand data join → differentiated reprint · resource=HathiTrust no-renewal corpus (1931–63)
- Score (1-5): speed 3 · early 4 · fit 4 · ceiling 4

### I-014 · Trap Atlas: opening traps ranked by measured win rate
- Money now flows to: Club players buy chess trap books and courses (KDP paperbacks ~$12–20, Chessable trap courses ~$20–60). These list traps without any evidence of how often each one works at a given rating.
- Why now: Lichess releases every rated game (billions of them) and its puzzle set under CC0. With rating-band data, a laptop can measure for each of about 60 named traps how often opponents fall for it and how the trapper scores once the opponent finds the right defense, by rating band and time control. Nov–Dec is peak chess-gift season, and January brings players trying to improve.
- Edge: The existing chess game-analysis pipeline (python-chess + Stockfish) checks each line and labels the correct defenses. Coaching experience turns the numbers into advice like "play this below 1400, drop it above 1600". Re-running the data each year gives a new edition.
- Silent test: Publish on KDP ($7.99 ebook, $14.99 paperback with diagrams) and sell a $9 PGN file, ready to import as a Lichess study, on Gumroad. Pass: ≥25 combined sales in 45 days. Fail: <8.
- First $: $7.99–14.99; ~14–21 days.
- Flags: none. The data is CC0; credit Lichess as a courtesy but don't imply endorsement or use its logo.
- Unique: No accepted ideas yet. Nearest in this batch is I-013 (data join into a KDP book), which differs in resource (a CC0 game database, not PD texts), product (new statistics, not a reprint) and buyer (chess players).
- Tags: customer=club chess players · mechanism=open-data analytics → evidence-ranked guide · resource=Lichess CC0 database + chess pipeline
- Score (1-5): speed 4 · early 3 · fit 5 · ceiling 3

### I-015 · HABS/HAER drawings → prototype-accurate model railroad STLs
- Money now flows to: Model railroaders pay $40–120 for craftsman structure kits, which cover only a few dozen real buildings, or spend weeks building from photos. Shapeways' 2024 bankruptcy disrupted print-on-demand, and many modelers switched to home resin printers (~$200) and now buy STL files.
- Why now: Resin printing is cheap and AI speeds up 3D modeling. The Library of Congress HABS/HAER collection has PD measured drawings (plans, elevations, details) of thousands of depots, interlocking towers, freight houses, grain elevators, mills and covered bridges. These are exact dimensions that few kit makers use. Winter is peak layout-building season.
- Edge: Game-dev 3D modeling skills (Blender) turn the drawings into printable HO- and N-scale parts. Free slicer software checks wall thickness and supports. A library makerspace printer, if one is available, allows test prints at material cost.
- Silent test: Model 3 structures (e.g., an Ohio covered bridge, a small-town depot, an interlocking tower) in HO and N scale. List them on Cults3D and Etsy at $12–18. Pass: ≥20 sales in 45 days. Fail: <5.
- First $: ~$14 STL; ~21–35 days.
- Flags: Leave off railroad names, logos and heralds, since railroads charge licensing fees for their marks on models; sell unbranded. Confirm each HABS/HAER sheet carries a "no known restrictions" statement. Buildings from before 1990 have no architectural copyright.
- Unique: No accepted ideas yet. Nearest in this batch is I-016 (Sanborn kits), which differs in resource (HABS/HAER measured drawings), output (printable 3D models) and buyer (model railroaders).
- Tags: customer=model railroaders · mechanism=PD measured drawings → printable 3D kits · resource=LoC HABS/HAER (federal PD dataset)
- Score (1-5): speed 3 · early 3 · fit 4 · ceiling 3

### I-016 · Real-1920s town kits for Call of Cthulhu from Sanborn maps
- Money now flows to: Call of Cthulhu Keepers (game masters for the 1920s horror tabletop RPG) buy maps, handouts and town guides on DriveThruRPG for $3–15 each, or spend hours preparing period-accurate locations themselves.
- Why now: The Library of Congress hosts tens of thousands of PD Sanborn fire-insurance map sheets. They show 1900s–1920s towns block by block, with each building's use, material and height labelled. AI vectorizing and OCR of the labels turn a raw sheet into a clean game-master map, a player map and a building directory (livery, undertaker, opera house, ice house) in about a day.
- Edge: A game developer's eye for level design, plus Claude Code tooling. Chaosium's Miskatonic Repository lets anyone sell Call of Cthulhu–compatible material on DriveThruRPG by signing an online agreement, with no contact needed, and the section has its own browsing traffic.
- Silent test: Publish one town kit at $4.95 on the Miskatonic Repository, e.g., a Vermont town for running Lovecraft's 1931 "The Whisperer in Darkness", or an Ohio river town. Add a free (pay-what-you-want) sample map. Pass: ≥30 paid sales in 30 days. Fail: <8.
- First $: $4.95 kit (creator gets ~50%); ~7–14 days.
- Flags: Use only the Library of Congress's free online Sanborn sheets. The ProQuest Sanborn set in the Ohio Web Library is licensed and for research only. Keep handouts fictional: no real private individuals' names taken from period newspapers.
- Unique: No accepted ideas yet. Nearest in this batch is I-015, which differs in resource (Sanborn insurance maps, not HABS drawings), output (2D game-master and player maps plus a building directory) and buyer (tabletop RPG game masters).
- Tags: customer=TTRPG game masters · mechanism=PD map vectorizing + gazetteer packaging · resource=LoC Sanborn maps (PD)
- Score (1-5): speed 4 · early 3 · fit 4 · ceiling 2

### I-017 · 2027 Off-Patent Plant List
- Money now flows to: Small nurseries, Etsy/Facebook plant sellers and garden-club plant sales pay brand royalties or skip popular cultivars out of patent fear (or propagate patented ones by mistake); no one sells a clean "what legally came off patent this year" list.
- Why now: Plant patents run 20 years from filing with no maintenance fees, so 2007 filings expire through 2027; USPTO bulk data (PatentsView) is public, and AI can now map code names ('Bailmer') to trade names (Endless Summer) at scale; Jan–Mar is when growers start cuttings for summer sales.
- Edge: Propagation skill ranks each cultivar by ease-from-cuttings x retail demand; versioned-catalog method gives annual editions + changelog; AI text clustering does the name matching.
- Silent test: $24 PDF+CSV on Etsy and Gumroad, plus free static "Is <cultivar> still patented?" pages on GitHub Pages; pass ≥10 sales by Feb 28, 2027 or ≥1,000 organic lookups/month; kill <3 sales.
- First $: "2027 Off-Patent Plant List" (~400 cultivars, propagation notes, trademark warnings) $24; $9/yr for quarterly updates; ~25–45 days.
- Flags: legal review (patent/trademark status claims; brand trademarks outlive patents; not legal advice). Omit inventor names (individuals); list assignee companies only.
- Unique: No accepted ideas yet; nearest in batch I-021 sells planting timing to home gardeners, this sells legal-status data to commercial propagators.
- Tags: customer=small nurseries + plant resellers · mechanism=annual versioned data product · resource=USPTO plant patents + propagation skill + catalog method
- Score (1-5): speed 3 · early 5 · fit 4 · ceiling 3

### I-018 · Your Chess Year, Printed
- Money now flows to: Gift buyers spend $20–60 on generic chess merch (mugs, posters, boards); players get free but forgettable on-screen recaps; nobody prints a person's own games as a training keepsake.
- Why now: Holiday gift season with a ~Dec 10 print/ship cutoff; Chess.com PubAPI and Lichess API serve any public game archive; Lulu's print API means $0 upfront print-on-demand.
- Edge: The chess pipeline already pulls rapid games, runs Stockfish and builds catalog.json; the coach skill writes captions; game-dev skills render diagrams and layout.
- Silent test: Etsy personalized listing (username field) live by Nov 12; pass ≥8 orders by Dec 10; kill the print tier if <3 orders with ≥1,000 views by Dec 1 (keep PDF tier).
- First $: 96-page 6x9 paperback (rating arc, opening tree, 10 best moves, 50 "puzzles you missed" from own games, QR to each original game) $44 + shipping, Lulu prints/ships for ~$12; $14 PDF tier; ~20–35 days.
- Flags: Privacy: buyer-supplied public username of an adult account only; delete data after delivery. Orchestrator: a gift processes the recipient's games, so require their consent or limit to the buyer's own account. Disclose Lulu as Etsy production partner; use platform names only nominatively.
- Unique: Nearest in batch I-020 is a diagnostic service for improvers; this is a seasonal physical keepsake sold to gift buyers on a gift marketplace.
- Tags: customer=gift buyers for chess players · mechanism=personalized print-on-demand keepsake · resource=chess pipeline + public chess APIs + Lulu
- Score (1-5): speed 4 · early 4 · fit 5 · ceiling 3

### I-019 · Custom GPT → Agent Skill Port
- Money now flows to: Small businesses and consultants paid Fiverr/Upwork freelancers $50–500 per Custom GPT or Claude Project; those builds sit locked in one vendor's app, untested, and drift silently when models change.
- Why now: Agent Skills (SKILL.md folders) became an open, cross-tool format in late 2025; teams adopting Claude Cowork/Claude Code want their GPTs moved and tested; few Fiverr gigs target "GPT to Skill" search terms yet.
- Edge: Existing agent-instruction builder + skill-writing practice + eval method (test prompts with expected outputs); pure writing/testing work, no calls.
- Silent test: Fiverr gig with requirements form (paste GPT instructions, upload knowledge files, "no calls" stated); pass ≥3 orders in 30 days; kill if 0 orders after ≥500 impressions.
- First $: $79 per port (1 GPT, ≤5 knowledge files, 5 eval cases, install guide); $149 packaged as a Cowork plugin; ~10–25 days.
- Flags: Client files may be confidential: accept no credentials, delete after delivery. Otherwise none.
- Unique: Nearest in batch I-022 uses agent personas to critique a document; this sells portable, tested instructions to businesses.
- Tags: customer=small businesses with Custom GPTs · mechanism=migration + packaging service · resource=agent-instruction builder + eval method
- Score (1-5): speed 4 · early 4 · fit 5 · ceiling 3

### I-020 · 100-Game Leak Audit
- Money now flows to: Adult improvers pay coaches $30–80/hr, much of it for slow game-by-game review, or pay premium memberships whose reviews go one game at a time and don't give a ranked plan.
- Why now: Stockfish + LLM narration turn a 100-game audit into a ~15-minute compute job; January "break my plateau" resolutions peak in 6–9 weeks.
- Edge: The chess pipeline and coach skill already do this for the owner; Bayesian A/B method estimates rating points lost per leak (e.g., time-trouble conversions vs opening deficits).
- Silent test: Fiverr gig, adults only (requirements: username, platform, time control); pass ≥3 orders in 30 days or ≥2% impression→order; kill if 0 orders after ≥500 impressions.
- First $: PDF with top 3 leaks and their rating-point cost, 3 example positions each, 20 drills from own games, opening ROI table, $29; $59 with a 30-day re-audit; ~10–21 days.
- Flags: Adult accounts only (avoids kids review); buyer-supplied username; delete data after delivery.
- Unique: Nearest in batch I-018 is a once-a-year gift keepsake; this is a repeatable coaching diagnostic for improvers with a re-audit upsell.
- Tags: customer=adult chess improvers · mechanism=engine-backed diagnostic service · resource=chess pipeline + coach skill + Bayesian method
- Score (1-5): speed 5 · early 2 · fit 5 · ceiling 2

### I-021 · ZIP-Exact 2027 Garden + Propagation Calendar
- Money now flows to: Gardeners buy generic $5–15 printable planners on Etsy and seed-company zone charts; zones measure winter lows, not frost dates, so starts get mistimed, and propagation windows are rarely included.
- Why now: NOAA 1991–2020 Climate Normals publish per-station freeze-date probabilities (public domain), so a per-ZIP calendar generates in seconds; demand peaks with Christmas gardener gifts and Jan–Mar seed-starting; a "2027" edition is naturally dated.
- Edge: Existing garden planning catalog supplies crop timing rules; propagation skill adds hardwood/softwood/division windows; Google Calendar know-how for an .ics reminder file.
- Silent test: Etsy personalized digital listing (ZIP + crop picks) live by Nov 15; pass ≥15 orders by Jan 31; kill <5.
- First $: Personalized PDF (week-by-week sow, transplant and cutting dates, 10/50/90% frost-risk dates) + .ics reminders, $12, delivered by Etsy file message within 24h; ~15–30 days.
- Flags: none.
- Unique: Nearest in batch I-017 sells patent-status data to commercial propagators; this sells personalized timing to home gardeners.
- Tags: customer=home gardeners + gardener-gift buyers · mechanism=personalized generated calendar · resource=garden catalog + NOAA normals + propagation skill
- Score (1-5): speed 4 · early 3 · fit 4 · ceiling 3

### I-022 · Blind-Playtest Rulebook Audit
- Money now flows to: Indie tabletop designers pay freelance rulebook editors (~$300–1,000 per book) and spend weeks recruiting blind playtesters, and still launch crowdfunding with ambiguous rules that breed FAQs and errata.
- Why now: Long-context LLM agents can now play rule-literal novices, rules lawyers and edge-case hunters against a rulebook in hours, logging every point where play stalls, which used to take human blind-test rounds.
- Edge: Game-design skill + agent-instruction builder (reusable persona suite); chess-trained rules precision; local AI models offered so unreleased designs never leave the machine.
- Silent test: Fiverr gig with a sample audit of a CC-licensed print-and-play rulebook as portfolio; pass ≥2 orders in 30 days; kill if 0 orders after ≥400 impressions.
- First $: Ranked ambiguity/contradiction report with page refs and suggested rewrites, $49 (≤12 pages) / $129 (≤40 pages); ~20–35 days.
- Flags: Confidential designs: no-training, delete-after policy; disclose AI use in the gig. Otherwise none.
- Unique: Nearest in batch I-019 writes instructions for businesses; this sells a critique deliverable to game designers, using agents as simulated players.
- Tags: customer=indie tabletop designers · mechanism=AI persona audit service · resource=game-design skill + agent-instruction builder + local models
- Score (1-5): speed 3 · early 4 · fit 3 · ceiling 3

### I-023 · Etsy Seller Year-End Books Kit
- Money now flows to: Etsy sellers pay bookkeepers for catch-up work (often $300+), pay $20–50/mo maker-accounting apps, or buy static spreadsheets that make them hand-key every order and fee line each tax season.
- Why now: Tax season (Jan–Apr); Etsy lets sellers download Payments and Sold Orders CSVs, and AI cheaply categorizes leftover bank lines; most competing Etsy templates still rely on manual entry.
- Edge: The budgeting app's import + categorization rules, repurposed into Google Sheets + Apps Script and sold where the buyers already are (Etsy).
- Silent test: Etsy digital listing live by Dec 15; pass ≥12 sales by Feb 15; kill <4.
- First $: Sheet that imports Etsy CSVs + one bank CSV and outputs a fee breakdown, net profit, expense totals by Schedule C line, and a "questions for your preparer" list, $19; ~20–45 days.
- Flags: legal review (tax/finance): bookkeeping organizer only, no tax advice, clear disclaimer.
- Unique: No accepted ideas yet; the only budgeting-app idea in this batch, distinct by customer (Etsy sellers) and mechanism (self-serve tool run on the buyer's own records).
- Tags: customer=Etsy sellers · mechanism=spreadsheet tool with CSV import · resource=budgeting app categorizer + Etsy exports
- Score (1-5): speed 4 · early 2 · fit 3 · ceiling 3

### I-024 · Chess Club in a Box for Non-Chess Teachers
- Money now flows to: Schools pay outside chess-enrichment vendors per student per semester, or an assigned teacher who barely knows the moves stitches together YouTube videos; most TpT chess listings are single worksheets, not run-ready club sessions.
- Why now: The Lichess puzzle database (CC0, millions of rated, theme-tagged puzzles) + AI drafting make a graded, original curriculum a 2–3 week build; clubs restart in January.
- Edge: Chess-coach skill for sequencing; game-dev skill for an offline HTML projector board (no login, no data collection).
- Silent test: TpT listing + free Session 1 sample; pass ≥10 paid sales by Feb 28, 2027 (leading signal: ≥50 sample downloads by Jan 15); kill <3 paid.
- First $: 12 sessions (slides + teacher script), 300 graded printable puzzles, projector board and mini-tournament kit, $19 on TpT (free Basic account keeps ~55%); ~25–45 days.
- Flags: legal review (kids): sold to adults, content only, no student data collected or stored.
- Unique: Nearest in batch I-020 sells analysis to individual adults; this sells a curriculum to teachers, built from CC0 puzzles rather than the buyer's games.
- Tags: customer=K-12 teachers running chess clubs · mechanism=curriculum digital download · resource=chess-coach skill + Lichess CC0 puzzles + game dev
- Score (1-5): speed 3 · early 2 · fit 4 · ceiling 2

**Round 2** (L5 moat · L6 AI shovels)

### I-025 · Public-domain status evidence API for dataset builders
- Money now flows to: AI dataset builders, PD reprint publishers and digital archives pay the Copyright Office's $200/hr records-search fee or rights-clearance firms per title, or check renewal volumes by hand. Most simply drop every post-1930 book. After the $1.5B Bartz v. Anthropic book settlement (2025, ~$3,000 per work), "provably public domain" became a budget line for anyone building a training corpus.
- Why now: Registration records (NYPL's Catalog of Copyright Entries transcriptions), renewal records (Stanford Copyright Renewal Database) and HathiTrust's Hathifiles are free bulk data. LLM-assisted fuzzy matching now joins any title list against them for about a cent per title and logs the evidence. PD-only corpora (Harvard's Institutional Books, EleutherAI's Common Pile, both 2025) show the demand. On Jan 1, 2027 the US cutoff moves to 1931, so every existing PD list goes stale overnight.
- Edge: Data-joining plus the versioned-catalog habit: each determination is dated and shows the queries run and the nearest non-matches. One determination can be sold to every buyer who asks about that title. Channels with no contact: a free sample on the Hugging Face Hub (where dataset builders search) and paid lookups as an Apify Store Actor (pay per result, also callable by AI agents through Apify's MCP server).
- Silent test: Publish 20,000 determinations for 1929–63 US books (title, year, status, reason code, evidence links) as a free Hugging Face dataset, and list the Actor at $0.03 per title. Pass: ≥300 dataset downloads and ≥$150 Actor revenue within 45 days. Fail: <75 downloads, or $0 revenue after 60 days.
- First $: $0.03 per lookup, $9 single-title evidence PDF (e.g., to answer a KDP public-domain query), $1,500 per 100k-title bulk run; ~21–35 days.
- Flags: legal review. Sell evidence summaries with confidence levels, never legal opinions or warranties. Foreign works restored under URAA don't depend on renewal, so mark them "renewal test not applicable." Publish bibliographic metadata only, never text. Confirm reuse terms for each source dataset.
- Unique: Closest is I-013, which uses HathiTrust's existing rulings to pick books to reprint. This sells the rights determination itself, extends it to titles HathiTrust never reviewed by matching registration and renewal records, and reaches dataset builders and agents through data/API marketplaces.
- Tags: customer=AI dataset builders + PD publishers · mechanism=rights-evidence lookups sold per call and in bulk · resource=NYPL CCE + Stanford renewals + Hathifiles
- Score (1-5): speed 3 · early 4 · fit 4 · ceiling 4

### I-026 · GPL-free, human-calibrated chess AI kit for game developers
- Money now flows to: Indie devs adding chess or chess-like modes buy $20–60 asset-store chess kits whose "easy" levels hang random pieces, or spend weeks writing their own minimax. They can't embed the strong engines in closed-source, console or App Store builds, because Stockfish, Fairy-Stockfish (the main variant engine) and Lc0 are all GPLv3.
- Why now: Lichess's CC0 database (billions of rated games) shows how players at each rating actually go wrong: which pieces they hang, in which phase, under how much clock pressure. A small permissive engine can now be tuned to play like a real 800, 1200 or 1600 player rather than a crippled engine. Chess-like roguelikes (Shotgun King, Pawnbarian and their followers) created demand for custom pieces and boards. AI-assisted coding makes a compact engine with C# and GDScript bindings a few weeks' work.
- Edge: The chess pipeline (python-chess + Stockfish) measures error rates by rating band and checks the calibration. Game-dev skill packages the engine for Unity and Godot. Sold where developers already search and buy without contact: itch.io, Fab and the Unity Asset Store.
- Silent test: Pre-check: asset-store searches show no permissive engine with rating-calibrated, human-like levels (otherwise stop). List a $29 kit on itch.io and Fab (live at once) and on the Unity Asset Store (1–3 week review), with a free WebGL "beat the 1200 bot" demo. Pass: ≥10 paid in 45 days, or ≥2% demo-to-purchase. Fail: <3 paid with ≥500 demo plays.
- First $: $29 kit (standard chess, human-like levels); $59 pro (fairy pieces, custom boards, hint/explain API); ~25–40 days.
- Flags: The engine is written from scratch, with no GPL code or weights. Lichess data is CC0; no usernames appear in any output. Otherwise none.
- Unique: Closest is I-014, which turns Lichess CC0 statistics into a trap guide for players. This sells licensable software to game developers and exploits a constraint no listed idea uses: GPL engines can't ship inside closed-source games.
- Tags: customer=indie game developers · mechanism=permissively licensed SDK sold in asset stores · resource=Lichess CC0 + chess pipeline + game-dev skill
- Score (1-5): speed 3 · early 3 · fit 5 · ceiling 2

### I-027 · Plant-shipping law checker (Shopify app)
- Money now flows to: Online nurseries and houseplant shops refund or reship parcels that state quarantines stop: citrus into CA/AZ/TX/FL, Japanese-beetle host plants into western states, soil-grown plants into Hawaii. Some unknowingly sell banned invasives (e.g., Ohio has banned Callery pear sales since 2023). Others pay staff to hand-key rules from 50 state PDFs, or pay $5–20/mo for generic shipping-rule apps that know nothing about plant law.
- Why now: The National Plant Board's state-by-state law summaries and USDA APHIS Federal Orders are public but written as dense prose. An LLM can now turn them into a dated rules table (genus/species × state × condition) and diff it monthly. Shopify's checkout-validation Functions can block a restricted cart-and-address combination before payment. Spring shipping season opens in Feb–Mar.
- Edge: Gardening and propagation knowledge maps cultivars to the regulated genera and pest hosts. The versioned-catalog method gives every rule a source, a "last verified" date and a changelog. Sold in the Shopify App Store, where merchants search and install with no contact; Shopify takes 0% of a developer's first $1M.
- Silent test: Pre-check: App Store search for "plant shipping restrictions" returns no plant-law-specific app (otherwise stop). Launch a free plan (25 products) and a $12/mo plan (full catalog, checkout blocking, monthly rule-change email), plus a free public "Can I ship [genus] to [state]?" lookup. Pass: ≥40 installs and ≥5 paid within 60 days of approval. Fail: <10 installs.
- First $: $12/mo after a 14-day trial; ~45–60 days (2–3 weeks to build, 1–2 weeks of review).
- Flags: Advisory only: cite each source. It doesn't replace phytosanitary certificates or nursery licenses, and the merchant stays responsible. Small one-time Shopify developer registration fee (~$19).
- Unique: Closest is I-017 (off-patent plant data for nurseries). This turns state quarantine and invasive-species law into a rules engine that acts at checkout. It differs in resource (plant-protection law, not patents) and mechanism (enforcement at the point of sale).
- Tags: customer=online nurseries + plant shops · mechanism=checkout-embedded compliance app · resource=National Plant Board summaries + APHIS orders + gardening skill + catalog method
- Score (1-5): speed 3 · early 4 · fit 4 · ceiling 3

### I-028 · Blindfold Tactics: spoken chess puzzles for commuters
- Money now flows to: Adult improvers pay $20–100 per Chessable course and $10–25 per tactics book. All of it needs a screen or a diagram, so commute, gym and dog-walk time goes unused, even though coaches prescribe visualization (blindfold) training. Chess shelves in audiobook stores hold biographies and narrated beginner books that only make sense with a board in front of you.
- Why now: The Lichess puzzle database (CC0, ~5M rated, theme-tagged puzzles) can be filtered to positions with ≤7 pieces and one clear solution, which a listener can hold in their head. Free local TTS models or Google Play Books' free auto-narration bring a 4-hour volume's production cost to about $0. Spotify has accepted AI-narrated audiobooks via ElevenLabs since 2025. Improvement plans start in January.
- Edge: Coach skill to grade difficulty, write spoken hints and set each pause as thinking time. The chess pipeline (Stockfish) verifies every solution is unique. Audio is a store category that diagram-bound competitors can't enter, and buyers reach it by searching "chess" in audiobook stores and podcast apps.
- Silent test: Pre-check: <5 audio-native chess drill titles show up in Google Play and Spotify audiobook search. Publish Vol. 1 (300 puzzles rated 1200–1600, ~4 hrs) at $9.99 on Google Play Books and Spotify, with a free 10-puzzle podcast feed as the sampler. Pass: ≥25 paid units in 45 days. Fail: <8.
- First $: $9.99 audiobook, followed by Vol. 2 (1600–2000) and an endgame volume; ~14–30 days.
- Flags: Disclose AI narration wherever platforms require it; no Lichess branding. Otherwise none.
- Unique: Closest is I-024 (CC0 puzzles turned into a teacher curriculum). This is a product built for listening, sold to adult improvers in audiobook and podcast stores, a channel that the book (I-014) and curriculum (I-024) formats can't serve.
- Tags: customer=adult chess improvers · mechanism=audio-native training product · resource=Lichess CC0 puzzles + local TTS + coach skill
- Score (1-5): speed 4 · early 4 · fit 5 · ceiling 2

### I-029 · On-device AI redaction app for the Mac
- Money now flows to: HR staff, school and township records clerks and small professional offices redact by hand in Acrobat Pro (~$20–30/mo per seat). Others pay per-page redaction vendors or cloud AI redaction tools that their own policies forbid them to upload records to. Public-records and document-request volumes keep rising.
- Why now: Apple's Foundation Models framework (macOS 26, fall 2025) gives every Mac app a free on-device LLM, and Vision OCR runs locally too. Detecting names, SSNs, account numbers and addresses in scanned PDFs now costs $0 per page and nothing leaves the machine, which is the one claim cloud tools can't make.
- Edge: The brief's local-AI experience; agent-instruction writing for reusable "redaction profiles" (e.g., an Ohio public-records preset for SSNs and account numbers); Claude Code for Swift. Sold through the Mac App Store, where buyers search "redact" and buy without contact.
- Silent test: Pre-check: no on-device AI auto-detect redaction app in the Mac App Store has >100 ratings. List it free for 5 pages per document, with a $29.99 one-time unlock. Pass: ≥30 paid unlocks within 45 days of approval. Fail: <8 paid with ≥2,000 product-page views.
- First $: $29.99 one-time (batch-folder Pro $59); ~25–40 days.
- Flags: The Apple Developer Program costs $99/yr, an exception to the ~$0 budget. The app must strip text layers and metadata, not just draw boxes, require human review before export, and promise no completeness guarantee. Any preset that names HIPAA or FERPA needs legal review. Runs only on Apple-silicon Macs with Apple Intelligence.
- Unique: Closest is I-008, which uses local models as a privacy edge when bidding on transcription work. This is a self-serve desktop app sold in an app store, for redaction, built on Apple's free on-device model, with no service delivery.
- Tags: customer=privacy-bound office staff (HR, records clerks, small firms) · mechanism=on-device AI utility sold in an app store · resource=Apple Foundation Models + local AI + Claude Code
- Score (1-5): speed 3 · early 3 · fit 3 · ceiling 3

### I-030 · Federal Register → Jira rule-change tickets
- Money now flows to: Compliance and operations leads at small regulated firms (food plants, motor carriers, chemical distributors, drone operators, alcohol producers) pay regulatory-intelligence services ($10k+/yr) or rely on law-firm client alerts. Otherwise a staffer reads the Federal Register every morning and keeps a spreadsheet of effective dates.
- Why now: The Federal Register and Regulations.gov APIs are free and filter by CFR part. An LLM can now summarize each document, score "does this affect us?" against a company profile, and pull out effective and comment dates for pennies. Rule churn is unusually high: 2025's 10-for-1 deregulation order (EO 14192), mass rescissions and the FAR overhaul keep moving dates.
- Edge: The versioned-catalog habit (a dated changelog per tracked CFR part) and AI text clustering to group related documents. Free FederalRegister.gov email alerts only notify; this triages and creates the work items. Atlassian handles trials, billing and licensing, so selling stays contact-free.
- Silent test: Pre-check: Atlassian Marketplace search for "Federal Register" returns ≤3 apps (otherwise stop). List a Forge app: pick CFR parts and get one Jira issue per relevant document (summary, applicability score, dates as subtasks), with a 30-day trial. Pass: ≥25 trial installs and ≥3 paid conversions within 75 days of listing. Fail: <8 installs.
- First $: ~$15–50/mo per site, tiered by user count; ~60–80 days (build, Marketplace approval, then the 30-day trial).
- Flags: Information only, not legal advice; link every summary to the official document. Leave flagged domains (health, finance) out at launch, or put them through legal review first.
- Unique: Closest is I-005 (a versioned requirements catalog for contractors). This watches federal rulemaking by CFR part and delivers it as tickets inside the buyer's work tracker, sold through an integration marketplace. It differs in resource (Federal Register API), mechanism (workflow-embedded alerts) and buyer.
- Tags: customer=small regulated-business compliance leads · mechanism=workflow-embedded alert app · resource=Federal Register + Regulations.gov APIs + catalog method
- Score (1-5): speed 2 · early 3 · fit 3 · ceiling 4

### I-031 · Cited needs-statement data add-on for Google Docs
- Money now flows to: Small nonprofits and freelance grant writers ($50–100/hr) spend 2–4 hours per application pulling poverty, income, unemployment and housing figures from data.census.gov for the statement of need, or pay for data-mapping subscriptions. AI grant-writing tools now draft these sections with plausible but unsourced numbers, which reviewers catch.
- Why now: The Census API (ACS, SAIPE) and BLS LAUS are free. An add-on can insert a sourced table and a draft paragraph for any county, place, tract or school district in seconds, with every number tied to a table ID and vintage. The ACS 2021–2025 5-year release (scheduled for December 2026) makes every boilerplate's figures stale just before spring grant deadlines.
- Edge: Public-data skill, plus agent-instruction writing for a citation-strict drafting spec (no number without a table ID and margin of error). Listed in the Google Workspace Marketplace, where nonprofits on free Google Workspace for Nonprofits find add-ons, with Word's AppSource as a second listing.
- Silent test: Free tier (3 inserts/month) and a $12/mo or $79/yr unlock via a Stripe link. Pass: ≥150 installs and ≥8 paid within 60 days of Marketplace approval. Fail: <40 installs.
- First $: $79/yr; ~30–50 days (build, then Marketplace and OAuth review).
- Flags: Show ACS margins of error and never present estimates as exact counts. Request access to the current document only. No health-outcome data at launch. Otherwise none.
- Unique: Closest is I-002 (compliance matrices for grant applicants). This supplies the proposal's data section, not its requirements, and differs in resource (Census/BLS APIs), mechanism (a cited-data insert tool inside the editor) and channel (an add-on marketplace).
- Tags: customer=small nonprofits + freelance grant writers · mechanism=in-editor cited-data add-on · resource=Census ACS/SAIPE + BLS APIs
- Score (1-5): speed 3 · early 3 · fit 3 · ceiling 3

### I-032 · Title II-ready township & village website theme
- Money now flows to: Small townships, villages, library boards and special districts pay gov-web platforms (CivicPlus/Granicus-class, ~$3k–15k setup plus annual fees) or local designers ($2k–10k) to rebuild sites. Some bought accessibility overlays, which the FTC's $1M accessiBe order (2025) discredited.
- Why now: DOJ's Title II rule requires WCAG 2.1 AA by Apr 26, 2027 for entities under 50k population and all special districts, so rebuild decisions land in Jan–Mar budget meetings. Claude Code plus automated axe-core testing makes a fully tested accessible theme a ~3-week build. It would include a meeting archive (agenda, minutes, video), public notices, a records-request page and accessible-PDF guidance.
- Edge: Local knowledge of what Ohio township sites need (trustees, fiscal officer, zoning, roads, cemeteries, Sunshine Law notices), plus the catalog habit for a clean meeting-archive data model. Sold where clerks' web designers already shop (ThemeForest's WordPress section), with a free WordPress.org version and a pro upsell. A footer credit shows it to neighboring clerks.
- Silent test: Free lite theme on WordPress.org plus a $59 pro version on ThemeForest. Pass: ≥10 ThemeForest sales, or ≥150 WordPress.org active installs and ≥5 pro upgrades, within 60 days of approval. Fail: <3 sales.
- First $: $59 pro license, or $149 with a starter-content pack; ~35–60 days (ThemeForest review takes 1–3 weeks, with a real chance of rejection).
- Flags: Say "built and tested to WCAG 2.1 AA," never "ADA compliant," since content added later can break conformance. Confirm DOJ hasn't moved the date (same check as I-001).
- Unique: Closest is I-001 (Title II minutes and agendas for small Ohio bodies). This sells a one-time site template nationally through theme marketplaces, not a per-meeting document subscription. It differs in mechanism (template product) and resource (WordPress/ThemeForest + axe-core).
- Tags: customer=small local governments + their web designers · mechanism=accessible site template sold in theme marketplaces · resource=WordPress/ThemeForest + axe-core + Claude Code
- Score (1-5): speed 2 · early 3 · fit 3 · ceiling 3

### I-033 · Photo-to-placard lockout/tagout procedures for small plants
- Money now flows to: Small manufacturers and machine shops pay safety consultants and LOTO-service vendors about $100–300 per machine. The money buys the machine-specific energy-control procedures that OSHA requires under 29 CFR 1910.147(c)(4). Shops that don't pay post one generic procedure and get cited. Lockout/tagout is in OSHA's top-10 most-cited standards every year, and a serious violation can cost up to about $16.5k (2025 maximum).
- Why now: In the Economic Index, conversations matched to production tasks are well under 1% of usage, and so are installation/maintenance/repair tasks. Together these occupations hold about a tenth of US jobs. The people who own this paperwork are not using AI to write it. Vision models can now read nameplates and mark disconnects, valves and stored-energy points on phone photos. Claude then fills a fixed template: shut down, isolate, lock, release stored energy, verify.
- Edge: Game-dev layout skills make the placards consistent and easy to read. Agent-instruction writing fixes the procedure spec and the QA checklist. A versioned catalog holds energy-source templates by machine type (press brake, CNC lathe, injection molder, compressor, conveyor, saw). Butler County's many small plants (Hamilton, Fairfield, West Chester, Middletown) are the first market for search pages.
- Silent test: Pre-check: ≥15 SW Ohio Indeed postings from the last 90 days list writing LOTO procedures among EHS or maintenance duties. Then publish 25 pages titled "Lockout/tagout procedure for a [machine]: sample placard". Add an Etsy personalized listing and a Fiverr gig where the buyer uploads 4–8 machine-only photos and fills in a form. Pass: ≥4 paid machines, or one order of ≥10 machines, within 45 days. Fail: 0 paid after ≥400 combined visits and impressions.
- First $: $39 per machine, or $290 for a 10-pack. Each order gets a one-page color placard (PDF + editable DOCX) with numbered photo callouts, plus an equipment list and an annual periodic-inspection checklist, within 48h; ~20–40 days.
- Flags: Safety-critical. Deliver each placard as a draft that the employer's authorized employee must check on the machine, and require a checkbox confirming it. Never claim "OSHA compliant". Get legal review of the liability terms, and consider E&O insurance before scaling. Accept machine-only photos, with no faces.
- Unique: Nearest is I-006, which checks a buyer's own label artwork against rules. This writes a new safety procedure from the buyer's machine photos, under a different rule (OSHA 1910.147), for a different buyer (plant and maintenance managers).
- Tags: customer=small manufacturers/maintenance managers · mechanism=photo-to-compliance-document per-unit service · resource=vision AI + OSHA 1910.147 + Index/Indeed occupation gap
- Score (1-5): speed 3 · early 4 · fit 3 · ceiling 4

### I-034 · Forklift-battery Tier II packets (the hidden sulfuric-acid trigger)
- Money now flows to: Warehouses, distribution centers (DCs) and plants with electric forklift fleets pay EHS consultants about $300–1,500 per facility for the EPCRA §312 Tier II chemical inventory due every March 1, or never file it. Most don't know that sulfuric acid in lead-acid forklift batteries is an Extremely Hazardous Substance with a 500-lb reporting threshold. An industrial battery holds roughly 100–300 lb of acid, so a handful of batteries crosses that threshold, counting spares. About 8 or more batteries also cross the 10,000-lb threshold for lead. EPCRA penalties can reach five figures per day.
- Why now: Transportation/material-moving and production tasks barely show up in the Economic Index, so operations managers are not using AI to read safety data sheets (SDSs). Vision models now reliably pull CAS numbers, weight percentages and GHS hazard classes from battery, propane and fuel SDS PDFs. What remains is arithmetic. The filing window runs Jan 1 to Mar 1, 2027. The I-75 corridor through Butler County (West Chester, Monroe, Fairfield) is full of exactly these buildings.
- Edge: Calculator and spreadsheet skills from the budgeting app. A versioned catalog of battery models (weight, electrolyte %, acid %) built from public manufacturer SDSs. Monitoring of the Federal Register and EPA guidance. Local logistics geography for the first search pages.
- Silent test: By Dec 15, publish a free "Do your forklift batteries trigger Tier II?" calculator. The user enters battery count plus model or weight and sees pounds of sulfuric acid and lead against the thresholds. A $99 filing packet is the upsell. Pass: ≥150 calculator runs and ≥5 paid packets by Mar 1, 2027. Fail: <2 paid with ≥150 runs (no willingness to pay), or <40 runs (channel dead).
- First $: $99 for the first facility, $49 for each additional one. The packet holds a threshold worksheet with SDS citations; Tier II chemical entries (CAS numbers, hazard categories, amount range codes, storage types and locations) ready to type into EPA's Tier2 Submit or the state portal; and a state checklist (Ohio portal and fees). ~30–60 days.
- Flags: Light legal review. Sell it as a compliance aid, not legal advice; the facility owner certifies the filing. Verify EPA's current guidance on batteries and each state's portal and fees. Use public SDSs only.
- Unique: Nearest is I-004, an alert subscription for Ohio commercial and industrial facilities. This is a one-time threshold check and filing packet tied to a yearly deadline, under a different law (EPCRA §312). It is built by extracting data from SDSs and sold to warehouse operators.
- Tags: customer=warehouse/DC & plant operators · mechanism=free threshold calculator → paid filing packet · resource=EPCRA §312 + manufacturer SDSs + vision extraction
- Score (1-5): speed 3 · early 4 · fit 3 · ceiling 3

### I-035 · WH-347 builder with wage-determination check for first-time public-works subs
- Money now flows to: Small subcontractors (concrete, electrical, paving, sewer) on federally funded and Ohio prevailing-wage jobs pay for certified payroll. They buy add-ons from payroll providers or use specialty services, often about $25–75 per weekly report. The alternative is 2–4 office hours per job per week on Form WH-347. A wrong classification or fringe rate means withheld payments and back-wage findings.
- Why now: IIJA money keeps pulling small local firms onto their first Davis-Bacon jobs (roads, water, sewer) through 2027. DOL's 2023 Davis-Bacon rule, the first major overhaul in about 40 years, tightened the rules on classification and withholding. Construction & extraction tasks are among the least represented in the Economic Index, so these offices are not building their own automations. Claude can now read the wage-determination (WD) text on SAM.gov and pre-map thousands of job titles to WD classifications, which is the step that takes the most office time.
- Edge: The budgeting app's CSV import and mapping logic, rebuilt in Google Sheets + Apps Script. It runs in the buyer's own Drive, so no worker data ever reaches us. A title-to-classification synonym table built with AI-tagged clustering ships with the sheet, so it needs no AI calls at runtime. Ohio prevailing-wage rate tables are a second mode.
- Silent test: Etsy and Gumroad listings, plus a free "is this rate compliant?" page, targeting "WH-347 excel," "certified payroll template" and "Davis-Bacon rate check". Pass: ≥8 sales in 45 days. Fail: <3.
- First $: $49/yr per company. The buyer imports a payroll CSV (QuickBooks, Gusto or ADP export) and confirms the suggested classifications. The sheet checks base pay, fringe and overtime against the pasted WD, then outputs a print-ready weekly WH-347 and Statement of Compliance; ~15–30 days.
- Flags: legal review (wage-and-hour law). The sheet organizes and checks only; the contractor signs and certifies. Verify that it matches the current WH-347 version and Ohio's prevailing-wage thresholds.
- Unique: Nearest is I-023, a budgeting-app spreadsheet for Etsy sellers' year-end books. This checks payroll against federal and state wage determinations and produces a mandated weekly federal form for public-works subcontractors. It uses a different resource (SAM.gov WDs) and exploits a different constraint (Davis-Bacon and Ohio prevailing wage).
- Tags: customer=small public-works subcontractors · mechanism=self-run compliance spreadsheet (rate check + mandated form) · resource=SAM.gov wage determinations + budgeting-app importer + AI-built classification table
- Score (1-5): speed 4 · early 3 · fit 4 · ceiling 3

### I-036 · First-edition 2027 water-quality reports (CCRs) for small water systems
- Money now flows to: About 50,000 US community water systems must deliver a Consumer Confidence Report (CCR) by July 1 each year. Most serve fewer than 3,300 people: villages, mobile-home parks, HOAs, rural schools. Small systems pay engineering or consulting firms about $500–2,500 per report, or a part-time licensed operator puts it together from state templates.
- Why now: EPA's 2024 CCR Rule Revisions take effect Jan 1, 2027, so reports due July 1, 2027 are the first that must include the new elements:
  - a plain-language summary at the top;
  - narratives on corrective actions for violations;
  - how to access the lead service line inventory;
  - translation, or translation assistance, where ≥10% or ≥1,000 residents share a language and have limited English.
  Systems serving ≥10,000 people also move to two reports a year. Drafting and translation are cheap for AI now, while water-operator tasks barely show up in the Economic Index.
- Edge: Each system's monitoring results and violations are public in state SDWIS portals (Ohio EPA's Drinking Water Watch), so a draft needs no client data. Census ACS language tables decide whether translation is required. A Claude Code pipeline inserts the fixed regulatory health-effects wording. Federal Register monitoring catches rule changes. Village buyers overlap with I-001, which allows cross-selling.
- Silent test: Publish a "What changes in your 2027 CCR" page and a free translation-trigger checker (enter a place, see ACS limited-English shares against the 10%/1,000 test). Add a $149 order form for a draft built from the system's public data. Pass: ≥60 checker uses and ≥3 paid orders by Apr 30, 2027. Fail: 0 paid after ≥300 visits.
- First $: $149 per draft CCR (English plus required translations, as a print-ready PDF and accessible HTML). Systems serving ≥10k can add the second yearly report for $99. ~90–150 days, since buying peaks Mar–Jun.
- Flags: Light legal review. The owner or operator reviews the report and certifies it to the state. Verify the state-adopted version of the rule and any EPA delay. Pay a native-speaker reviewer to check translations before the first sale (small cost). Pull each system's public data only when it orders, with no bulk scraping.
- Unique: Nearest is I-001, minutes and accessible PDFs for small public bodies. This drafts a different mandated document (40 CFR 141 Subpart O) from public monitoring data and ACS language data. Its buyers also include private systems (parks, HOAs, schools).
- Tags: customer=small community water systems & contract operators · mechanism=public-data-built regulatory report + AI translation · resource=SDWIS monitoring data + ACS language data + 2024 CCR revisions
- Score (1-5): speed 2 · early 4 · fit 3 · ceiling 3

### I-037 · TechCred-reimbursed "Applied AI for Plant Technicians" credential
- Money now flows to: Ohio's TechCred program reimburses employers up to $2,000 per credential, and up to $30,000 per round, for short tech credentials. The employer pays the provider up front and the state reimburses it when the employee finishes. Most of this money goes to colleges and national vendors for IT, CNC, PLC, Six Sigma and generic office-AI courses. Almost none of it buys AI training built for plant-floor roles.
- Why now: On the Economic Index state map, Ohio's per-capita Claude usage is below the US average, and production, maintenance and logistics tasks barely show up. The gap is both regional and occupational, and the state already pays to close tech-skill gaps. With Claude, building a course for one role, with practical assessments, takes 3–4 weeks.
- Edge: Ohio location: only Ohio employers can claim TechCred. Agent-instruction writing becomes the curriculum: turning a manual into a PM checklist, writing work instructions, analyzing downtime logs. Lynda.com, through the Lane card, is used to benchmark competing AI courses. Game-dev skills build scenario-based assessments. A module on decisions AI must not make (lockout, energy isolation) sets the course apart.
- Silent test: Pre-check:
  - The current Index release shows Ohio's usage index below 1.0.
  - The public TechCred site shows the program is funded and accepts credentials submitted by providers.
  - ≤3 approved AI credentials target production or maintenance roles.
  Then submit the credential and publish a landing page with the syllabus, a sample module and the price. Pass: approved within 2 rounds, and ≥5 seats sold in the first round after approval. Fail: rejected twice, or 0 seats after one full round.
- First $: $450 per seat for 10 hours self-paced, a practical assessment and a verifiable credential page; ~75–120 days.
- Flags: Follow TechCred's provider and credential rules exactly. Make no outcome guarantees. Learners practice on synthetic manuals and logs, so no confidential employer data reaches us.
- Unique: Nearest is I-024, a curriculum download sold to teachers. This is a workforce credential that Ohio employers buy and the state reimburses. The money source, the buyer and the constraint all differ: an Ohio-only program for a region and occupations that lag in AI use.
- Tags: customer=Ohio manufacturers & logistics employers · mechanism=state-reimbursed workforce credential · resource=TechCred + Claude-built course + Index region/occupation gap
- Score (1-5): speed 1 · early 4 · fit 3 · ceiling 4

### I-038 · Accessible-math conversion for STEM course materials
- Money now flows to: Public universities and colleges pay vendors to fix PDFs for accessibility at about $3–15 per page. Equation-heavy files cost more, or the vendor won't take them. The schools also fund accessibility offices with long backlogs, while STEM faculty retype equations by hand in LMS editors. Notes that are scanned, handwritten or compiled from LaTeX usually show equations as images, which fails WCAG 2.1 AA.
- Why now: DOJ's Title II web rule set a deadline of Apr 24, 2026 for public entities serving ≥50k people, which includes state universities. Smaller entities have until Apr 26, 2027. Large institutions are therefore already past due. Educational instruction and science are among the fastest-growing Economic Index categories, so faculty already draft with AI. The math work is still manual: converting equations to LaTeX and then MathML, writing alt text for plots, adding structure, and validating. Vision models now transcribe handwritten and scanned equations well, and Pandoc/LaTeXML output MathML for free.
- Edge: A Claude Code pipeline with a local-model option. The validation stack (axe, PAC, and a read-through with NVDA + MathCAT) is shared with I-001's tooling.
- Silent test: Landing page with a free 2-page demo upload, targeting "make math PDF accessible," "handwritten notes accessible" and "MathML Canvas". Pass: ≥3 paid orders (≥150 pages total) within 45 days. Fail: 0 paid after ≥30 demos.
- First $: $4 per page for scanned or handwritten notes, $1.50 per page for born-digital LaTeX. Delivery in 72h: LMS-ready HTML with MathML, a tagged PDF and figure descriptions. A course packet runs about $200–600; ~20–40 days.
- Flags: Sell "WCAG 2.1 AA conformance checks," never legal compliance. Convert only material the buyer wrote or holds rights to (no publisher textbooks). Accept no student work or grades (FERPA). Confirm DOJ hasn't moved the Title II dates.
- Unique: Nearest is I-001, which applies the same DOJ rule to minutes and PDFs for small public bodies. This sells per-page conversion to STEM faculty and uses a different resource (vision math OCR → LaTeX → MathML). It targets the ≥50k cohort that is already past due.
- Tags: customer=STEM faculty & departments at public colleges · mechanism=per-page accessibility conversion · resource=vision math OCR + Pandoc/LaTeXML + Title II rule
- Score (1-5): speed 3 · early 4 · fit 3 · ceiling 3

### I-039 · Brief citation & quotation verifier for small-firm litigators
- Money now flows to: Big firms pay for Westlaw/Lexis brief-analysis add-ins. Solo and small firms spend associate or paralegal hours checking citations, or skip it. Since Mata v. Avianca (2023), courts have sanctioned lawyers in hundreds of cases over AI-invented citations. Penalties have included fines from about $1k to over $30k, disqualification and referral to the bar. More judges now require lawyers to certify how they used AI.
- Why now: Legal tasks are a small but growing share of Economic Index conversations, and each error costs more there than anywhere else. Free Law Project's CourtListener now holds the Caselaw Access Project's full run of US reporters. It offers opinion text and a citation-lookup API, and its open-source eyecite parser pulls citations out of text. Checking that a case exists is now nearly free. What nobody checks yet is whether the case name matches the citation, whether the pin cite falls inside the opinion, and whether quoted language actually appears in it.
- Edge: Claude Code connects eyecite, CourtListener and fuzzy quote matching into a one-upload report. Agent-instruction writing enforces a strict spec: flag problems, never give an opinion. No legal-database license is needed.
- Silent test: A free 10-citation check plus a $9 full report per brief, targeting "fake case citation checker" and "verify citations in brief". Pass: ≥100 free checks and ≥5 paid briefs in 45 days. Fail: <2 paid with ≥100 free checks (no willingness to pay), or <30 free checks (channel dead).
- First $: $9 per brief (up to 75 citations). Each citation gets red, amber or green: not found, name mismatch, pin cite outside the opinion, or quote not found. The report includes an exportable verification log. $29/mo for unlimited briefs; ~25–40 days.
- Flags: legal review (close to legal services; client confidentiality). It is not a citator and makes no claim that a case is still good law. Uploads are processed in memory, deleted after the report, and never used for training. Confirm CourtListener's API terms and rate limits allow commercial volume.
- Unique: Nearest is I-022, where AI personas critique a rulebook. This checks a court filing against an open case-law database with deterministic rules, for litigators. The resource (CourtListener/CAP + eyecite), buyer and mechanism all differ.
- Tags: customer=solo/small-firm litigators · mechanism=registry-backed verification report · resource=CourtListener + Caselaw Access Project + eyecite + Claude
- Score (1-5): speed 3 · early 3 · fit 3 · ceiling 4

### I-040 · "Can your AI agent answer this?" readiness audit for Shopify stores
- Money now flows to: Shopify merchants pay AI support agents (Intercom Fin or Gorgias class) about $1 per resolved conversation, or a plan fee. They pay freelancers and agencies $300–2,000 to write help-center content. They also absorb refunds and chargebacks when the agent guesses at a policy the store never wrote down, such as returns on sale items, international shipping, warranty or order changes.
- Why now: The Economic Index's Sep 2025 analysis of enterprise use found that API use leans heavily toward automation. It also found that complex deployments are held back more by getting the right context to the model than by price. Merchants turn agents on for holiday volume and January returns. Claude can generate the questions a store's customers will ask from the store's own products and policies, then test whether the published content answers each one.
- Edge: The eval method from the agent-instruction builder (test prompts with expected outputs), built with Claude Code. Read-only access to the store's own products, pages and policies means the app never touches customer data, which avoids Shopify's review for that data. The exported eval CSV works with any vendor's agent.
- Silent test: Shopify App Store listing with a free 20-question scan. Pass: ≥50 installs and ≥5 paid within 60 days of approval. Fail: <15 installs (channel dead), or 0 paid after ≥50 installs.
- First $: $49 one-time full audit: 150 generated questions, each scored as answered, ambiguous or missing; draft policy and FAQ text for the merchant to approve; and an eval CSV. Or $19/mo to re-scan when the catalog or policies change. ~45–75 days, covering the build and app review.
- Flags: Store content only, with no customer or order data. The merchant approves every policy text; never invent terms on their behalf. Disclose that the text is AI-generated.
- Unique: Nearest is I-019, a service that ports agent instructions. This is a self-serve app-store product that scores a merchant's own content against generated customer questions. The buyer (e-commerce merchants), channel (app store) and mechanism (gap scoring plus eval export) all differ.
- Tags: customer=Shopify merchants deploying AI support agents · mechanism=app-store content-gap audit + eval-set generator · resource=Claude + Shopify Admin API (own-store data) + agent-eval method
- Score (1-5): speed 2 · early 4 · fit 3 · ceiling 4

**Round 2** (L4 local geography)

### I-041 · Township hybrid-worker city-tax refund kit
- Money now flows to: Hybrid workers living in SW Ohio townships pay city income tax on days they work from home. Townships levy no municipal income tax (outside JEDD areas); these residents live in West Chester, Liberty and Fairfield Twp in Butler; Green, Colerain, Anderson and Delhi in Hamilton; Deerfield in Warren; and Washington and Miami in Montgomery. Employers still withhold 1–2.5% for the office city (Cincinnati 1.8%, Dayton 2.5%, Blue Ash, Mason, Sharonville) on every day, including home days. Getting it back takes that city's own refund form, a day log and an employer-signed statement. Most never file, or they pay preparers $50–150 extra per city return.
- Why now: Ohio taxes wages where the work is done. HB 197's COVID-era rule ended after 2021, and Schaad v. Alder (2024) settled 2020. Refunds can go back 3 years, so tax-year 2023 claims expire around Apr 15, 2027, and the 2027 season is the last one that can claim four years (2023–26) at once. Census TIGER place boundaries answer "city or township?" for any address. AI turns a calendar export or badge history into a dated day log and fills each city's form.
- Edge: Here the local geography is the product. Roughly 600–700k people live in township areas of Butler, Hamilton, Warren and Montgomery counties, and many commute into income-tax cities. The versioned-catalog method keeps one record per city: administrator (RITA, CCA or self-administered), form, employer-signature rule and deadline.
- Silent test: Free "Do I owe city tax on my home-office days?" address checker + refund estimator, with a $29 kit. Pass: ≥15 paid kits by Apr 15, 2027 with ≥1,000 checker uses. Fail: <4 paid.
- First $: $29 kit for one work city and up to four tax years: day-log builder, pre-filled refund forms, employer-letter template, mailing checklist. ~30–60 days, since 2023–25 claims can be filed now.
- Flags: legal review (tax). This is a forms organizer, not tax advice or return preparation. Warn residents of income-tax cities that the resident-city credit can wipe out the gain. The address check runs only on the buyer's own address and stores nothing.
- Unique: Closest is I-023 (Etsy seller tax-season sheet). This one differs in customer (W-2 hybrid workers in townships), resource (Ohio municipal income-tax law + city/township boundary data) and mechanism (recovering over-withheld tax before a dated lookback deadline).
- Tags: customer=SW Ohio hybrid workers living in townships · mechanism=refund-recovery kit with lookback deadline · resource=Ohio muni-tax rules + Census place boundaries + catalog method
- Score (1-5): speed 3 · early 4 · fit 4 · ceiling 3

### I-042 · Board of Revision value-challenge kit for the 2026 update
- Money now flows to: Homeowners and small landlords who think the auditor's new value is too high either pay the higher tax or hire help to file a Board of Revision complaint (DTE Form 1), which can only be filed Jan 1–Mar 31. Tax-appeal firms work on contingency (often 25–50% of first-year savings); appraisers charge $350–600.
- Why now: Butler and several neighboring counties set new values for tax year 2026 in the triennial update after their 2023 reappraisal (confirm in the pre-check). Owners can generally file only once per three-year cycle, so the cycle's first year is the time to file. HB 126 (2024) sharply limited school boards' value complaints and appeals, which lowers owners' risk. County auditors publish sales and appraisal files, so a script can compute each auditor neighborhood's median value-to-sale ratio, the core evidence a hearing weighs.
- Edge: Local geography plus data-joining: sales-ratio tables by neighborhood for Butler, Hamilton, Warren and Montgomery. Bayesian shrinkage (from the brief's methods) keeps thin-sample neighborhoods from looking over-assessed by chance.
- Silent test: Pre-check: ≥2 of the 4 counties issued new TY2026 values and offer sales data as an official download (no scraping); otherwise stop. By Jan 2, publish free "Is your neighborhood over-assessed? 2025–26 sales vs 2026 values" pages with a $29 parcel kit. Pass: ≥20 paid kits by Mar 31, 2027. Fail: <5 paid with ≥1,500 visits.
- First $: $29 kit for the buyer's own parcel: neighborhood ratio, 5 arm's-length comps by parcel number, DTE Form 1 walkthrough, evidence and hearing checklist. $99 for up to 10 parcels for small landlords. ~45–75 days (the window opens Jan 1).
- Flags: legal review (property tax). Ohio limits who may file for someone else, so owners file their own complaint, and the kit is not legal advice. No owner names anywhere: public pages show only neighborhood aggregates, and comps appear only in the buyer's own report.
- Unique: Closest is I-003 (aggregated SW Ohio public price data). This one differs in resource (auditor sales and appraisal files, not bid tabs), customer (property owners) and mechanism (evidence kit timed to a dated annual appeal window).
- Tags: customer=SW Ohio homeowners + small landlords · mechanism=seasonal appeal-evidence kit · resource=county auditor sales/appraisal data + Bayesian methods
- Score (1-5): speed 3 · early 3 · fit 4 · ceiling 3

### I-043 · CAUV-qualifying nursery plan for 3–9.9 acre owners
- Money now flows to: Owners of 3–9.9 acre exurban parcels in Butler, Warren, Preble and Clermont pay property tax at full market value on their open acres. CAUV, Ohio's farm-use valuation, often values land 85–95% below market, but parcels under 10 acres qualify only if they gross an average $2,500/yr from commercial agriculture. The usual route, leasing the ground to a hay or row-crop farmer, rarely works on small, broken-up acreage. On ~6 open acres that means ~$1.5–2.5k/yr in savings left unclaimed.
- Why now: The 2026 value update raised the land portion of these bills. CAUV applications (DTE 109, $25) are due at the county auditor by the first Monday in March (Mar 1, 2027). Nursery stock counts as commercial agriculture, and a small propagation bed of fast-rooting hardwood cuttings (elderberry, ninebark, red-twig dogwood, willow, native shrubs) can gross $2,500 on a fraction of an acre. Web Soil Survey plus the state's CAUV soil tables make a per-parcel savings estimate automatic.
- Edge: The propagation skill supplies realistic yields per bed and timing, alongside the garden catalog and Fermi sizing. Local knowledge of western Butler's exurban townships (Ross, Hanover, Milford, Reily, Morgan) helps. Wooded parcels of ≥10 acres get the Ohio Forest Tax Law route instead.
- Silent test: Free "CAUV savings estimate" page (acres, soils from Web Soil Survey, county rates), with a $39 playbook. Pass: ≥10 paid by Mar 1, 2027 with ≥800 estimator uses. Fail: <3 paid.
- First $: $39 PDF + sheet: eligibility checklist, a 3-year propagation income plan (plants, bed sizes, wholesale-to-garden-center channel), records and receipts kit, DTE 109 walkthrough, recoupment warning. ~30–60 days.
- Flags: legal review (tax). The auditor decides eligibility; warn clearly about the "exclusively commercial agriculture" requirement, the homesite carve-out, and recoupment if the land later leaves CAUV. Selling nursery stock requires an ODA nursery license, so the plan includes getting one.
- Unique: Closest is I-017 (off-patent plant list for propagators). This one differs in customer (small-acreage landowners), mechanism (a micro-farm plan that qualifies the land for a tax valuation) and constraint exploited (Ohio's under-10-acre CAUV income test).
- Tags: customer=SW Ohio small-acreage landowners · mechanism=tax-qualification playbook · resource=Ohio CAUV rules + Web Soil Survey + propagation skill
- Score (1-5): speed 3 · early 4 · fit 4 · ceiling 2

### I-044 · Great Miami corridor flood-zone exit screener (LOMA)
- Money now flows to: Homeowners with federally backed mortgages in FEMA flood zones along the Great Miami River (Hamilton, Middletown, Fairfield, Miamisburg, West Carrollton, Dayton), Mill Creek and the Ohio River must carry flood insurance. Risk Rating 2.0 raises those premiums every year until they reach full-risk rates. Owners whose ground actually sits above the base flood elevation (BFE) can file a free FEMA LOMA to be removed from the zone. Today they either pay a surveyor $400–900 for an elevation certificate without knowing their odds, or pay a LOMA consultant $1–2.5k.
- Why now: Ohio's statewide LiDAR and USGS 3DEP give sub-meter ground elevations. FEMA's NFHL publishes BFEs and zone lines, and open building footprints locate each house. A script can compare the ground around a footprint with the BFE in seconds. OpenFEMA's anonymized policy data shows where premiums concentrate.
- Edge: Local geography: river towns protected by levees and the conservancy district, with mapped zones that cut through old neighborhoods. The game-dev 3D/geometry skill and a Claude Code GIS pipeline run at $0 on open data.
- Silent test: Pre-check: screen all Butler County flood-zone footprints, and continue only if ≥10% have lowest ground ≥1 ft above the BFE. Then launch a free "Is your house really in the flood zone?" lookup with a $39 screening report. Pass: ≥8 paid in 60 days with ≥600 lookups. Fail: <2 paid.
- First $: $39 report: LiDAR ground vs BFE around the footprint, LOMA odds, MT-EZ walkthrough, what the surveyor must certify, lender-waiver letter template. ~30–60 days.
- Flags: Screening only, not a survey or engineering opinion; a licensed surveyor or engineer certifies. A lender may still require coverage, so recommend keeping voluntary coverage. Lookups use only the buyer's own address; no owner names or policy-level data.
- Unique: Closest is I-007 (per-site report from public maps). This one differs in resource (current LiDAR and FEMA NFHL data, not historical maps), customer (homeowners, not environmental consultants) and mechanism (screening for a free federal remedy that ends a recurring premium).
- Tags: customer=flood-zone homeowners in SW Ohio river towns · mechanism=geodata screening report → free federal remedy · resource=Ohio LiDAR/3DEP + FEMA NFHL + open building footprints
- Score (1-5): speed 2 · early 3 · fit 3 · ceiling 4

### I-045 · Ohio local-government spend intel for B2G vendors
- Money now flows to: Small vendors that sell to Ohio cities, townships, schools and libraries (IT/MSP, mowing, road salt, uniforms, engineering, software) pay ~$5–30k/yr for GovSpend/GovWin-class spend databases. The rest guess who buys what, from whom, and when the contract renews.
- Why now: OhioCheckbook.com posts line-level payments for the state and for hundreds of opted-in local governments, a level of detail few states match. LLMs can now merge vendor-name variants, sort free-text payment memos into categories (NIGP-style) and spot each entity's renewal month. That cleanup used to be the costly part of any spend-data product.
- Edge: An Ohio-specific transparency asset, plus data-joining and the versioned-catalog skill (quarterly editions). SW Ohio's dense mix of townships, villages and districts is familiar ground.
- Silent test: Pre-check: Checkbook's export terms allow reuse, and ≥150 SW Ohio local entities are in the data; otherwise stop. Publish 10 free teaser pages (e.g., "Who SW Ohio townships paid for IT, 2024–26: top 15 vendors") with $99 category reports and a $49/mo explorer. Pass: ≥3 paid reports or ≥1 subscription in 45 days. Fail: 0 paid with ≥400 visits.
- First $: $99 category report (spend by entity, incumbent vendor, typical renewal month, 3-year trend). ~21–45 days.
- Flags: Leave out payments to individuals (employees, refunds, sole proprietors trading under personal names). Use only the official exports, with no scraping, and link every figure to its source.
- Unique: Closest is I-003 (bid-tab unit prices). This one differs in resource (checkbook payment ledgers, not bid tabulations), customer (vendors' sales teams, not estimators) and mechanism (account and incumbent intelligence, not cost data).
- Tags: customer=small B2G vendors selling into Ohio local government · mechanism=spend-intelligence reports + subscription · resource=Ohio Checkbook + AI entity resolution
- Score (1-5): speed 3 · early 4 · fit 4 · ceiling 4

### I-046 · New bar & restaurant feed from Ohio liquor-permit notices
- Money now flows to: Vendors that need to reach a restaurant 30–90 days before it opens pay $100–300/mo for national "new business" lead lists, which are stale and thin on SW Ohio, or send reps to drive around looking for "coming soon" signs. These include POS resellers, linen and uniform services, kitchen-equipment dealers, grease-trap and pest-control firms, distributor reps and insurance agents.
- Why now: The Division of Liquor Control notifies the local council or township trustees of every new or transferred permit (D-5, D-1/D-2, C-1/C-2), and they have 30 days to object. Each notice shows up as a dated item in a public agenda PDF, and the Division's permit search shows its status. AI can now read dozens of agenda packets a week and match each notice to a commercial build-out permit. New and expanded DORAs (outdoor drinking districts) in Hamilton, Middletown, Fairfield and Mason keep openings coming.
- Edge: Local geography (the council and trustee agenda pages of Butler, Hamilton, Warren and Montgomery jurisdictions), a Claude Code agenda parser and a weekly versioned feed.
- Silent test: Publish a free monthly "New SW Ohio bar & restaurant permits, Nov 2026" page showing half the rows, plus a $29/mo full weekly CSV/email feed. Pass: ≥3 subscribers in 45 days. Fail: 0 with ≥300 visits.
- First $: $29/mo feed (business/dba, address, permit class, filing date, council date, matched build-out permit). ~21–45 days.
- Flags: Business names only, never individual applicants or principals. Read public agendas and the Division's public search at polite rates, or request records through public-records web forms. Nothing alcoholic is sold, so liquor rules don't apply.
- Unique: Closest is I-005 (SW Ohio catalog built from local-government pages). This one differs in mechanism (event-triggered B2B lead feed, not a requirements catalog), resource (liquor-permit notices in council agendas) and customer (vendors to new restaurants).
- Tags: customer=vendors selling to new restaurants/bars · mechanism=public-filing lead-feed subscription · resource=Ohio liquor-permit notices + council agendas + building permits
- Score (1-5): speed 4 · early 3 · fit 3 · ceiling 3

### I-047 · Ohio small-business electric contract checkup
- Money now flows to: Small commercial accounts in Duke Energy Ohio and AES Ohio territory (restaurants, churches, small offices, shops) sign supplier contracts through brokers, who often bury a 0.3–1.5¢/kWh fee in the rate. Many of these contracts roll into variable rates at term end, and some "fixed" contracts have added capacity pass-through charges since PJM's capacity price spike.
- Why now: PJM capacity costs have reached the utilities' default-service prices and supplier offers in 2025–26, so contracts renewing in 2027 face a sharp step up. PUCO publishes the default price to compare and every supplier's offers ("Apples to Apples"). A vision LLM can pull rate, term, renewal date, early-termination fee and pass-through clauses from a bill and contract PDF in seconds.
- Edge: Ohio's retail-choice rules and local utility territories. The PJM research overlaps with I-004 if both run, and the brief's Bayesian method can estimate the next price-to-compare reset. Taking no commissions makes the advice unconflicted.
- Silent test: Free "Ohio price-to-compare tracker" page (Duke/AES history plus the next reset) and a $39 checkup. Pass: ≥5 paid in 60 days with ≥500 visits. Fail: <2 paid.
- First $: $39 per account: contract terms extracted, cost compared with default service and the 3 best fixed offers, renewal and cancel-by dates as calendar events, red-flag clauses. $99 for up to 5 accounts. ~30–60 days.
- Flags: legal review. PUCO certifies brokers and aggregators, so stay advisory: no supplier payments, no arranging contracts, no legal advice on contract terms. Buyers upload only their own bill; delete it after delivery.
- Unique: Closest is I-004 (PJM peak alerts). This one differs in mechanism (a one-off contract audit, not operational alerts), customer (small commercial accounts, not large sites with capacity tags) and resource (PUCO Apples-to-Apples data + the buyer's own bill and contract).
- Tags: customer=Ohio small commercial electricity accounts · mechanism=document audit + market benchmark · resource=PUCO retail-choice data + vision LLM
- Score (1-5): speed 3 · early 4 · fit 3 · ceiling 3

### I-048 · Ohio solar & storage land-offer benchmark
- Money now flows to: Farmland owners in SW and west-central Ohio (Preble, Darke, Clinton, Greene, Clark, Madison, Fayette) are getting option and lease offers from solar and battery developers. They pay attorneys $1.5–5k to review them, or sign at the landman's first rent ($600–1,200/acre/yr) without knowing local comparables, who pays CAUV recoupment, or whether their county bans the project.
- Why now: Data-center load and PJM's capacity spike have developers hunting for sites near substations with spare capacity. SB 52 (2021) lets counties ban utility-scale solar in some or all townships, and many have. OPSB dockets publish each project's acreage and total landowner payments, so $/acre can be worked out. PJM's queue lists projects by county and substation. LLMs can mine both in a day.
- Edge: Ohio-specific rules: SB 52 restricted areas, CAUV recoupment when farmland converts, and drainage-tile repair (a big issue on Ohio farms). Local geography, and a versioned catalog of county status and project payments.
- Silent test: Publish free county pages ("Solar leasing in [county], Ohio: bans, queued projects, typical rent") for ~15 counties, with a $49 report. Pass: ≥4 paid in 60 days. Fail: <1 paid with ≥500 visits.
- First $: $49 report for the buyer's area: county and township ban status, queued projects and substations within 10 mi, $/acre range from OPSB filings, and a 25-item clause checklist (CAUV recoupment, decommissioning bond, tile repair, crop damage). ~30–60 days.
- Flags: legal review (real-property contracts). Not legal advice; take no attorney or developer referral fees. Leave out the participating landowners named in OPSB filings.
- Unique: Closest is I-004 (also built on PJM data). This one differs in customer (rural landowners), mechanism (offer benchmark + clause checklist) and resource (OPSB dockets, SB 52 county resolutions and the PJM interconnection queue).
- Tags: customer=Ohio farmland owners with energy-lease offers · mechanism=offer-benchmark report · resource=OPSB dockets + PJM queue + SB 52 county resolutions
- Score (1-5): speed 2 · early 4 · fit 3 · ceiling 3

## Round log

| Round | Lenses | Proposed | Accepted | Note |
|---|---|---|---|---|
| 1 | L1 stale flows · L2 free assets · L3 skills | 24 | 24 | All distinct; Sanborn used twice for different buyers |
| 2 | L5 moat · L6 AI shovels | 16 | 16 | All distinct; Title II now anchors I-001, I-032, I-038 |
| 2 | L4 local geography | 8 | 8 | All distinct; resumed after usage limit |
