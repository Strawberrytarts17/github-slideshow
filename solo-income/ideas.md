# Solo Income Ideas

Single source list for the brainstorm. Agents add ideas; the orchestrator merges, dedupes, and shortlists.
Instructions for round agents: [round-agent.md](round-agent.md).

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

## Round log

| Round | Lenses | Proposed | Accepted | Note |
|---|---|---|---|---|
| 1 | L1 stale flows · L2 free assets · L3 skills | 24 | 24 | All distinct; Sanborn used twice for different buyers |
