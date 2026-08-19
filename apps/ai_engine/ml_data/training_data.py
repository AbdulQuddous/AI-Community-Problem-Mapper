TRAINING_EXAMPLES = [
    # ============================================================
    # 1. GARBAGE CATEGORY (50 examples)
    # Focus: Uncollected household waste, overflowing bins, trash piles, missed collection, rotting waste attracting pests
    # ============================================================
    # --- Short Examples (13) ---
    ("Kitchen waste bags remain uncollected on Maple Lane.", "garbage"),
    (
        "Flies are swarming the full dumpster behind our bakery.",
        "garbage",
    ),
    (
        "Four days without refuse collection along Elm Court.",
        "garbage",
    ),
    (
        "Empty the rotting household rubbish bin near the clinic.",
        "garbage",
    ),
    (
        "Crows tore open uncollected trash sacks outside block 4.",
        "garbage",
    ),
    (
        "Green waste containers on 3rd Street are overflowing.",
        "garbage",
    ),
    ("Our residential wheelie bin was completely skipped today.", "garbage"),
    (
        "Decomposing food scraps left sitting beside the bus shelter.",
        "garbage",
    ),
    (
        "Foul odor rising from unattended domestic garbage bags.",
        "garbage",
    ),
    ("Garbage truck missed our alleyway three times this month.", "garbage"),
    ("Unemptied trash cans blocking pedestrian access near the pharmacy.", "garbage"),
    ("Maggots crawling over uncollected organic refuse on Pine Road.", "garbage"),
    ("Rats spotted inside the overflowing residential garbage bin.", "garbage"),
    # --- Medium Examples (22) ---
    (
        "Because sanitation trucks missed Monday morning pickup, putrid organic rubbish is fermenting in the summer heat.",
        "garbage",
    ),
    (
        "Communal dumpsters outside Greenfield Housing Society have sat unemptied for eight days, creating a severe health hazard.",
        "garbage",
    ),
    (
        "Stray dogs ripped through uncollected household trash sacks stacked beside the grocery store entrance this morning.",
        "garbage",
    ),
    (
        "When will sanitation staff haul away the decomposing waste pile accumulated outside the primary school?",
        "garbage",
    ),
    (
        "Festering food waste bags on Oak Avenue are producing an unbearable stench that penetrates our living rooms.",
        "garbage",
    ),
    (
        "If waste collectors ignore our sector again tomorrow, uncollected domestic refuse will spill across the roadway.",
        "garbage",
    ),
    (
        "Sanitation workers bypassed our cul-de-sac on Wednesday, leaving twelve overflowing domestic bins sitting on the curb.",
        "garbage",
    ),
    (
        "Uncollected kitchen scraps stacked near the commercial plaza are drawing hordes of rodents and swarming flies.",
        "garbage",
    ),
    (
        "Ten days without curbside trash pickup has turned our front porch into an accidental waste repository.",
        "garbage",
    ),
    (
        "Rotting vegetable matter and uncollected domestic refuse outside building 12 are leaking dark, smelly fluids.",
        "garbage",
    ),
    (
        "Our housing block has not seen a municipal garbage truck since last Thursday morning.",
        "garbage",
    ),
    (
        "Local shopkeepers cannot open their display windows due to the rancid stench from the unemptied trash container.",
        "garbage",
    ),
    (
        "Urgent collection needed for five overflowing refuse bins stationed outside the community health centre.",
        "garbage",
    ),
    (
        "Rotting household refuse has accumulated into a massive mound outside the dental clinic on 7th Avenue.",
        "garbage",
    ),
    (
        "Sanitation crews emptied bins on the main road but ignored every residential side street in our neighborhood.",
        "garbage",
    ),
    (
        "Two missed trash collection cycles have left our apartment complex with twenty overflowing green bins.",
        "garbage",
    ),
    (
        "Foul-smelling garbage mounds sitting outside the temple entrance are ruining religious morning gatherings.",
        "garbage",
    ),
    (
        "Can someone send a garbage compactor truck to clear the uncollected residential waste bins on Willow Way?",
        "garbage",
    ),
    (
        "Unattended refuse bags left on the sidewalk have torn open, scattering soiled food packaging everywhere.",
        "garbage",
    ),
    (
        "Six days of uncollected residential trash has turned our apartment entryway into a putrid breeding zone for pests.",
        "garbage",
    ),
    (
        "Municipal collectors forgot our entire block during Tuesday's scheduled morning waste round.",
        "garbage",
    ),
    (
        "Disgusting garbage heaps outside the fish market are decaying rapidly under direct midday sunlight.",
        "garbage",
    ),
    # --- Long Examples (15) ---
    (
        "Since Wednesday of last week, sanitation vehicles have completely failed to service the residential refuse bins on Sunset Boulevard, resulting in huge mounds of decomposing food scraps that attract stray cats and rodents.",
        "garbage",
    ),
    (
        "Elderly residents on Oak Lane cannot step onto the sidewalk because putrid, leaking domestic garbage bags have been stacking up along the curb ever since the scheduled municipal collection was abruptly cancelled.",
        "garbage",
    ),
    (
        "The stench from the unemptied residential waste container behind the shopping arcade is overwhelming nearby apartments, and rotting liquid is oozing across the walkway where children walk to school every morning.",
        "garbage",
    ),
    (
        "Unless municipal crews dispatch a compactor truck to clear the decomposing trash mountains beside the maternity hospital, patients and healthcare staff will face severe bacterial contamination risks from swarming flies.",
        "garbage",
    ),
    (
        "Five overflowing communal trash dumpsters at the intersection of 12th and Pine have sat unemptied through hot weather, causing decaying organic refuse to bake onto the sidewalk and produce a nauseating odor.",
        "garbage",
    ),
    (
        "Our neighborhood welfare association repeatedly logged requests for waste pickup for the bins near block B, yet the collection vehicle drove right past without clearing a single household container.",
        "garbage",
    ),
    (
        "Piles of residential rubbish bags have grown into a waist-high heap outside the pediatric clinic because regular weekly collection has been absent for nearly thirteen days without explanation.",
        "garbage",
    ),
    (
        "Because our street was skipped by the morning sanitation route, ten households were forced to leave bursting trash cans outside, which neighborhood dogs promptly knocked over and scattered across driveways.",
        "garbage",
    ),
    (
        "Rotting food residues inside the unserviced municipal dumpster on Commercial Road have begun fermenting, producing a vile acidic stench that makes outdoor dining impossible for adjacent café owners.",
        "garbage",
    ),
    (
        "If the sanitation department does not empty the overflowing communal refuse bins outside our apartment block before the weekend, decomposing meat scraps will create an unbearable environmental sanitation crisis.",
        "garbage",
    ),
    (
        "Twelve days of uncollected household waste on Cedar Avenue has created an intolerable nuisance, with foul leachate trickling down the curb and entering underground stormwater openings.",
        "garbage",
    ),
    (
        "Residents across Hillside Colony are frustrated because municipal garbage trucks consistently skip odd-numbered houses during weekly rounds, leaving dozens of families stranded with festering kitchen waste.",
        "garbage",
    ),
    (
        "Unattended domestic waste bags piled high outside the municipal library have started decomposing, releasing a suffocating odor that forces staff to keep all ground-floor windows tightly shut.",
        "garbage",
    ),
    (
        "When will municipal authorities ensure that waste removal crews actually collect the curbside bins on River Lane rather than marking the scheduled route complete while bins remain completely full?",
        "garbage",
    ),
    (
        "Spoiled organic scraps and uncollected diaper bags sitting in the midday sun outside the daycare center are attracting swarms of blowflies, creating an immediate health hazard for toddlers.",
        "garbage",
    ),
    # ============================================================
    # 2. ROADS CATEGORY (50 examples)
    # Focus: Potholes, cracked pavement, broken/damaged road surfaces, uneven roads, road collapse, missing road markings
    # ============================================================
    # --- Short Examples (13) ---
    ("Massive asphalt crater near the central bus terminal.", "roads"),
    ("Pothole on 3rd Street damaged my vehicle suspension.", "roads"),
    ("Crumbling pavement along Highway 9 requires urgent resurfacing.", "roads"),
    ("Sunken road section outside the primary school entrance.", "roads"),
    ("Sharp road depression on 8th Avenue popped my tire.", "roads"),
    ("Cracked tarmac at the corner of Pine and 4th.", "roads"),
    ("Repave the uneven road surface near the market.", "roads"),
    ("Severe pavement erosion splitting the outer northbound lane.", "roads"),
    ("Deep fissures spreading across the newly paved bridge road.", "roads"),
    ("Faded center lane markings on bypass road cause confusion.", "roads"),
    ("Asphalt collapsed into a two-foot cavity on Elm Street.", "roads"),
    ("Dangerous road rutting scraping vehicle undercarriages on Grand Avenue.", "roads"),
    ("Broken concrete slabs protruding along the industrial bypass road.", "roads"),
    # --- Medium Examples (22) ---
    (
        "Deep craters on Industrial Parkway are forcing heavy delivery trucks to swerve erratically into oncoming traffic lanes.",
        "roads",
    ),
    (
        "Because asphalt along Grand Avenue has disintegrated into loose stones, multiple scooter riders have slipped during rush hour.",
        "roads",
    ),
    (
        "Wheelchair users cannot cross 7th Street safely due to jagged fissures and broken road pavement near the pedestrian crossing.",
        "roads",
    ),
    (
        "After yesterday's rainstorm, the pothole opposite the maternity clinic expanded into a dangerous two-foot-wide trench.",
        "roads",
    ),
    (
        "When will public works crews resurface the crumbling tarmac between 14th Street and the bypass interchange?",
        "roads",
    ),
    (
        "Uneven asphalt settling on the eastbound expressway overpass creates severe vehicle bouncing at high commuter speeds.",
        "roads",
    ),
    (
        "Subsurface erosion caused a large section of pavement on Cedar Road to sink five inches overnight.",
        "roads",
    ),
    (
        "Damaged road surface outside the grocery warehouse has developed deep ruts that scrape the bumpers of standard cars.",
        "roads",
    ),
    (
        "Heavy seasonal rains completely washed away the top asphalt layer on Hillside Road, exposing sharp underlying stones.",
        "roads",
    ),
    (
        "Missing road markings combined with severely rutted tarmac make night driving hazardous along the south ring corridor.",
        "roads",
    ),
    (
        "Cracked asphalt near the train station is breaking apart into loose gravel that flies into car windshields.",
        "roads",
    ),
    (
        "Our neighborhood access road has completely deteriorated into a bumpy, uneven strip of fractured concrete.",
        "roads",
    ),
    (
        "Delivery drivers are refusing to enter Rosewood Lane because deep roadway depressions damage commercial wheel alignments.",
        "roads",
    ),
    (
        "If road maintenance does not patch the widening cavity on Church Road, the entire outer lane will collapse.",
        "roads",
    ),
    (
        "Jagged asphalt edges along the newly widened intersection of Main and Oak are slicing through bicycle tires.",
        "roads",
    ),
    (
        "Pothole clusters along Market Street make driving virtually impossible without swerving onto the opposite shoulder.",
        "roads",
    ),
    (
        "Crumbled asphalt and loose stones outside the college gates cause daily skidding incidents among student motorcyclists.",
        "roads",
    ),
    (
        "Resurface the damaged intersection outside City Hospital to prevent ambulances from jarring critically ill patients.",
        "roads",
    ),
    (
        "A sudden road surface cave-in on Victoria Avenue has left a three-foot hole directly in the driving lane.",
        "roads",
    ),
    (
        "Worn-out road markings on the four-lane highway crossing have vanished completely, leading to near-miss collisions every evening.",
        "roads",
    ),
    (
        "Continuous truck traffic has crushed the asphalt on Freight Way into uneven waves and dangerous ridges.",
        "roads",
    ),
    (
        "Severe subsidence along the riverbank road has created a steep tilt across both vehicle travel lanes.",
        "roads",
    ),
    # --- Long Examples (15) ---
    (
        "Asphalt roadway directly outside the children's hospital has broken into jagged chunks and deep ruts, forcing emergency ambulances to brake abruptly and risking vehicle damage during urgent patient transfers.",
        "roads",
    ),
    (
        "Since last month's storm, a five-foot wide depression in the asphalt on Western Avenue has steadily worsened, and motorists dodging the crater frequently swerve across double yellow lines into opposing traffic.",
        "roads",
    ),
    (
        "Deep longitudinal cracks running down the middle lane of Commercial Boulevard have begun separating into distinct gaps, creating an extreme skidding hazard for bicyclists and two-wheeler commuters in wet conditions.",
        "roads",
    ),
    (
        "Unless maintenance teams patch the cluster of jagged potholes spanning the intersection of Market and 2nd, continuous pounding from municipal buses will cause total asphalt collapse before winter sets in.",
        "roads",
    ),
    (
        "Crumbling road margins along River Road have eroded into the adjacent ditch, narrowing the usable driving lane and leaving dangerously sharp asphalt edges exposed to oncoming morning commuters.",
        "roads",
    ),
    (
        "Our delivery van blew two tires yesterday afternoon because the broken pavement near the freight depot contains exposed rebar and razor-sharp chunks of fragmented concrete tarmac.",
        "roads",
    ),
    (
        "Multiple deep potholes near the university campus gate have caused three scooter accidents this week alone, with riders losing control over the crumbled, uneven road surface during evening peak hours.",
        "roads",
    ),
    (
        "Because the asphalt foundation on 5th Street was poorly laid, heavy summer monsoon rains have stripped the top tar layer, leaving behind an undulating surface of loose gravel and hazardous craters.",
        "roads",
    ),
    (
        "If municipal road crews do not fill the massive cavity opening up near the highway off-ramp, high-speed passenger vehicles will suffer catastrophic tire blowouts or rollover accidents.",
        "roads",
    ),
    (
        "Extensive frost heaves and asphalt fracturing along the northern collector road have made school bus transit dangerously bumpy, causing young students to bounce violently in their seats.",
        "roads",
    ),
    (
        "The newly paved surface on Airport Road is already exhibiting severe alligator cracking and settling, indicating catastrophic base failure that requires complete milling and resurfacing by road contractors.",
        "roads",
    ),
    (
        "Missing crosswalk paint and completely obliterated lane divider markings on Broad Avenue make pedestrian navigation terrifying, especially for visually impaired citizens trying to reach the clinic.",
        "roads",
    ),
    (
        "A severe structural road depression outside the post office has formed a four-inch ledge, jarring vehicle axles and threatening to crack oil pans on lower-riding passenger cars.",
        "roads",
    ),
    (
        "When will public works engineers inspect the fractured road deck on the canal bridge, where expanding cracks and missing asphalt chunks expose bare steel mesh to vehicle tires?",
        "roads",
    ),
    (
        "Uneven asphalt settling across three lanes of the south interchange causes heavy trailers to sway precariously, posing an immediate hazard to smaller passenger vehicles traveling alongside.",
        "roads",
    ),
    # ============================================================
    # 3. WATER CATEGORY (50 examples)
    # Focus: Clean water supply, dry taps, low pressure, broken water mains, municipal delivery tankers
    # ============================================================
    # --- Short Examples (13) ---
    ("No running water in our apartment since dawn.", "water"),
    ("Low water pressure makes bathing completely impossible upstairs.", "water"),
    ("Murky brown water coming from our main pipeline.", "water"),
    ("Broken water main flooding the corner of 6th.", "water"),
    ("Municipal water tanker never arrived in our sector today.", "water"),
    ("Dry pipeline throughout block C for 48 hours.", "water"),
    ("Restore drinking water supply to the residential colony.", "water"),
    ("High chlorine smell in our municipal drinking supply.", "water"),
    ("Water supply cuts without prior warning across Sector 4.", "water"),
    ("Discolored, rusty water flowing into residential storage tanks.", "water"),
    ("Zero water flow from municipal inlet pipes since yesterday.", "water"),
    ("Ruptured freshwater conduit wasting drinking water on Oak Street.", "water"),
    ("Tainted, cloudy drinking water causing stomach illness among neighbors.", "water"),
    # --- Medium Examples (22) ---
    (
        "For three consecutive days, our taps have been completely dry across the entire Northridge housing development.",
        "water",
    ),
    (
        "Rusty, discolored municipal water with visible sediment has been flowing into our household storage tanks since Thursday.",
        "water",
    ),
    (
        "Because incoming water pressure dropped to zero, local restaurants cannot operate their dishwashing and cooking equipment.",
        "water",
    ),
    (
        "A ruptured supply main under Maple Drive is shooting clean drinking water twenty feet into the air.",
        "water",
    ),
    (
        "When is the city water board going to refill our communal supply overhead tank in sector 4?",
        "water",
    ),
    (
        "Elderly residents on 3rd floor flats are carrying heavy buckets because line pressure cannot push water upstairs.",
        "water",
    ),
    (
        "Foul, chemical-smelling tap water coming through the public connection is causing skin irritation among neighborhood children.",
        "water",
    ),
    (
        "Since Monday morning, over sixty families in our apartment complex have been without any municipal water supply.",
        "water",
    ),
    (
        "Clean drinking water continues to gush wastefully from a cracked distribution pipe opposite the government polytechnic.",
        "water",
    ),
    (
        "Scheduled tanker distribution for our drought-affected neighborhood was cancelled without notice, leaving two hundred families stranded.",
        "water",
    ),
    (
        "Incoming water pressure is too feeble to fill our ground-floor cistern, leaving our household without cooking water.",
        "water",
    ),
    (
        "Yellowish drinking water containing grit and silt has been entering our kitchen taps for two days.",
        "water",
    ),
    (
        "Our entire housing society has suffered an unannounced water shutdown since five o'clock this morning.",
        "water",
    ),
    (
        "If municipal water engineers do not restore supply today, the local clinic cannot maintain sanitary operations.",
        "water",
    ),
    (
        "A broken municipal water valve on 10th Avenue is leaking thousands of liters of treated freshwater.",
        "water",
    ),
    (
        "Residents in Block G have received only twenty minutes of trickle water pressure over the past forty-eight hours.",
        "water",
    ),
    (
        "Contaminated tap water smelling strongly of petroleum is flowing into residential homes along Meadow Street.",
        "water",
    ),
    (
        "Send an emergency water tanker to the public dispensary because the primary supply pipeline failed completely.",
        "water",
    ),
    (
        "Low pipeline pressure prevents water from reaching overhead reservoirs across seventy residential homes in our sector.",
        "water",
    ),
    (
        "Muddy water gushing out of residential faucets has ruined our household laundry and clogged our filtration units.",
        "water",
    ),
    (
        "Taps across our street produce only a dry hissing sound whenever the morning supply valve is opened.",
        "water",
    ),
    (
        "Municipal water tankers have skipped our locality for two scheduled delivery days in a row.",
        "water",
    ),
    # --- Long Examples (15) ---
    (
        "Our entire residential colony has experienced zero municipal water flow for five straight days, forcing senior citizens to spend their pensions purchasing costly private tanker refills to meet basic hygiene needs.",
        "water",
    ),
    (
        "The underground freshwater transmission main near the central railway station burst early this morning, wasting thousands of gallons of clean drinking water while surrounding businesses have completely dry supply lines.",
        "water",
    ),
    (
        "Tap water across the eastern municipal zone has turned yellowish with an oily chemical film, making it completely unsafe for cooking, drinking, or washing infant bottles.",
        "water",
    ),
    (
        "Unless municipal engineers boost line pressure to the higher elevation streets in Fairview, dozens of households will remain without running water for a third consecutive weekend.",
        "water",
    ),
    (
        "A major fracture in the primary water distribution conduit has flooded neighboring basements with clean water while leaving surrounding commercial plazas with completely non-functional plumbing.",
        "water",
    ),
    (
        "Families with newborn infants on Willow Street cannot sterilize bottles or wash clothing because the neighborhood supply line has delivered only air hisses and brown sludge since Tuesday.",
        "water",
    ),
    (
        "Drinking water delivered to our neighborhood public supply station smells intensely of sulfur and contains dark particulate matter, rendering it completely unpotable for residents.",
        "water",
    ),
    (
        "Because water supply cuts have persisted without notice for four days, our bakery cannot mix dough or clean preparation tables, threatening our small business with complete closure.",
        "water",
    ),
    (
        "If the water board does not repair the fractured intake pipe before tomorrow morning, over five hundred school students will be left without drinking facilities or functioning restrooms.",
        "water",
    ),
    (
        "Extremely low distribution pressure across the western sector means water barely reaches ground-level faucets, leaving families unable to fill emergency storage buckets during the morning supply window.",
        "water",
    ),
    (
        "Municipal drinking water supplied to Crescent Colony yesterday contained visible rust particles and suspended dirt, prompting multiple families to report acute gastrointestinal illness among young children.",
        "water",
    ),
    (
        "When will the municipal water authority send emergency supply tankers to Sector 8, where three hundred households have had dry taps since the primary pumping station failed on Monday?",
        "water",
    ),
    (
        "A massive rupture in the treated water trunk line along Boulevard Road has submerged the sidewalk in clean water while three adjacent residential colonies suffer complete supply deprivation.",
        "water",
    ),
    (
        "Taps throughout our multi-story apartment block have run completely dry for seventy-two hours, and private water delivery services are charging exorbitant black-market prices to fill our tanks.",
        "water",
    ),
    (
        "Discolored brown tap water with an acrid metallic taste has been pouring from kitchen faucets along Hill Road, clogging fine filter membranes and ruining household appliances.",
        "water",
    ),
    # ============================================================
    # 4. SEWER CATEGORY (50 examples)
    # Focus: Blocked drains, sewage overflow, open/broken manholes, drainage backup, sewage smell, clogged pipes
    # ============================================================
    # --- Short Examples (13) ---
    ("Raw sewage overflowing from the street manhole cover.", "sewer"),
    ("Open manhole on 5th Street poses extreme danger.", "sewer"),
    ("Blocked underground sewer line backing up into basements.", "sewer"),
    ("Black wastewater bubbling out of the stormwater grate.", "sewer"),
    ("Unbearable sewer gas stench near the elementary school.", "sewer"),
    ("Clear the clogged sewage drain behind the dispensary.", "sewer"),
    ("Foul wastewater pooling across our commercial alleyway.", "sewer"),
    ("Damaged sewer concrete lid cracked open on sidewalk.", "sewer"),
    ("Gurgling sewer pipes pushing contaminated backflow into sinks.", "sewer"),
    ("Sewage sludge spilling onto the pedestrian walkway.", "sewer"),
    ("Choked municipal drain causing black foul effluent flooding.", "sewer"),
    ("Missing manhole cover near the neighborhood children's playground.", "sewer"),
    ("Toxic sewer odor leaking from collapsed underground conduit.", "sewer"),
    # --- Medium Examples (22) ---
    (
        "Because the main sewer line is choked with silt, contaminated dark wastewater is backing up into ground-floor toilets.",
        "sewer",
    ),
    (
        "A heavy cast-iron manhole cover collapsed into the sewer pit near the bazaar, leaving a deadly ten-foot drop.",
        "sewer",
    ),
    (
        "Raw municipal wastewater has been leaking continuously from a cracked underground conduit directly into the alleyway.",
        "sewer",
    ),
    (
        "When will sanitation pump trucks clear the choked underground sewer lines servicing the busy food street?",
        "sewer",
    ),
    (
        "Putrid black sludge from an overflowing sewer culvert has flooded the pedestrian entrance to the neighborhood mosque.",
        "sewer",
    ),
    (
        "If municipal maintenance does not clear the clogged sewer junction today, toxic blackwater will enter our living rooms.",
        "sewer",
    ),
    (
        "Intense hydrogen sulfide sewer odor is rising through the pavement grates, making pedestrians nauseous outside the clinic.",
        "sewer",
    ),
    (
        "Clogged wastewater channels along Market Lane have caused filthy contaminated runoff to submerge our storefront steps.",
        "sewer",
    ),
    (
        "An uncovered sewer pit outside the nursery school playground has remained exposed without safety barricades for three days.",
        "sewer",
    ),
    (
        "Grease and silt blockage in the municipal sewer main has forced raw sewage to spill over the curbside walkway.",
        "sewer",
    ),
    (
        "Black, foul-smelling sewer effluent is pooling across our driveway, preventing vehicles from entering or exiting.",
        "sewer",
    ),
    (
        "Heavy rains caused our street's sewer conduit to back up, flooding residential basements with untreated wastewater.",
        "sewer",
    ),
    (
        "A broken concrete manhole cover on 4th Avenue has left exposed rusted iron rebar sticking up dangerously.",
        "sewer",
    ),
    (
        "Sanitation crews must de-silt the choked sewage culvert along Industrial Road before toxic runoff spreads further.",
        "sewer",
    ),
    (
        "Overflowing sewage effluent from a choked roadside drain is seeping into the foundations of neighboring homes.",
        "sewer",
    ),
    (
        "Our entire commercial plaza smells like an open septic tank due to a blocked municipal sewage line.",
        "sewer",
    ),
    (
        "Raw sewage is bubbling up from an inspection chamber directly in front of the local pharmacy.",
        "sewer",
    ),
    (
        "Pedestrians are jumping over streams of contaminated black wastewater running along the sidewalk on Elm Street.",
        "sewer",
    ),
    (
        "The underground sewer junction outside block D has completely collapsed, trapping foul wastewater in the pipes.",
        "sewer",
    ),
    (
        "Choked sewer conduits on Church Lane are forcing toxic effluent into the yard of our community daycare.",
        "sewer",
    ),
    (
        "Persistent sewer gas leakage from an unsealed manhole frame is triggering headaches among residents of Maple Court.",
        "sewer",
    ),
    (
        "Unclog the primary wastewater collector line near the bus terminal to stop foul sewage from flooding the road.",
        "sewer",
    ),
    # --- Long Examples (15) ---
    (
        "Underground sewer junction on Lexington Road has completely backed up, forcing foul-smelling black wastewater to bubble up through stormwater grates and flood the ground-floor hallway of our apartment complex.",
        "sewer",
    ),
    (
        "A cracked, overflowing sewer pipe beside the public hospital boundary wall is discharging gallons of untreated sewage onto the road, creating an intolerable stench and a critical biohazard for patients.",
        "sewer",
    ),
    (
        "Over eight days, an open sewer manhole near the crowded community playground has remained completely uncovered, and young children playing soccer could easily fall into the deep toxic wastewater chamber.",
        "sewer",
    ),
    (
        "Unless vacuum suction trucks de-silt the municipal sewer culverts along Sector 9, recurring sewage overflow will continue seeping into local shop foundations and contaminating nearby soil.",
        "sewer",
    ),
    (
        "Gurgling sounds in our ground-floor drainage pipes preceded a full sewage eruption this morning, leaving our medical clinic waiting room covered in two inches of unsanitary wastewater sludge.",
        "sewer",
    ),
    (
        "The entire block around 8th Avenue smells like rotten eggs because stagnant sewage is pooling in broken underground drainage channels and overflowing past commercial food stalls.",
        "sewer",
    ),
    (
        "Pedestrians and cyclists are forced into heavy oncoming traffic because a continuous river of foul wastewater from a broken sewer main has submerged thirty meters of the sidewalk.",
        "sewer",
    ),
    (
        "Because tree roots penetrated the primary municipal sewer line on Park Avenue, wastewater cannot flow downstream and is erupting from manhole covers throughout our residential court.",
        "sewer",
    ),
    (
        "If municipal suction jetting machines are not dispatched to clean the blocked sewage line on 3rd Street, raw wastewater will continue flooding the basement storage units of ten small businesses.",
        "sewer",
    ),
    (
        "An open, fractured sewer pit outside the eye clinic has been left without warning signs or cones, creating an imminent falling hazard for elderly patients walking along the sidewalk.",
        "sewer",
    ),
    (
        "Stagnant, putrid sewage has accumulated in an open drainage trench outside our housing society, breeding swarms of mosquitoes and releasing noxious gas that causes severe nausea among residents.",
        "sewer",
    ),
    (
        "When will sewer maintenance crews arrive to pump out the blocked wastewater junction on Broad Street, where dark fecal slurry has been spilling onto the roadway for forty-eight hours?",
        "sewer",
    ),
    (
        "Heavy rains overwhelmed the clogged municipal sewer pipes on Grand Way, causing contaminated wastewater to burst through ground-level floor drains in five commercial retail shops.",
        "sewer",
    ),
    (
        "A broken concrete manhole frame on the corner of Elm and 6th has sunk below the asphalt, allowing toxic sewer stench and raw wastewater to leak into the pedestrian walking zone.",
        "sewer",
    ),
    (
        "Untreated sewage effluent escaping from a fractured underground conduit has pooled into a large fetid lagoon behind the community library, creating an urgent public health emergency.",
        "sewer",
    ),
    # ============================================================
    # 5. ELECTRICITY CATEGORY (50 examples)
    # Focus: Power outages, faulty transformers, unstable voltage, frequent load shedding, sparking wires, meter issues
    # ============================================================
    # --- Short Examples (13) ---
    ("Complete power blackout across Sector G for three hours.", "electricity"),
    (
        "Sparking overhead electrical transformer outside the shopping plaza.",
        "electricity",
    ),
    (
        "Severe voltage surges burning out household electronic appliances.",
        "electricity",
    ),
    ("Exposed dangling power cables near the bus stop.", "electricity"),
    ("Low voltage prevents water pumps from switching on.", "electricity"),
    ("Fix the buzzing utility power pole on 4th.", "electricity"),
    (
        "Frequent unannounced load shedding ruining small business operations.",
        "electricity",
    ),
    ("Electric power meter smoking on the exterior wall.", "electricity"),
    ("Repeated power tripping every ten minutes in block B.", "electricity"),
    ("Phase failure left half our apartment complex without electricity.", "electricity"),
    ("Overhead power lines snapped and resting on a car.", "electricity"),
    ("Sudden voltage drop causing computers and machinery to reboot.", "electricity"),
    ("Loud explosion heard from the municipal electrical substation.", "electricity"),
    # --- Medium Examples (22) ---
    (
        "Because of unstable high voltage yesterday evening, refrigerators and air conditioning units burned out across our building.",
        "electricity",
    ),
    (
        "The electrical transformer on Elm Street exploded with a loud bang, plunging the entire residential block into darkness.",
        "electricity",
    ),
    (
        "Live high-tension electric wires snapped in the wind and are hanging dangerously three feet above the sidewalk.",
        "electricity",
    ),
    (
        "When will the power utility dispatch technicians to restore electrical service to the south commercial zone?",
        "electricity",
    ),
    (
        "Persistent electrical phase failure in our colony has left half the homes without power for over eighteen hours.",
        "electricity",
    ),
    (
        "If power supply is not stabilized soon, dairy shops in the central market will lose thousands in spoiled inventory.",
        "electricity",
    ),
    (
        "Rapid voltage fluctuations between 140V and 280V are causing lights to strobe and frying delicate computer hardware.",
        "electricity",
    ),
    (
        "Frequent intermittent power tripping has occurred twelve times today, disrupting online examinations at the local college.",
        "electricity",
    ),
    (
        "A utility pole distribution box is emitting green sparks and heavy smoke outside the dental practice.",
        "electricity",
    ),
    (
        "Eight hours of continuous unannounced power outage has left our nursing home relying on expensive emergency generators.",
        "electricity",
    ),
    (
        "Our digital electricity meter is displaying incorrect error codes and making continuous clicking sounds.",
        "electricity",
    ),
    (
        "Unannounced load shedding during the hottest hours of the day is causing severe distress to elderly residents.",
        "electricity",
    ),
    (
        "Heavy sparks from the transformer on Oak Avenue are dropping burning embers onto parked vehicles below.",
        "electricity",
    ),
    (
        "Three-phase power supply has dropped to single-phase, disabling commercial refrigeration units at the meat market.",
        "electricity",
    ),
    (
        "Restore electricity supply to Sector 11 immediately so medical clinic cold-storage units can function.",
        "electricity",
    ),
    (
        "A snapped power cable is dangling in puddle water right outside the kindergarten entrance.",
        "electricity",
    ),
    (
        "Severe voltage drops on Cedar Lane make it impossible to operate basic household appliances.",
        "electricity",
    ),
    (
        "Our entire neighborhood has suffered four blackout cycles in a single twelve-hour period.",
        "electricity",
    ),
    (
        "Electric utility wires caught in tree branches on 9th Street are arcing and throwing bright sparks.",
        "electricity",
    ),
    (
        "Why did the electricity company cut power to our residential area without giving any advance schedule?",
        "electricity",
    ),
    (
        "A smoking electricity distribution pillar outside our apartment complex needs urgent emergency inspection.",
        "electricity",
    ),
    (
        "Sudden voltage spikes have destroyed two television sets and a microwave oven in our home.",
        "electricity",
    ),
    # --- Long Examples (15) ---
    (
        "Overhead electrical transformer mounted on pole #42 outside the government school has been buzzing loudly and spewing oil for two days, and neighborhood parents fear an imminent electrical fire or explosion.",
        "electricity",
    ),
    (
        "During five consecutive afternoons, our entire residential subdivision has experienced rolling three-hour power blackouts, leaving bedridden senior citizens without ventilation or medical oxygen concentrator power in extreme heat.",
        "electricity",
    ),
    (
        "Dangerous high-voltage electrical cables came loose during the thunderstorm and are currently draped over a metal fence adjacent to the community playground, posing an immediate electrocution hazard.",
        "electricity",
    ),
    (
        "Unless electrical crews replace the blown substation fuse servicing the industrial estate, thirty manufacturing workshops will remain entirely without operational machinery for the rest of the workweek.",
        "electricity",
    ),
    (
        "Severe single-phase electrical drops across Highland Park have rendered elevators inoperative and prevented household booster pumps from running, leaving high-rise residents stranded without power.",
        "electricity",
    ),
    (
        "Our manufacturing facility lost three expensive motor drives this morning after an extreme power surge surged through the municipal distribution feeder line without warning.",
        "electricity",
    ),
    (
        "Power cuts lasting over twelve hours every night have crippled refrigeration at the local veterinary clinic, putting sensitive vaccines and medical supplies at immediate risk.",
        "electricity",
    ),
    (
        "Because an electrical cable short-circuited inside the communal junction box on 7th Avenue, twelve residential homes have had no power supply since three o'clock yesterday afternoon.",
        "electricity",
    ),
    (
        "If power utility engineers do not replace the overloaded transformer on Willow Street, continuous voltage drops will permanently damage medical monitoring equipment in our home healthcare setup.",
        "electricity",
    ),
    (
        "An electric utility pole on Commercial Way caught fire after heavy sparks erupted from the main connection box, cutting electricity to sixty retail stores during peak shopping hours.",
        "electricity",
    ),
    (
        "Voltage fluctuating wildly between 110 volts and 290 volts has blown out light tubes and fried circuit boards in five neighboring residences on Pine Crescent.",
        "electricity",
    ),
    (
        "When will emergency electrical line crews repair the snapped power cables lying across the public sidewalk near the metro station entrance after yesterday's high winds?",
        "electricity",
    ),
    (
        "Frequent unannounced load shedding spanning eight hours daily has disrupted operations at our dialysis center, forcing staff to exhaust backup diesel generator fuel supplies.",
        "electricity",
    ),
    (
        "A loud transformer blast on Church Street knocked out electricity for the entire eastern quadrant of our colony, leaving four hundred homes in total blackout overnight.",
        "electricity",
    ),
    (
        "Persistent electrical phase failures on Orchard Road mean that while ceiling fans rotate sluggishly, water heaters and refrigerators receive insufficient voltage to operate safely.",
        "electricity",
    ),
    # ============================================================
    # 6. STREETLIGHTS CATEGORY (50 examples)
    # Focus: Broken/non-functional street lighting, dark streets, flickering lights, damaged lamp posts, no lighting on roads
    # ============================================================
    # --- Short Examples (13) ---
    ("Streetlight outside house #14 is completely burnt out.", "streetlights"),
    ("Pitch black street along Willow Avenue every night.", "streetlights"),
    (
        "Flickering lamp post creating strobe effect near crossing.",
        "streetlights",
    ),
    ("Damaged lighting pole leaning dangerously over the curb.", "streetlights"),
    ("No street illumination along the entire park perimeter.", "streetlights"),
    ("Replace the broken sodium bulb on pole 9.", "streetlights"),
    ("Seven consecutive streetlights remain dark on 5th.", "streetlights"),
    ("Exposed wiring inside the open street lamp base.", "streetlights"),
    (
        "Broken streetlight fixture hanging by a single cable.",
        "streetlights",
    ),
    ("Dark roadway along River Lane makes driving unsafe.", "streetlights"),
    ("Street lighting timer is broken, keeping lamps off at night.", "streetlights"),
    ("Shattered glass lantern on the public light pole.", "streetlights"),
    ("Non-functional streetlights outside the girls' secondary school.", "streetlights"),
    # --- Medium Examples (22) ---
    (
        "Because four consecutive streetlights on Pine Street are broken, women feel unsafe walking home from the transit station.",
        "streetlights",
    ),
    (
        "A delivery truck backed into the decorative light pole outside the public library, leaving it tilted at a 45-degree angle.",
        "streetlights",
    ),
    (
        "The entire stretch of street lighting along River Road failed three nights ago, leaving sharp roadway curves in pitch darkness.",
        "streetlights",
    ),
    (
        "When will technicians repair the solar street lamp array illuminating the community recreation center pathway?",
        "streetlights",
    ),
    (
        "Rapidly flashing LED streetlights at the intersection of Oak and Main are distracting drivers and causing severe glare.",
        "streetlights",
    ),
    (
        "If municipal lighting is not restored along the school lane, pedestrian safety after sunset will remain severely compromised.",
        "streetlights",
    ),
    (
        "Darkness on our residential street has led to two vehicle break-ins this week because the lamp post bulbs burnt out.",
        "streetlights",
    ),
    (
        "Public lamp post #18 has an open inspection panel with live wires exposed at children's eye level.",
        "streetlights",
    ),
    (
        "Overhead street lamps along the pedestrian underpass have been out of order for over six weeks.",
        "streetlights",
    ),
    (
        "Non-functional lighting along the cemetery perimeter road makes nighttime driving extremely hazardous for commuters.",
        "streetlights",
    ),
    (
        "Dark street conditions outside our housing colony gate have turned the area into an accident hotspot after dark.",
        "streetlights",
    ),
    (
        "A rusting steel streetlight pole on Maple Avenue is swaying dangerously in moderate wind gusts.",
        "streetlights",
    ),
    (
        "Replace the defunct street lamp bulbs illuminating the bus stop opposite the municipal polytechnic.",
        "streetlights",
    ),
    (
        "Every lamp post on Hillside Crescent has stayed unlit for five straight evenings, leaving residents in total darkness.",
        "streetlights",
    ),
    (
        "Flickering street lighting outside my bedroom window is causing continuous sleep disruption every night.",
        "streetlights",
    ),
    (
        "Streetlights on 8th Avenue stay illuminated throughout broad daylight but switch off completely at dusk.",
        "streetlights",
    ),
    (
        "Pedestrians are tripping over broken curbs because the street lighting on Church Road has been dead for weeks.",
        "streetlights",
    ),
    (
        "An errant car sheared off the street lamp pole at the corner of 3rd and Elm, leaving exposed wires.",
        "streetlights",
    ),
    (
        "Dim, failing streetlight fixtures along the canal walkway provide almost no illumination for evening pedestrians.",
        "streetlights",
    ),
    (
        "Restore functioning streetlights along Market Street so evening shoppers and vendors can conduct business safely.",
        "streetlights",
    ),
    (
        "Four street lamp posts in front of the maternity hospital have been non-functional since last Friday.",
        "streetlights",
    ),
    (
        "Complete darkness along the residential bypass road is encouraging unlawful anti-social activities after midnight.",
        "streetlights",
    ),
    # --- Long Examples (15) ---
    (
        "Every single overhead street lamp along the two-kilometer stretch of bypass road between the industrial zone and town has been completely non-functional for three weeks, causing multiple near-miss pedestrian accidents in the dark.",
        "streetlights",
    ),
    (
        "The steel light pole outside the senior living complex was struck by a vehicle last weekend and is now held up only by overhead cables, threatening to collapse onto the pedestrian sidewalk.",
        "streetlights",
    ),
    (
        "Nighttime visibility on Crescent Avenue has dropped to zero because all eight municipal streetlights have suffered burnt out bulbs, forcing residents to walk with smartphone flashlights to avoid tripping on broken curbs.",
        "streetlights",
    ),
    (
        "Unless maintenance technicians replace the non-operational halogen streetlights near the central railway footbridge, commuters returning on late-night trains will continue facing serious safety risks in total darkness.",
        "streetlights",
    ),
    (
        "A malfunctioning photocell sensor on our neighborhood street lighting circuit causes all fourteen lamps to stay illuminated during daylight hours while remaining completely switched off at night.",
        "streetlights",
    ),
    (
        "Outdoor lamp post illuminating the municipal dispensary ambulance bay has been out of service for a month, making emergency night patient transfers difficult and hazardous for paramedics.",
        "streetlights",
    ),
    (
        "Erratic flickering from the high-pressure sodium street lamp right outside my second-floor bedroom window has made sleeping impossible for my elderly parents for nearly ten days.",
        "streetlights",
    ),
    (
        "Because street lighting along Grand Boulevard failed completely on Monday, the pedestrian crosswalk outside the elementary school is shrouded in blackness, endangering children attending after-school programs.",
        "streetlights",
    ),
    (
        "If municipal electrical teams do not repair the damaged underground cabling feeding the streetlights on 11th Street, the entire commercial market block will remain dark and vulnerable to nighttime burglaries.",
        "streetlights",
    ),
    (
        "Five broken streetlights along the park walkway have left the jogging track completely pitch black, forcing evening runners and dog walkers to abandon the facility after sunset.",
        "streetlights",
    ),
    (
        "A corroded metal streetlight pole on the corner of 6th Avenue has developed a severe structural lean toward oncoming traffic, risking a fatal collision if high winds topple it.",
        "streetlights",
    ),
    (
        "When will public works replace the shattered LED streetlight heads on Western Way, where vandals threw stones and broke six light fixtures in a single night?",
        "streetlights",
    ),
    (
        "Complete failure of street lighting across Sector 14 has made navigating residential driveways hazardous, with several neighbors scraping their cars against hidden curb barriers in the dark.",
        "streetlights",
    ),
    (
        "Our residential association has repeatedly reported the dead streetlight outside building 8, yet municipal maintenance has left the entire entranceway unlit for twenty-two days.",
        "streetlights",
    ),
    (
        "Burnt out bulbs in all three streetlights surrounding the community center parking lot have created a dangerous blind spot where multiple vehicle break-ins have occurred this month.",
        "streetlights",
    ),
    # ============================================================
    # 7. ILLEGAL DUMPING CATEGORY (50 examples)
    # Focus: Unauthorized waste dumping action (construction debris, rubble, trash dumped on vacant lots/canals by trucks or individuals)
    # ============================================================
    # --- Short Examples (13) ---
    ("Dump truck unloaded construction rubble on vacant plot.", "illegal_dumping"),
    (
        "Midnight fly-tipping of discarded drywall along canal bank.",
        "illegal_dumping",
    ),
    ("Unidentified pickup dumped old tires in the woods.", "illegal_dumping"),
    (
        "Contractor dumping broken concrete slabs beside the road.",
        "illegal_dumping",
    ),
    ("Illegal disposal of commercial demolition waste in forest.", "illegal_dumping"),
    ("Catch the violators dumping chemical drums on farmland.", "illegal_dumping"),
    ("Piles of dumped roofing tiles on empty corner lot.", "illegal_dumping"),
    (
        "Someone dumped eight discarded mattresses in drainage ditch.",
        "illegal_dumping",
    ),
    ("Fly-tippers left asbestos insulation sheets along the nature trail.", "illegal_dumping"),
    ("Rogue builder dumped asphalt shavings into public wetland.", "illegal_dumping"),
    ("Commercial truck dumping industrial scrap metal behind the cemetery.", "illegal_dumping"),
    ("Stop vehicles from dumping excavated soil on our lane.", "illegal_dumping"),
    ("Unauthorized dumping of broken porcelain sinks on parkway.", "illegal_dumping"),
    # --- Medium Examples (22) ---
    (
        "Last night, an unmarked flatbed truck dumped three tons of demolished masonry and ceramic debris onto the empty corner plot.",
        "illegal_dumping",
    ),
    (
        "Commercial roofers are illegally abandoning asphalt shingles and fiberglass insulation bags in the greenbelt corridor behind our neighborhood.",
        "illegal_dumping",
    ),
    (
        "Because unscrupulous contractors repeatedly dump excavated dirt along the stream embankment, natural rainwater runoff is getting severely obstructed.",
        "illegal_dumping",
    ),
    (
        "A white van was spotted unloading broken furniture, old television sets, and paint cans into the nature reserve.",
        "illegal_dumping",
    ),
    (
        "When will enforcement officers install surveillance cameras to prevent repeat offenders from dumping industrial scrap on our lane?",
        "illegal_dumping",
    ),
    (
        "If the city does not penalize perpetrators of midnight fly-tipping along Railroad Avenue, the vacant lot will become an unauthorized landfill.",
        "illegal_dumping",
    ),
    (
        "Piles of hazardous drywall, fiberglass, and chemical containers were dumped overnight near the agricultural irrigation canal.",
        "illegal_dumping",
    ),
    (
        "Rogue builders have repeatedly unloaded truckloads of mortar, bricks, and broken tiles directly onto the public wetland reserve.",
        "illegal_dumping",
    ),
    (
        "An auto body shop has been illicitly dumping scrap bumpers and used oil barrels onto the vacant field.",
        "illegal_dumping",
    ),
    (
        "Fly-tippers dumped over forty worn automobile tires into the dry culvert beside Highway 10 overnight.",
        "illegal_dumping",
    ),
    (
        "A private landscaping crew dumped truckloads of tree trunks and yard waste onto the abandoned municipal plot.",
        "illegal_dumping",
    ),
    (
        "Unknown culprits dropped a heap of demolished concrete pillars along the quiet residential access road at 3:00 AM.",
        "illegal_dumping",
    ),
    (
        "Illegal disposal of commercial kitchen appliances on the riverbank is causing severe environmental contamination.",
        "illegal_dumping",
    ),
    (
        "Unlicensed renovation workers dumped piles of cracked drywall and broken tiles directly beside the public school fence.",
        "illegal_dumping",
    ),
    (
        "Enforce strict penalties against the commercial trucks dumping concrete slurry into the open storm channel.",
        "illegal_dumping",
    ),
    (
        "A flatbed lorry was caught fly-tipping worn truck tires and plastic crates into the forest reserve.",
        "illegal_dumping",
    ),
    (
        "Someone dumped five large containers of used motor oil on the vacant land opposite the community clinic.",
        "illegal_dumping",
    ),
    (
        "Contractors are avoiding municipal tipping fees by dumping heavy demolition rubble in our quiet residential cul-de-sac.",
        "illegal_dumping",
    ),
    (
        "Midnight dumping of broken glass and construction timber on the open field creates a severe hazard for children.",
        "illegal_dumping",
    ),
    (
        "A pickup truck driver dumped heaps of commercial plumbing pipes into the ditch along Country Road.",
        "illegal_dumping",
    ),
    (
        "Unauthorized dumping of chemical paint residue in the vacant industrial lot is releasing toxic noxious fumes.",
        "illegal_dumping",
    ),
    (
        "Catch the illegal dumpers who discarded three truckloads of excavated clay onto our neighborhood walking path.",
        "illegal_dumping",
    ),
    # --- Long Examples (15) ---
    (
        "At approximately 2:00 AM last night, a large commercial tipper truck illegally dumped ten cubic yards of concrete slabs and twisted rebar onto the public green space adjacent to the municipal park, completely blocking the foot trail.",
        "illegal_dumping",
    ),
    (
        "Rogue construction contractors have turned the abandoned parcel behind our housing community into an illicit dumping ground, repeatedly depositing truckloads of toxic drywall dust, broken brickwork, and asphalt shavings under cover of darkness.",
        "illegal_dumping",
    ),
    (
        "A landscape maintenance crew was witnessed unloading dozens of plastic bags filled with tree cuttings and commercial chemical containers directly into the protected wildlife ditch rather than using the certified waste facility.",
        "illegal_dumping",
    ),
    (
        "Unless municipal authorities impound vehicles caught dumping construction rubble along Meadow Lane, private builders will continue avoiding landfill fees by turning our quiet rural access road into a debris dump.",
        "illegal_dumping",
    ),
    (
        "Surveillance footage from our warehouse captured an unmarked flatbed unloading twenty industrial plastic drums containing unknown chemical sludge into the empty field behind the train tracks yesterday evening.",
        "illegal_dumping",
    ),
    (
        "Unlicensed demolition crews have dumped mountains of jagged masonry and shattered window glass along the riverbank path, creating an extreme laceration hazard for local fishermen and joggers.",
        "illegal_dumping",
    ),
    (
        "Repeat fly-tipping behind the industrial park has left dozens of discarded automotive batteries and engine blocks leaking corrosive fluids onto the unpaved access lane.",
        "illegal_dumping",
    ),
    (
        "Because the vacant municipal lot on 9th Street has no perimeter fencing, dishonest contractors are constantly dumping commercial roofing tar, fiberglass sheets, and concrete blocks during late night hours.",
        "illegal_dumping",
    ),
    (
        "If the municipal council does not prosecute the transport company dumping commercial packing crates and styrofoam heaps along the bypass canal, the entire drainage basin will choke before autumn.",
        "illegal_dumping",
    ),
    (
        "An unidentified commercial truck dumped three tons of crushed masonry and broken ceramic floor tiles across the horse riding trail, forcing local equestrian clubs to halt operations.",
        "illegal_dumping",
    ),
    (
        "Fly-tippers exploited the lack of lighting on Timber Road to dump over sixty discarded commercial truck tires into the creek bed, creating an immediate environmental hazard for aquatic wildlife.",
        "illegal_dumping",
    ),
    (
        "When will municipal code enforcement investigate the illegal dumping of lead paint scraps and demolished ceiling tiles on the vacant plot directly across from the pediatric health center?",
        "illegal_dumping",
    ),
    (
        "A demolition company working on downtown renovations has been illegally unloading trailer-loads of crushed concrete and mortar fragments onto the agricultural verge beside Farm Road 12.",
        "illegal_dumping",
    ),
    (
        "Contractors renovating the commercial mall dumped ten cubic meters of plaster debris and broken glass fixtures in the wooded nature buffer behind our residential neighborhood.",
        "illegal_dumping",
    ),
    (
        "Security cameras recorded a flatbed truck dumping hazardous asbestos cladding sheets in the ditch along North Parkway, requiring immediate hazardous materials containment and cleanup by the city.",
        "illegal_dumping",
    ),
    # ============================================================
    # 8. CLEANLINESS CATEGORY (50 examples)
    # Focus: General dirtiness/unkempt state of public spaces (parks, sidewalks, public restrooms, markets, plazas)
    # ============================================================
    # --- Short Examples (13) ---
    ("Public restrooms at the central terminal are filthy.", "cleanliness"),
    (
        "Unsanitary conditions throughout the municipal vegetable bazaar.",
        "cleanliness",
    ),
    ("City park lawn covered in scattered snack wrappers.", "cleanliness"),
    ("Disgusting grime and stains across pedestrian subway steps.", "cleanliness"),
    (
        "Filthy conditions inside the public botanical garden pavilion.",
        "cleanliness",
    ),
    ("Sanitize the grimy municipal bus shelter benches.", "cleanliness"),
    ("Litter-strewn pedestrian walkway along the river promenade.", "cleanliness"),
    ("Greasy, dirty public plaza pavement needs pressure washing.", "cleanliness"),
    ("Public park fountain is filled with green slime.", "cleanliness"),
    ("Deplorable hygiene inside the civic center public washrooms.", "cleanliness"),
    ("Sidewalks along the market street are stained and unwashed.", "cleanliness"),
    ("Grimy, sticky floor tiles inside the municipal transit hall.", "cleanliness"),
    ("General state of neglect in the children's public playground.", "cleanliness"),
    # --- Medium Examples (22) ---
    (
        "The municipal park is in an unkempt state with cigarette butts, food wrappers, and plastic cups littering every lawn area.",
        "cleanliness",
    ),
    (
        "Public toilets adjacent to the community center are utterly foul, lacking hand soap, paper, or any semblance of basic hygiene.",
        "cleanliness",
    ),
    (
        "Because the town square has not been swept in weeks, dust and loose street debris blow into open-air restaurant seating.",
        "cleanliness",
    ),
    (
        "Pedestrian walking paths through Memorial Park are neglected, overgrown with weeds, and covered in dried bird droppings.",
        "cleanliness",
    ),
    (
        "When will sanitation crews deep-clean and disinfect the sticky, foul-smelling platforms at the central bus transit terminal?",
        "cleanliness",
    ),
    (
        "If public restrooms in the civic building are not scrubbed regularly, they will continue posing a severe health hazard to visitors.",
        "cleanliness",
    ),
    (
        "The historic clock tower plaza has become unhygienic with greasy stains, food residue, and discarded plastic cups covering the brickwork.",
        "cleanliness",
    ),
    (
        "Spit stains and sticky grime have accumulated across the tiled walls and floors of the downtown pedestrian underpass.",
        "cleanliness",
    ),
    (
        "Children cannot play on the public playground slides because the surrounding sandbox is littered with broken glass and wrappers.",
        "cleanliness",
    ),
    (
        "General cleanliness throughout the government hospital waiting area is deplorable, with unwashed floors and dust-covered seating.",
        "cleanliness",
    ),
    (
        "The public library courtyard is covered in fallen rotting leaves, discarded beverage cans, and bird droppings.",
        "cleanliness",
    ),
    (
        "Filthy, grease-stained walkways outside the municipal seafood market are creating a slippery slip-and-fall hazard for shoppers.",
        "cleanliness",
    ),
    (
        "Our municipal rose garden has fallen into severe disrepair, with weeds choking flowerbeds and windblown plastic littering the grass.",
        "cleanliness",
    ),
    (
        "Sanitize and scrub the public washroom cubicles at the beach pavilion to eliminate intolerable odors.",
        "cleanliness",
    ),
    (
        "Sidewalks surrounding the central train station are coated in dark gum stains, spilled drinks, and general grime.",
        "cleanliness",
    ),
    (
        "The entire civic amphitheater is covered in discarded wrappers, peanut shells, and sticky liquid stains after weekend events.",
        "cleanliness",
    ),
    (
        "Public benches in front of the municipal museum are coated with grime and soot, making it impossible to sit down.",
        "cleanliness",
    ),
    (
        "Unwashed public footpaths through the old bazaar are littered with trampled food scraps and dirty plastic bags.",
        "cleanliness",
    ),
    (
        "Why are municipal sweepers not cleaning the perimeter sidewalks around the central sports complex?",
        "cleanliness",
    ),
    (
        "The pedestrian bridge over Highway 4 is disgusting, with stained railings, scattered litter, and uncleaned debris along steps.",
        "cleanliness",
    ),
    (
        "Filthy conditions inside the municipal recreation hall are discouraging families from utilizing public community facilities.",
        "cleanliness",
    ),
    (
        "Power-wash the grimy, oil-stained pavement throughout the downtown pedestrian shopping promenade.",
        "cleanliness",
    ),
    # --- Long Examples (15) ---
    (
        "The public promenade along the beachfront is in an unacceptable state of neglect, with sticky food spills, hundreds of cigarette butts, and windblown litter scattered across benches where tourists and families attempt to sit.",
        "cleanliness",
    ),
    (
        "Public restrooms near the downtown bazaar have reached a shocking state of unhygienic filth, with overflowing sanitary bins, clogged washbasins, and unwashed porcelain bowls making them completely unusable for visitors.",
        "cleanliness",
    ),
    (
        "Our municipal botanical garden paths have become severely degraded and littered with beverage cans, faded food packets, and dried animal waste because groundskeeping staff have not conducted regular sweepings this season.",
        "cleanliness",
    ),
    (
        "Unless maintenance personnel thoroughly power-wash and disinfect the public transit pavilion on 2nd Avenue, the accumulated grime, food grease, and pigeon droppings will continue degrading the city center's public image.",
        "cleanliness",
    ),
    (
        "The open-air amphitheater in the civic park is surrounded by filthy seating tiers covered in dried mud, spilled drinks, and windblown debris, making it unsuitable for community weekend cultural performances.",
        "cleanliness",
    ),
    (
        "Market vendors and shoppers at the weekly farmer's square are forced to navigate greasy, slippery pavement coated in squashed fruit residue and general municipal grime that hasn't been washed in weeks.",
        "cleanliness",
    ),
    (
        "Underground pedestrian passageway connecting the train station to Main Street has become utterly unkempt, smelling of urine and featuring stained walls and discarded food containers that haven't been cleaned in months.",
        "cleanliness",
    ),
    (
        "Because municipal sweepers have neglected the waterfront boardwalk for over a month, decomposing algae, dried beverage stains, and plastic straw litter have turned the tourist area into an uninviting eyesore.",
        "cleanliness",
    ),
    (
        "If the city does not implement daily janitorial maintenance for the public rest facilities at Central Park, the accumulated filth and unsanitary conditions will lead to serious bacterial contamination risks for park visitors.",
        "cleanliness",
    ),
    (
        "The communal plaza outside the municipal art gallery is marred by stubborn chewing gum deposits, grease trails from street food carts, and dusty windblown debris that gives the district an abandoned feel.",
        "cleanliness",
    ),
    (
        "When will the sanitation board deploy power-washing crews to cleanse the grime-encrusted subway entrances on 4th Street, where sticky residues on handrails make commuters reluctant to touch support bars?",
        "cleanliness",
    ),
    (
        "Public seating areas along the civic canal pathway are covered in dried bird feces, moss, and decaying leaf litter, preventing elderly citizens from resting comfortably during their daily morning walks.",
        "cleanliness",
    ),
    (
        "The historic municipal marketplace pavilion is plagued by unwashed stone floors, grease accumulations around vendor stalls, and scattered vegetable waste that produce a constant foul, sour odor throughout the hall.",
        "cleanliness",
    ),
    (
        "Filthy conditions across the public playground on Elm Street, including rusted swings covered in grime and sandpits filled with snack wrappers, make the facility completely uninviting for neighborhood families.",
        "cleanliness",
    ),
    (
        "Our city center pedestrian zone looks shameful due to neglected street sweeping, with piles of windblown flyers, discarded coffee cups, and grime clinging to decorative planters along the entire avenue.",
        "cleanliness",
    ),
    # ============================================================
    # 9. OTHER CATEGORY (50 examples)
    # Focus: Stray animals, broken traffic signals, noise complaints, damaged public benches, illegal parking, fallen trees, unauthorized construction
    # ============================================================
    # --- Short Examples (13) ---
    ("Pack of aggressive stray dogs chasing morning joggers.", "other"),
    ("Broken traffic signal blinking red on all sides.", "other"),
    ("Fallen tree branch crushing the park bench.", "other"),
    ("Illegal commercial parking blocking the fire hydrant access.", "other"),
    ("Deafening construction noise echoing throughout midnight hours.", "other"),
    ("Remove the abandoned rusted vehicle on Elm.", "other"),
    ("Vandalized public bus shelter with smashed glass panels.", "other"),
    (
        "Unauthorized building extension encroaching onto the public footpath.",
        "other",
    ),
    ("Stray cow wandering across the highway causing traffic jam.", "other"),
    ("Loud industrial machinery operating without municipal sound permits.", "other"),
    ("Overgrown tree branches completely obscuring the stop sign.", "other"),
    ("Damaged public playground swing set with broken chains.", "other"),
    ("Unauthorized billboard erected without municipal zoning approval.", "other"),
    # --- Medium Examples (22) ---
    (
        "An aggressive stray bull wandering through the central marketplace is knocking over vendor stalls and endangering pedestrians.",
        "other",
    ),
    (
        "Traffic lights at the busy intersection of 5th Avenue and Broad Street are completely blank, causing severe vehicular gridlock.",
        "other",
    ),
    (
        "A large oak limb snapped during yesterday's gale and is currently resting across both driving lanes on Lincoln Way.",
        "other",
    ),
    (
        "Delivery vans have illegally parked along the bike lane outside the shopping arcade, forcing cyclists into high-speed traffic.",
        "other",
    ),
    (
        "When will code enforcement halt the illegal second-story concrete construction operating without municipal permits on Plot 45?",
        "other",
    ),
    (
        "Loud industrial generators operating behind the commercial warehouse are violating nighttime municipal noise ordinances.",
        "other",
    ),
    (
        "Vandals smashed three public seating benches and spray-painted graffiti across the war memorial in the town square.",
        "other",
    ),
    (
        "A swarm of wild bees has built a massive nest inside the children's jungle gym at Fairview Park.",
        "other",
    ),
    (
        "Overgrown wild tree branches are completely obstructing the stop sign at the corner of 8th and Elm.",
        "other",
    ),
    (
        "An unlicensed outdoor night club has been blasting amplified music past 2:00 AM, disturbing our entire residential neighborhood.",
        "other",
    ),
    (
        "A pack of feral dogs has established territory near the bus depot, barking aggressively at commuters every morning.",
        "other",
    ),
    (
        "Vehicles parked illegally across both sides of narrow Church Lane prevent emergency ambulances from accessing residential houses.",
        "other",
    ),
    (
        "A rotted pine tree on municipal property is leaning precariously over our roof, threatening to fall during high winds.",
        "other",
    ),
    (
        "Traffic signals at the crossroads of Pine and Grand are frozen on green in all directions, causing extreme crash hazards.",
        "other",
    ),
    (
        "Building contractors on 6th Avenue are operating heavy jackhammers at 3:00 AM in violation of city noise regulations.",
        "other",
    ),
    (
        "Remove the abandoned station wagon with broken windows that has occupied a public parking bay for six months.",
        "other",
    ),
    (
        "Unauthorized concrete pillars erected by a private shopkeeper are encroaching five feet onto the public sidewalk.",
        "other",
    ),
    (
        "Aggressive stray monkeys in the public park are snatching food from visitors and scratching children.",
        "other",
    ),
    (
        "A fallen telephone pole is blocking vehicle entry into our residential court following yesterday's thunderstorm.",
        "other",
    ),
    (
        "Broken pedestrian crossing button at the school signal fails to trigger the walk phase for waiting students.",
        "other",
    ),
    (
        "Illegal commercial car washing operations on the sidewalk are causing water to flood neighbor driveways.",
        "other",
    ),
    (
        "Vandalism has left the public park exercise equipment broken, with loose bolts creating dangerous pinch points.",
        "other",
    ),
    # --- Long Examples (15) ---
    (
        "Electronic pedestrian crossing signals at the school crosswalk on Grand Boulevard have malfunctioned, displaying walk and don't-walk lights simultaneously and confusing young students trying to cross safely during morning peak hours.",
        "other",
    ),
    (
        "A pack of seven unvaccinated stray dogs has established territory around the community hospital entrance, barking aggressively and biting at the heels of patients and nurses arriving for night shifts.",
        "other",
    ),
    (
        "An immense rotting elm tree on the municipal parkway has developed a severe structural lean toward overhead cables, and neighbors fear the next heavy windstorm will bring it crashing down onto passing vehicles.",
        "other",
    ),
    (
        "Unless traffic wardens issue citations for the dozen commercial trucks permanently parked illegally along the narrow residential shoulder of Church Street, emergency fire vehicles will remain unable to pass through in a crisis.",
        "other",
    ),
    (
        "Unauthorized building contractors on 14th Street have erected steel scaffolding directly across the public sidewalk without safety netting, dropping brick dust and scaffolding clamps onto passing pedestrians.",
        "other",
    ),
    (
        "Nightly illegal drag racing along the open bypass between midnight and 3:00 AM generates extreme exhaust noise and endangers local residents living in the adjacent apartment developments.",
        "other",
    ),
    (
        "A concrete boundary wall belonging to the abandoned municipal warehouse collapsed outward onto the sidewalk, leaving heavy rubble blocking wheelchair access.",
        "other",
    ),
    (
        "Because an illegal auto repair garage on Oak Avenue operates without permits, mechanics test loud engines and spray volatile paint fumes into the air throughout late evening hours.",
        "other",
    ),
    (
        "If municipal animal control officers do not capture the aggressive stray bull roaming the crowded bazaar, someone will suffer severe goring injuries near the vegetable stalls.",
        "other",
    ),
    (
        "A massive dead maple tree limb snapped during yesterday's storm and currently rests across two parked vehicles on Maple Court, crushing one roof and blocking the exit lane.",
        "other",
    ),
    (
        "Vandals dismantled the protective fencing surrounding the public duck pond, allowing young toddlers to wander dangerously close to steep, slippery water embankments.",
        "other",
    ),
    (
        "When will the municipal transport division repair the completely darkened traffic signal heads at the five-way intersection near the metro station, where near-collisions occur hourly?",
        "other",
    ),
    (
        "Persistent high-decibel exhaust fan noise from the industrial bakery behind our residential terrace exceeds permissible municipal decibel limits and prevents families from sleeping.",
        "other",
    ),
    (
        "Commercial tour buses are parking illegally in designated handicap spaces outside the municipal museum, forcing disabled visitors to disembark in active traffic lanes.",
        "other",
    ),
    (
        "An unauthorized mobile vendor has set up a massive steel food stall directly on the sidewalk corner of 10th and Pine, forcing schoolchildren to step into moving vehicular traffic.",
        "other",
    ),
]