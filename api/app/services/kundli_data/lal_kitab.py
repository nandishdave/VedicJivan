"""Lal Kitab remedy + interpretation data.

Split out of the former 1895-line kundli_data.py god-module (data only).
Re-exported via kundli_data/__init__.py so imports are unchanged."""



# ── LAL KITAB PREDICTIONS (9 planets × 12 houses = 108 entries) ────────────
# Lal Kitab is a 19th–20th century Indian astrological tradition (originally
# Urdu/Punjabi, attributed to Pandit Roop Chand Joshi), distinct from
# classical Parashari Vedic astrology. It uses simplified rules and offers
# very specific physical remedies. Lookup:
#   LAL_KITAB_DATA[planet_name][house_number] → {"prediction": str, "remedies": list[str]}

LAL_KITAB_DATA = {
    "Sun": {
        1: {
            "prediction": "The Sun in its pukka ghar grants the native a commanding personality, bright complexion, and natural authority over others. The father will be prosperous and respected, and the native himself will rise to a position of recognition through honest effort. Health will generally be robust, though tendencies toward eye trouble, headaches, and high blood pressure exist after middle age. Government favour and paternal blessings come easily, but arrogance can spoil ripening fortune. Marriage may be slightly delayed, and the spouse should be treated with restraint to preserve domestic peace.",
            "remedies": [
                "Donate jaggery and wheat to a temple every Sunday before sunrise.",
                "Offer water mixed with red flowers to the rising Sun for 43 consecutive days.",
                "Place a square piece of gold or copper in the family safe and never remove it.",
                "Avoid accepting clothes or articles in copper colour as gifts from in-laws.",
            ],
        },
        2: {
            "prediction": "The Sun in the second house gives a sharp tongue and a tendency to speak harshly, which often damages family wealth and relations. The native will earn through government, administration, or family business, but accumulated savings tend to dissolve unless guarded carefully. Paternal property may bring litigation, and the relationship with maternal relatives often suffers. Eyesight may weaken and dental problems are likely after the age of thirty. Despite frequent income, expenses on relatives, ceremonies, and ego-driven displays keep the bank balance modest until later years.",
            "remedies": [
                "Drink water from a silver glass each morning for forty days.",
                "Donate red lentils and a copper coin to a temple priest on any Sunday.",
                "Avoid speaking ill of the father or paternal elders even in jest.",
                "Place a small piece of gold in honey and keep it in your worship room.",
            ],
        },
        3: {
            "prediction": "Sun in the third house bestows tremendous courage, initiative, and writing or oratorical ability. The native succeeds through self-effort, short journeys, and sibling cooperation, often becoming the de facto head of the family before age thirty. Younger brothers may face ill health or separation, and at times the native rises only after a sibling's setback. Paternal property usually multiplies, and government dealings turn favourable. Stomach disorders, particularly acidity and bile, are common. Restless ambition can lead to rash decisions, so consultation with elders before major moves is strongly advised.",
            "remedies": [
                "Offer raw almonds in a temple every Sunday and bring half home to consume.",
                "Keep a square piece of silver in your wallet at all times.",
                "Never sleep in a room facing south; align the head toward the east.",
                "Distribute sweets to younger children of the family on every birthday.",
            ],
        },
        4: {
            "prediction": "The Sun in the fourth house creates a hardworking but emotionally restless native whose mother's health remains a recurring concern. Domestic peace is disturbed by the native's pride, and properties acquired in youth may be lost or sold under pressure. Government service or work connected to land, mines, or fuel can bring steady income. Heart, chest, and circulation issues may surface in middle age. Children of the native will, in turn, do well, often surpassing the father in stature. Hospitality should be controlled, as guests sometimes overstay and drain resources.",
            "remedies": [
                "Place a copper vessel filled with Ganga jal in the north-east corner of the home.",
                "Donate wheat and jaggery to a cow keeper on every full moon.",
                "Serve your mother with your own hands at least one meal each Sunday.",
                "Bury a piece of unrefined copper under the threshold of the main door.",
            ],
        },
        5: {
            "prediction": "Sun in the fifth house favours intelligence, scholarship, and authority over subordinates, but creates difficulty regarding sons. The first male child may face health issues or delayed birth, and conflict with children appears once they reach adulthood. Speculative gains are unreliable; steady professional income from teaching, administration, or advisory roles serves the native far better. The father lives long and prospers. Stomach inflammation and weak digestion may trouble the native. Devotional inclination grows with age, and pilgrimage in the late forties brings noticeable improvement to family circumstances.",
            "remedies": [
                "Worship Lord Vishnu and recite the Aditya Hridaya Stotra every Sunday morning.",
                "Donate raw cotton and wheat to a poor Brahmin on Thursdays.",
                "Avoid keeping idle copper utensils in the kitchen for long periods.",
                "Offer water sweetened with jaggery at the roots of a peepal tree on Sundays.",
            ],
        },
        6: {
            "prediction": "The Sun in the sixth house defeats enemies, brings success in litigation, and grants service-class income with steady promotion. Maternal uncles either help significantly or oppose openly; there is rarely a middle ground. The native is sharp-tempered and tends to make hidden enemies through frank speech. Health concerns include skin trouble, urinary issues, and inflammations after the age of forty-eight. Sons born to the native are healthy and bring honour. Animals kept at home, especially cats or dogs, may suffer or die early, indicating the strength of the placement.",
            "remedies": [
                "Feed boiled rice mixed with jaggery to a black cow every Sunday for eleven weeks.",
                "Place a small copper pyramid on your office desk facing east.",
                "Never accept used clothing from a sister or maternal aunt.",
                "Donate red sandalwood at a Hanuman temple on any Tuesday.",
            ],
        },
        7: {
            "prediction": "Sun in the seventh house creates an ego-driven marriage where dominance and pride from one partner unsettles the home. Business partnerships rarely flourish; the native does best working alone or as the recognised head. Government dealings and foreign correspondence yield gains, but trips taken for trade may suffer reversals. Health of the spouse remains average, and a delay in marriage is common. The father may pass through difficult financial times around the native's wedding. Sweet speech and patience after marriage protect what destiny otherwise threatens to disturb.",
            "remedies": [
                "Throw a copper coin into a flowing river on the day of marriage anniversary.",
                "Avoid starting any new business venture between noon and three in the afternoon.",
                "Distribute wheat flour to a temple kitchen on every Sunday for forty-three weeks.",
                "Touch the feet of the spouse's parents at least once a year as a gesture of respect.",
            ],
        },
        8: {
            "prediction": "The Sun in the eighth house weakens vitality and brings unexpected difficulties in middle age. The father's longevity is uncertain, and inheritance, when it comes, may be entangled in disputes. The native's eyesight deteriorates earlier than expected and chronic stomach trouble is common. Career rises through long, slow effort rather than quick promotion, and government jobs are subject to transfer or demotion. However, occult, research, and surgical fields are highly favourable. Saving discipline, regular health checks, and avoidance of speculation will preserve both wellbeing and family wealth.",
            "remedies": [
                "Bury a copper coin wrapped in red cloth at the cremation ground after a relative's funeral.",
                "Drink water only from an earthen pot for forty consecutive days.",
                "Light a mustard oil lamp before a Bhairava idol every Saturday evening.",
                "Avoid working in any government job related to fire, weapons, or chemicals.",
            ],
        },
        9: {
            "prediction": "Sun in the ninth house produces a fortunate, religious, and law-abiding native blessed by the father's good karma. Education proceeds smoothly, and travel for studies or work brings advancement. The native often inherits land or a respected family name and is recognised in his community for fairness. Sons born will be virtuous, though only after some delay. Pilgrimages and donations performed with sincerity multiply blessings significantly. The chief warning is against pride in religious or moral matters, which can alienate friends and create silent jealousy among colleagues.",
            "remedies": [
                "Offer water to the rising Sun from a copper vessel every morning.",
                "Donate gold or yellow cloth at a temple of Lord Vishnu on Thursdays.",
                "Plant a peepal tree and water it regularly until it stands on its own.",
                "Touch the feet of the father every morning before leaving the house.",
            ],
        },
        10: {
            "prediction": "The Sun in the tenth house grants high office, executive power, and recognition in government or large institutions. The native rises by sheer ability and earns through legitimate means, often becoming the family's main earner before the age of thirty-two. The father may either be very accomplished or completely absent in influence. Health issues centre on the heart, blood pressure, and overwork. Subordinates respect but secretly resent the native's directness. Charitable deeds done quietly preserve the position; ostentatious displays attract obstacles from rivals and superiors alike.",
            "remedies": [
                "Place a copper Sun yantra at the workplace facing east.",
                "Donate jaggery, red sandalwood, and a copper coin at a Sun temple every Sunday.",
                "Never sit on a higher seat than your father at any family gathering.",
                "Offer a portion of every promotion bonus to a charitable kitchen.",
            ],
        },
        11: {
            "prediction": "Sun in the eleventh house promises steady income, powerful friends, and fulfilment of ambitions through influential contacts. The native gains through government, elders, or senior officials and accumulates assets steadily after the age of twenty-eight. Elder siblings prosper and lend support during difficult phases. Eye and ear troubles may appear after fifty. Sons may be few in number, but they will be capable. The native should beware of borrowing from or lending to friends in authority, as such transactions strain the most valuable relationships and erode hard-won reputation.",
            "remedies": [
                "Donate wheat and jaggery to a working-class labourer every Sunday.",
                "Keep a small piece of gold or copper in the savings cupboard at all times.",
                "Avoid gifting copper or red articles to elder brothers or paternal uncles.",
                "Offer water to the Sun while standing barefoot on bare earth once a week.",
            ],
        },
        12: {
            "prediction": "The Sun in the twelfth house often takes the native far from his birthplace and creates expenses related to the father, government, or charitable causes. Sleep is light, eyes weaken early, and hidden adversaries cause occasional setbacks. Foreign residence, work in remote areas, or service in confidential departments suits this placement well. The father may live separately or fall ill in the native's youth. Spiritual inclinations deepen with age, and donations made anonymously yield far greater results than public charity. Excessive ego ruins everything that destiny tries to give.",
            "remedies": [
                "Donate a copper vessel filled with wheat to a temple before any long journey.",
                "Avoid sleeping with the head facing west; align it toward east instead.",
                "Light a ghee lamp at home in the south-east corner every Sunday evening.",
                "Bury a small piece of gold under a peepal tree if eye trouble appears.",
            ],
        },
    },
    "Moon": {
        1: {
            "prediction": "The Moon in the first house produces a soft-hearted, imaginative, and emotionally sensitive native whose face shows every passing mood. The mother is long-lived and influential, and her blessings prove decisive at every turning point of life. Wealth comes through liquid trades, dairy, travel, or service to women and the public. Health concerns include cold, cough, and emotional anxiety; mental peace fluctuates with the lunar phases. The native attracts public goodwill and benefits greatly from work near rivers, lakes, or seas. Hasty decisions made during low moods always disappoint later.",
            "remedies": [
                "Offer milk and water to a Shivling every Monday morning before sunrise.",
                "Always carry a small silver coin in the pocket or wallet.",
                "Never refuse milk, water, or curd offered by an elderly woman.",
                "Wear white clothes on Mondays and avoid black or dark grey on that day.",
            ],
        },
        2: {
            "prediction": "Moon in the second house grants sweet speech, attractive features, and gradual accumulation of family wealth. The native enjoys good food, fine clothes, and a comfortable home, often inheriting jewellery or savings from the maternal side. Speech will charm strangers and disarm enemies, but emotional vulnerability around criticism is a lifelong issue. Education benefits from the mother's encouragement. Eye trouble or dental complaint may appear after forty. Marriage brings a partner who improves the financial picture, though family disputes over money may erupt at the time of inheritance distribution.",
            "remedies": [
                "Donate rice, sugar, and milk to a temple kitchen every Monday.",
                "Drink water out of a silver glass each morning for at least forty days.",
                "Place a silver coin in the family safe and refresh it during every Diwali.",
                "Avoid speaking sharply at the dining table; treat food as worship.",
            ],
        },
        3: {
            "prediction": "Moon in the third house creates a courageous, cheerful, and creative native who succeeds through writing, art, music, or short travel. Younger brothers and sisters thrive, and one of them often becomes a lifelong supporter. The native travels widely for work and gains from such movement. Health-wise, chest, lungs, and respiratory tracts need attention; smoking is particularly harmful. Imagination is rich, but restlessness sometimes prevents completion of long projects. Mother's blessings and small daily disciplines bring stability. Rivalry with neighbours or relatives in the same trade should be patiently avoided.",
            "remedies": [
                "Feed milk to a stray cat every Monday for sixteen consecutive weeks.",
                "Offer water mixed with a few drops of milk at the roots of a peepal tree on Mondays.",
                "Gift silver bangles or a silver coin to a younger sister on her birthday.",
                "Recite Chandra Gayatri eleven times before beginning any creative project.",
            ],
        },
        4: {
            "prediction": "The Moon in its pukka ghar makes the native deeply attached to home, mother, and homeland. Domestic comforts, vehicles, and property accumulate naturally, and the family home becomes a centre of gatherings. The mother lives long and acts as the spiritual anchor of the household. Public support, popularity in the neighbourhood, and emotional intelligence are pronounced. Ailments related to chest, water retention, and anxiety appear in middle age. The native should never sell ancestral property in haste; even idle land left unsold continues to bless the family with hidden prosperity.",
            "remedies": [
                "Place a silver pot of water in the north-east corner of the house and refresh it daily.",
                "Serve your mother with your own hands at least one meal each Monday.",
                "Plant a tulsi at home and water it personally without missing a day.",
                "Donate white sweets and rice pudding to a temple on every full moon.",
            ],
        },
        5: {
            "prediction": "Moon in the fifth house grants a creative mind, devotional temperament, and beautiful children who bring social standing to the family. The native often excels in arts, education, or counselling, and earns the trust of the public through emotional sincerity. Speculative gains are mild but consistent, especially in trades connected to liquids, dairy, or hospitality. Children's education becomes a major lifelong investment that pays back richly. Conception may take time, especially for the first child. Devotional practice undertaken with the spouse multiplies both family harmony and material prosperity considerably.",
            "remedies": [
                "Offer kheer or rice pudding to children of a school on every full moon day.",
                "Worship Lord Krishna with white flowers every Monday evening.",
                "Donate a silver coin to a temple at the time of any child's birth in the family.",
                "Keep a silver glass of water by the bedside through the night.",
            ],
        },
        6: {
            "prediction": "Moon in the sixth house weakens emotional balance and creates sensitivity that enemies sometimes exploit. The mother's health is a recurring concern, and the native may face frequent minor illnesses related to stomach, anxiety, or digestion. Despite this, victory over open enemies is assured, and earnings through service, hospitals, food businesses, or care professions are favourable. Pets brought home, especially black animals, may not survive long. Lending money to relatives almost always ends in dispute. Charity given quietly to women in distress strengthens the placement and improves both health and finances steadily.",
            "remedies": [
                "Donate milk and rice at a temple every Monday morning for forty-three weeks.",
                "Avoid keeping a black dog or cat in the house.",
                "Offer water to a peepal tree before sunrise on every Monday for eleven weeks.",
                "Never refuse food or water to anyone who knocks at the door at meal time.",
            ],
        },
        7: {
            "prediction": "Moon in the seventh house gives an emotional, beautiful, and somewhat moody spouse, often connected to the water, dairy, or hospitality trade. The native is romantic and sensitive in marriage but prone to misunderstanding moods. Business in partnership with women, food, or liquids prospers. Travel with the spouse brings recognition and wealth. The native must guard against secret affairs, as such involvement always destroys reputation here. Health of the spouse needs attention around childbirth and again in the late forties. Sweet speech to in-laws preserves long-term peace and material gain.",
            "remedies": [
                "Gift silver ornaments to the wife or mother on every wedding anniversary.",
                "Offer milk-rice to a Shivling on Mondays before discussing any business deal.",
                "Avoid eating heavy food at night; prefer light, white-coloured meals on Mondays.",
                "Donate white clothes to a widowed lady on any full moon day.",
            ],
        },
        8: {
            "prediction": "Moon in the eighth house brings emotional turbulence, fluctuating finances, and an unusually intuitive, almost psychic mind. The mother's health needs vigilant care, and inheritance, when it comes, often arrives after prolonged illness in the family. The native is drawn to occult, mystical, or research subjects and may receive unexpected insights through dreams. Chronic stomach, urinary, or hormonal complaints may emerge after thirty-five. Sea voyages, foreign residence, and inheritance through the wife's family are likely. Compulsive worry is the chief enemy; meditation and regular routines are not optional but essential.",
            "remedies": [
                "Offer milk to a flowing river without looking back for eleven Mondays.",
                "Place a silver vessel of water by the bedside each night and discard it at sunrise.",
                "Donate a milch cow with calf to a temple or gaushala if circumstances allow.",
                "Avoid second-hand clothing, jewellery, or a used bed from unknown sources.",
            ],
        },
        9: {
            "prediction": "Moon in the ninth house grants a religious, fortunate, and emotionally generous native whose mother is the symbol of family religion. Education benefits from travel, especially abroad or to holy sites. Income grows through publishing, teaching, counselling, or service to the public. The father lives long, though may be of a quieter temperament than the mother. Dreams and intuition guide major decisions accurately. Charitable acts performed in the mother's name yield extraordinary benefit. Avoid making promises in the temple that you cannot keep, as broken vows here recoil with unusual swiftness.",
            "remedies": [
                "Donate rice, sugar, and a silver coin at a Shiva temple on every full moon.",
                "Visit a major pilgrimage site with the mother at least once in life.",
                "Offer water from a silver vessel to a peepal tree every Monday morning.",
                "Keep a small silver image of your family deity in the worship room.",
            ],
        },
        10: {
            "prediction": "Moon in the tenth house produces a public-facing career marked by recognition, popularity, and emotional investment in work. Professions in hospitality, dairy, water, public welfare, hospitals, or media suit best. The native rises through goodwill rather than aggression and becomes known as a person whose word is trusted. The mother's blessings are directly tied to professional success; her displeasure causes immediate setback. Frequent travel and changes of location are common. Mood fluctuations should not be allowed to dictate major career decisions, as such impulsive choices later cost months of recovery effort.",
            "remedies": [
                "Touch the feet of your mother before leaving for any major work meeting.",
                "Donate rice and milk to an orphanage every full moon.",
                "Keep a silver pen or silver-plated object on your work desk.",
                "Avoid signing important contracts during a no-moon (amavasya) day.",
            ],
        },
        11: {
            "prediction": "Moon in the eleventh house brings many friends, popularity in social circles, and steady fulfilment of wishes through influential women or maternal contacts. Income is variable but always sufficient, with sudden gains around full moon periods. Elder siblings prosper and assist generously. Children, when they arrive, become a continuing source of joy and support in old age. Health-wise, watch for swelling, blood-related issues, and emotional eating after middle age. Friendships built through honesty endure for decades; those built on flattery dissolve quickly and leave the native disappointed and emotionally drained.",
            "remedies": [
                "Donate sweets made of milk to children at a temple every full moon day.",
                "Always keep a silver coin or small silver utensil in the savings drawer.",
                "Avoid borrowing money from women relatives, even small amounts.",
                "Offer a glass of water from a silver vessel to your mother on her birthday.",
            ],
        },
        12: {
            "prediction": "The Moon in the twelfth house creates a contemplative, dreamy, and somewhat solitary native who may live far from the mother for long periods. Sleep disturbances, vivid dreams, and emotional withdrawal during stress are common. Foreign travel, residence abroad, or work in hospitals, monasteries, or charities suits well. Hidden enemies and secret expenses on relatives appear repeatedly. Spiritual practice yields exceptional progress here, and donations made anonymously to women in distress multiply. Eye trouble and water retention may appear after forty-five. Excessive isolation should be balanced with steady, simple human contact.",
            "remedies": [
                "Place a silver vessel of water at the bedside and discard it at sunrise daily.",
                "Donate milk and white sweets at a temple before any foreign journey.",
                "Offer water to a tulsi plant every morning before sunrise.",
                "Sleep with the head facing east and avoid the western direction strictly.",
            ],
        },
    },
    "Mars": {
        1: {
            "prediction": "Mars in the first house gives a strong, athletic body, fierce courage, and a quick temper that the native must learn to control early. The native becomes the protector of the family and rises through the police, military, sports, surgery, or engineering. Brothers may be few but the bond is intense, oscillating between deep loyalty and sharp conflict. Marriage requires care, especially if Mars is afflicted, as the native's hot temperament strains the spouse. Accidents involving fire, sharp objects, or vehicles are possible in youth. Discipline, exercise, and patience convert raw energy into steady success.",
            "remedies": [
                "Offer red flowers and jaggery at a Hanuman temple every Tuesday.",
                "Donate red lentils and a copper coin to a labourer on Tuesdays.",
                "Carry a small silver square in the wallet at all times.",
                "Avoid wearing red clothes on Saturdays and black on Tuesdays.",
            ],
        },
        2: {
            "prediction": "Mars in the second house creates a sharp tongue and a tendency to ignite quarrels at the dinner table. Family wealth fluctuates due to disputes among siblings or partners. The native earns through bold decisions, real estate, weapons, machinery, or short trades, but must avoid loans taken in anger. Speech is forceful and often persuasive in business, though it offends easily in personal life. Dental and eye trouble are likely. Inheritance disputes are common; the native should document family arrangements early. Practising silence for one hour each day visibly improves both finances and family harmony.",
            "remedies": [
                "Offer sweet rice (kheer) at a Hanuman temple every Tuesday.",
                "Donate red coral, copper, or a red-coloured cloth at a temple on Tuesdays.",
                "Drink water from a silver glass each morning for forty days.",
                "Distribute jaggery and gram to school children at least once a month.",
            ],
        },
        3: {
            "prediction": "Mars in its pukka ghar produces extraordinary courage, leadership in the family, and significant gains through self-effort. The native often rises higher than the elder brother and may eclipse the father's reputation by middle age. Writing, sports, surgery, engineering, military, and police professions are favourable. Younger siblings prosper and become lifelong allies. Short journeys bring success; long ones drain energy. Health is generally robust, though injuries from sharp objects and vehicles must be guarded against. The native's word carries unusual force; reckless promises made in anger return with painful precision.",
            "remedies": [
                "Recite Hanuman Chalisa eleven times every Tuesday.",
                "Donate red lentils and jaggery to a temple every Tuesday morning.",
                "Plant a neem or red-flowered tree near the home and care for it personally.",
                "Avoid lending sharp tools or weapons to others, even briefly.",
            ],
        },
        4: {
            "prediction": "Mars in the fourth house disturbs domestic peace and creates conflict with the mother or over property matters. The native is restless at home and finds peace only when occupied with vigorous outdoor work. Vehicles, machinery, and land deals can bring sudden gains followed by sudden losses. The mother's health needs care, particularly regarding blood pressure and inflammation. Frequent change of residence is likely until the late thirties, after which a permanent home becomes possible. Hospitality should be controlled, as guests sometimes cause friction. Cultivating patience at home yields disproportionate professional rewards.",
            "remedies": [
                "Place a sweet (peda) under your pillow at night and donate it the next morning.",
                "Bury a copper or silver coin in the four corners of the property.",
                "Offer water to a peepal tree every Tuesday before sunrise.",
                "Serve your mother with sweets prepared in jaggery on every Tuesday.",
            ],
        },
        5: {
            "prediction": "Mars in the fifth house grants sharp intelligence, quick wit, and an attraction toward strategy, sports, or competitive examinations. Children are bold and independent, though one of them may face health challenges in childhood. Speculative ventures bring sharp swings; the native should restrict trading to disciplined, rule-based methods. Education in technical, surgical, or military fields succeeds brilliantly. Stomach inflammation, acidity, and sudden fevers are typical health concerns. Romantic attachments before marriage often involve passionate but troubled relationships. Spiritual practice undertaken with discipline grants surprising creative breakthroughs and a calmer family environment.",
            "remedies": [
                "Donate red sweets to children at a school on every Tuesday.",
                "Recite Mangal Stotra eleven times before any examination or competition.",
                "Avoid speculative trading on Tuesdays and Saturdays.",
                "Offer sindoor and red flowers to a Hanuman idol every Saturday evening.",
            ],
        },
        6: {
            "prediction": "Mars in the sixth house grants outstanding ability to defeat enemies, win court cases, and rise in service through fearless action. The native is a natural fighter for justice and prospers in police, law, surgery, or sports professions. Maternal uncles either help significantly or oppose openly. Health concerns include blood disorders, inflammations, accidents from fire, and surgery in middle age. Pets, especially aggressive breeds, suit the native and prosper. Lending money should be avoided, as repayment usually arrives only after open conflict. Daily physical exercise channels the surplus energy and keeps the temper from leaking into relationships.",
            "remedies": [
                "Feed sweet bread (meetha roti) to a brown dog every Tuesday.",
                "Donate masoor dal and a copper coin at a Hanuman temple every Tuesday.",
                "Carry a small silver square or coin in the wallet always.",
                "Avoid keeping rusted iron, broken tools, or torn clothes anywhere in the home.",
            ],
        },
        7: {
            "prediction": "Mars in the seventh house creates Mangal dosha, often delaying marriage or creating sharp disputes within it. The spouse is bold, energetic, and independent-minded, sometimes overshadowing the native in business or social life. Partnerships in trade rarely last; the native does best as the controlling decision-maker. Travel for business, especially across borders, brings gains. Surgery in the abdominal region after thirty-five is possible. Marriage to a partner who has also been delayed in their own marriage is the classical neutralising remedy. Anger management directly translates into business success here.",
            "remedies": [
                "Marry only after the age of twenty-eight, preferably to a Manglik partner.",
                "Donate red lentils and a sweet (peda) to a temple before fixing a marriage.",
                "Recite Hanuman Chalisa daily and especially on Tuesdays before marriage.",
                "Avoid signing any partnership deed on Tuesday or Saturday.",
            ],
        },
        8: {
            "prediction": "Mars in the eighth house creates a serious Mangal dosha that affects the spouse's longevity and the native's own susceptibility to accidents. Sudden health emergencies, surgeries, and unexpected expenses appear repeatedly. However, the placement is excellent for surgeons, researchers, occult practitioners, and insurance professionals. Inheritance often arrives after a long delay or legal dispute. Underground or hidden assets may yield sudden gains in middle age. The native should drive carefully throughout life and avoid risky sports after thirty-five. Regular charity in the name of Hanuman tangibly reduces the severity of these effects.",
            "remedies": [
                "Recite Sundarkand once a week, preferably on Tuesday or Saturday evening.",
                "Donate a copper or red item at a cremation ground after a relative's funeral.",
                "Avoid surgery on Tuesdays or Saturdays unless it is an emergency.",
                "Offer red flowers and sindoor at a Bhairava temple on the eighth lunar day.",
            ],
        },
        9: {
            "prediction": "Mars in the ninth house gives a fiercely religious, principled, and reform-minded native who is willing to fight for righteousness. The father may be authoritarian or absent, and the relationship with him swings between deep respect and sharp argument. Education in law, military strategy, or religious philosophy succeeds. Long journeys, especially to holy sites or for missionary work, are frequent. Hip, thigh, and blood-related ailments may appear after fifty. Charity given to soldiers, athletes, or the disabled multiplies blessings remarkably. Excessive moral certainty alienates allies; humility in religious matters is essential.",
            "remedies": [
                "Donate red flowers and a copper coin at a Hanuman temple every Tuesday.",
                "Visit a major pilgrimage site once every three years.",
                "Offer water and red sandalwood paste to a peepal tree on Tuesdays.",
                "Touch the feet of the father every Tuesday morning if he is alive.",
            ],
        },
        10: {
            "prediction": "Mars in the tenth house gives commanding professional authority and rapid rise through bold, decisive action. The native suits military, police, engineering, surgery, sports administration, and crisis-management roles. Promotions come through visible action rather than diplomacy. Subordinates respect but fear the native's directness; cultivating warmth multiplies loyalty. Father's blessings are decisive in early career. Health concerns include hypertension, overwork, and inflammation. The native should avoid all litigation initiated from anger, as such disputes drain both finances and reputation. Steady evening exercise prevents the energy from corroding into irritability.",
            "remedies": [
                "Place a small Hanuman idol or yantra at the workplace facing south.",
                "Donate masoor dal, jaggery, and a copper coin every Tuesday.",
                "Offer sweets to children of subordinates on every promotion or festival.",
                "Avoid accepting expensive gifts from superiors or business partners.",
            ],
        },
        11: {
            "prediction": "Mars in the eleventh house brings powerful friends, gains through bold ventures, and significant income from real estate, machinery, weapons, sports, or technology. Elder siblings prosper and assist materially. Wishes are fulfilled, but only after a struggle that tests the native's persistence. Friendships are intense and useful but tend to break violently if betrayed. Income increases sharply after the age of thirty-two. Ear, hip, and blood-related issues may appear after fifty. The native should avoid joint speculation with friends, as profits attract envy and losses end relationships permanently.",
            "remedies": [
                "Donate red lentils and jaggery to labourers every Tuesday morning.",
                "Recite Hanuman Chalisa eleven times each Tuesday for forty-three weeks.",
                "Carry a small silver square in the wallet for protection of earnings.",
                "Avoid lending money to friends on Tuesday or Saturday.",
            ],
        },
        12: {
            "prediction": "Mars in the twelfth house creates expenses through accidents, litigation, hidden enemies, or impulsive ventures. Sleep is disturbed, and the native may suffer from frequent inflammations, eye trouble, and surgical interventions in middle age. Foreign travel and residence away from birthplace are likely, often connected to defence, research, or medical professions. Hidden adversaries cause harm through indirect means; legal action initiated by the native usually backfires. Spiritual practice involving discipline and silence tames the placement. Charity given quietly to the wounded or homeless brings unexpected protection during dangerous moments.",
            "remedies": [
                "Donate red sweets at a Hanuman temple every Tuesday evening.",
                "Sleep with the head facing east and never toward the south.",
                "Avoid keeping sharp weapons, broken glass, or rusted iron in the bedroom.",
                "Recite Bajrang Baan once a week for protection against hidden enemies.",
            ],
        },
    },
    "Mercury": {
        1: {
            "prediction": "Mercury in the first house gives a sharp intellect, quick speech, and youthful appearance that often makes the native look ten years younger than his age. Education proceeds smoothly, and the native excels in mathematics, accounts, communication, writing, or trade. The maternal uncle plays an unusually important role, either as benefactor or rival. Skin complaints, nervous disorders, and stress-related ailments may appear if Mercury is afflicted. Marriage to an intelligent, articulate partner is likely. Habit of speaking before thinking creates avoidable enemies; the native should learn to pause before replying in tense moments.",
            "remedies": [
                "Donate green moong dal and a green-coloured cloth at a temple on Wednesdays.",
                "Feed green grass to a cow every Wednesday for forty-three weeks.",
                "Wear a silver chain or silver ring on the little finger of the right hand.",
                "Pierce the right ear or nostril (in the case of a woman) for protection.",
            ],
        },
        2: {
            "prediction": "Mercury in the second house grants persuasive speech, accumulated wealth through trade, and a family known for its eloquence. The native excels in business, banking, journalism, teaching, or sales and tends to enjoy multiple income streams simultaneously. Speech is the chief asset and the chief liability — humour wins friends and sarcasm makes lasting enemies. Education benefits from the maternal side. Throat, dental, and nervous complaints may appear after forty. Marriage often connects two families through trade interests. Maintaining truthfulness in financial dealings preserves both reputation and the unusual fluency that destiny grants here.",
            "remedies": [
                "Donate green moong dal and a small piece of silver at a temple on Wednesdays.",
                "Feed green vegetables to a cow every Wednesday for forty-three weeks.",
                "Drink water from a silver glass and avoid harsh language at the dining table.",
                "Distribute notebooks and pens to school children every Wednesday.",
            ],
        },
        3: {
            "prediction": "Mercury in the third house produces a brilliant writer, speaker, or entrepreneur whose energy thrives on short trips, networking, and continuous learning. Younger siblings prosper, and one of them often becomes the native's business partner. Communication-based businesses such as publishing, IT, telecom, journalism, and education succeed beautifully. The native is restless and easily bored, so projects requiring long focus need a co-founder for completion. Health-wise, hands, shoulders, and the nervous system need rest periodically. Reputation is built and destroyed through written words; the native should never send an angry message in haste.",
            "remedies": [
                "Donate green books or notebooks to school children on Wednesdays.",
                "Plant a green-leaved tree near the home and water it personally.",
                "Wear a silver chain around the neck for steadiness of mind.",
                "Recite Vishnu Sahasranama every Wednesday morning.",
            ],
        },
        4: {
            "prediction": "Mercury in the fourth house grants a comfortable, well-furnished home filled with books, gadgets, and intellectual conversation. The mother is educated and influential, and her advice on financial matters proves repeatedly correct. The native may run a business from home or own multiple small properties. Vehicles change frequently as preferences evolve. Education in commerce, IT, or communication suits well. Anxiety, insomnia, and nervous complaints appear under stress; meditation is therefore essential. The maternal uncle's blessings are tied directly to the native's domestic prosperity, and any quarrel with him brings immediate household friction.",
            "remedies": [
                "Place a green plant in the north direction of the home.",
                "Donate green vegetables and moong dal to a temple kitchen on Wednesdays.",
                "Serve your mother with your own hands at least one meal each Wednesday.",
                "Keep a small silver glass of water in the worship room and refresh it daily.",
            ],
        },
        5: {
            "prediction": "Mercury in the fifth house produces a sharp-minded native with literary, mathematical, or strategic talents that surface in childhood. Education proceeds with distinction, particularly in commerce, mathematics, IT, or law. Children, especially daughters, are intelligent and add to the family's prestige. Short-term trades and intellectual speculation yield gains, but only with discipline. Romantic attachments tend to begin through written communication. Stomach and nervous complaints may appear during examinations or high-stress phases. Devotional practice combined with study gives the native a calm intuition that turns intellect into wisdom over the years.",
            "remedies": [
                "Donate green moong dal at a temple kitchen every Wednesday.",
                "Worship Lord Vishnu with tulsi leaves on every Wednesday morning.",
                "Distribute pens, notebooks, and sweets to school children on birthdays.",
                "Avoid speculation in stocks or lottery on Wednesdays.",
            ],
        },
        6: {
            "prediction": "Mercury in the sixth house grants outstanding analytical ability, especially in law, accounts, audit, medicine, or research. The native defeats enemies through sharper logic and better documentation rather than raw force. Maternal uncles play a significant role, sometimes as collaborators, sometimes as rivals. Service-class income is steady, with frequent promotions through skill rather than influence. Skin allergies, nervous disorders, and digestive issues are typical health concerns. Pets, particularly birds, suit the household. The native should avoid ridiculing enemies in writing, as such communications later become evidence and damage hard-won professional standing.",
            "remedies": [
                "Donate green moong dal and a copper coin at a temple every Wednesday.",
                "Feed green grass and fodder to a cow every Wednesday morning.",
                "Wear a silver ring on the little finger of the right hand.",
                "Avoid eating non-vegetarian food on Wednesdays for forty-three weeks.",
            ],
        },
        7: {
            "prediction": "Mercury in its pukka ghar gives a witty, intelligent, and youthful spouse, often connected to trade, communication, or education. Business partnerships flourish, especially in fields requiring negotiation, writing, or cross-border coordination. Marriage is often arranged through professional networks rather than family connections. The native gains through written contracts, agencies, and franchises. Health of the spouse remains generally good, though nervous strain and insomnia appear under prolonged stress. Verbal misunderstandings within marriage arise quickly but heal equally fast. Treating the spouse as an intellectual equal is the secret to lifelong harmony in this position.",
            "remedies": [
                "Gift the wife a silver chain or green-coloured saree on every anniversary.",
                "Donate green moong dal and a green cloth at a temple on Wednesdays.",
                "Avoid signing important contracts on a no-moon day.",
                "Recite Vishnu Sahasranama with the spouse every Wednesday evening.",
            ],
        },
        8: {
            "prediction": "Mercury in the eighth house grants extraordinary research ability, occult interest, and aptitude for forensic, audit, or investigative work. The native uncovers hidden truths and may earn through inheritance, insurance, or research grants. Speech is sometimes sharp and unusually penetrating, occasionally hurting close relatives without intention. Skin complaints, nervous disorders, and hormonal imbalances may appear after thirty-five. Maternal uncles' health remains a recurring concern. Sudden gains through unusual sources are likely. The native should avoid signing complex financial documents in haste, as fine print here often hides exactly the trouble that destiny watches for.",
            "remedies": [
                "Donate green moong dal at a temple kitchen on every Wednesday for forty-three weeks.",
                "Avoid borrowing from in-laws or sister's family.",
                "Feed green fodder to a cow every Wednesday morning.",
                "Recite Vishnu Sahasranama on Wednesday evenings for clarity in legal matters.",
            ],
        },
        9: {
            "prediction": "Mercury in the ninth house gives a learned, well-travelled native with a gift for languages, philosophy, and cross-cultural communication. Higher education abroad or in distant cities is likely. Income flows from publishing, teaching, consulting, law, or international trade. The father may be a scholar or trader, and his guidance is repeatedly accurate. Long journeys are frequent and almost always profitable. Religious philosophy fascinates the native, who often becomes a bridge between traditional wisdom and modern audiences. Avoid debating religion publicly, as intellectual victory here often costs friendship and professional collaboration.",
            "remedies": [
                "Donate green books, notebooks, or pens to a school every Wednesday.",
                "Visit a Vishnu temple on every Wednesday evening for blessings before travel.",
                "Wear a silver chain with a small Vishnu pendant for protection on journeys.",
                "Touch the feet of teachers and elders before any major examination or trip.",
            ],
        },
        10: {
            "prediction": "Mercury in the tenth house grants a successful career in communication, trade, IT, law, education, or finance. The native is recognised for intelligence, quick decision-making, and ability to negotiate complex deals. Multiple sources of income are common, sometimes through consulting alongside a primary job. Subordinates and clients respect the native's clarity. Father's profession often influences the early career. Health-wise, mental fatigue, insomnia, and nervous disorders need management through routine. Reputation built through written work endures; reputation built only through oral promises proves fragile and demands continual reinforcement.",
            "remedies": [
                "Place a green plant on the work desk and water it personally.",
                "Donate green moong dal and a green cloth to a temple on Wednesdays.",
                "Distribute sweets to office subordinates on every promotion or success.",
                "Recite Vishnu Sahasranama once a week before beginning major projects.",
            ],
        },
        11: {
            "prediction": "Mercury in the eleventh house brings many intellectual friends, multiple income streams, and steady fulfilment of ambitions through networking. The native excels in trade, brokerage, agencies, IT, and writing-based businesses. Elder siblings, particularly sisters, prosper and assist generously. Wishes are fulfilled through collaboration rather than solo effort. Income grows steadily after the age of twenty-eight. Hearing, nervous, or skin issues may appear after fifty. Friendships built on shared business interests endure as long as accounts remain transparent; secrecy in money matters here destroys the most valuable contacts the native makes in early career.",
            "remedies": [
                "Donate green moong dal and notebooks to school children every Wednesday.",
                "Wear a silver chain or silver ring on the little finger of the right hand.",
                "Avoid lending money to friends on Wednesdays without written agreement.",
                "Distribute sweets and pens to children of friends on their birthdays.",
            ],
        },
        12: {
            "prediction": "Mercury in the twelfth house grants intuition, dream insight, and aptitude for foreign trade, translation, or research in solitude. The native may live abroad or work in a behind-the-scenes capacity. Speech is gentle but sometimes hesitant, and writing serves the native better than oratory. Hidden enemies attempt to misrepresent the native's words; documentation prevents such damage. Eye, nervous, and skin complaints may appear after forty. Spiritual study, especially of philosophical texts, brings calm and unexpected insights. Excessive secrecy ruins partnerships; selective transparency with trusted associates protects both reputation and steady professional growth.",
            "remedies": [
                "Donate green moong dal at a temple before any foreign journey.",
                "Wear a silver chain with a Vishnu pendant for protection during travel.",
                "Recite Vishnu Sahasranama every Wednesday evening for clarity of mind.",
                "Avoid signing important documents during the time after sunset on Wednesdays.",
            ],
        },
    },
    "Jupiter": {
        1: {
            "prediction": "Jupiter in the first house produces a wise, generous, and respected native whose presence calms any room. The native is religious, principled, and naturally drawn toward teaching, advisory, or judicial roles. Wealth grows steadily through legitimate means, and the family's social standing improves visibly after the native's birth. Children, especially sons, are healthy and bring honour. Liver, weight, and metabolic issues may appear after forty. Marriage is to a virtuous partner, often from a respected family. Pride in religious or moral matters can isolate friends; humility multiplies the benefic effect of this excellent placement.",
            "remedies": [
                "Worship Lord Vishnu and donate yellow items at a temple every Thursday.",
                "Apply a saffron tilak on the forehead daily before leaving home.",
                "Donate gram dal, turmeric, and yellow cloth to a temple priest on Thursdays.",
                "Avoid wearing black or grey on Thursdays.",
            ],
        },
        2: {
            "prediction": "Jupiter in the second house grants steady wealth, sweet truthful speech, and a family known for its generosity. The native enjoys good food, fine dwellings, and the confidence of elders. Education benefits from the father's encouragement, and the family savings grow through prudent investment rather than speculation. Inheritance often arrives without dispute. Throat, weight, and dental issues may appear after forty-five. Marriage strengthens the financial position. Habit of giving advice unasked offends some relatives; the native should reserve counsel for those who request it, and even then, deliver it with restraint.",
            "remedies": [
                "Donate yellow sweets, turmeric, and gram dal at a temple every Thursday.",
                "Drink water from a silver glass and avoid harsh speech at the dining table.",
                "Place a small silver coin in the family safe and refresh it during Diwali.",
                "Recite Vishnu Sahasranama on Thursday mornings for stable family wealth.",
            ],
        },
        3: {
            "prediction": "Jupiter in the third house grants courage tempered with wisdom, gain through writing or teaching, and a strong bond with elder siblings. The native is honest, straightforward, and sometimes too candid in conversation. Short journeys for educational or religious purposes prosper. Income from publishing, training, consulting, or religious instruction is favourable. Health-wise, ears, throat, and lungs need protection from cold. The native should avoid taking on too many small projects at once, as Jupiter here loves expansion to the point of overcommitment. Quality of writing exceeds quantity here, and patient editing pays off.",
            "remedies": [
                "Donate yellow sweets and turmeric to a temple every Thursday.",
                "Recite Vishnu Sahasranama or Hanuman Chalisa on Thursdays.",
                "Plant a banana tree at home and water it personally.",
                "Touch the feet of elder siblings and elders on every Thursday.",
            ],
        },
        4: {
            "prediction": "Jupiter in the fourth house grants a peaceful, religious home filled with elders' blessings, books, and a steady flow of guests. The mother is virtuous and devoted, and her religious practice protects the family through difficult phases. Property, vehicles, and ancestral wealth accumulate slowly but reliably. Education benefits enormously from the home environment. Hospitality is a defining feature of the household. Liver, weight, and chest issues may appear after fifty. The native must resist excessive comfort and luxury, which slowly erode ambition. Donations made from the home itself yield disproportionately powerful results.",
            "remedies": [
                "Place a small Vishnu or Krishna idol in the worship room and offer tulsi daily.",
                "Donate yellow sweets, turmeric, and gram dal at a temple every Thursday.",
                "Serve your mother and elders with your own hands at least one meal each Thursday.",
                "Plant a tulsi at home and water it personally without missing a day.",
            ],
        },
        5: {
            "prediction": "Jupiter in the fifth house produces virtuous, intelligent, and devoted children who become the family's pride. The native excels in education, teaching, judicial work, finance, or counselling. Conception is generally easy, and the first child often arrives with great joy. Speculative gains are possible but should be limited to disciplined methods. Devotional practice begins early in life and brings tangible material rewards. Stomach, liver, and weight issues may appear after fifty. Mantra recitation undertaken regularly grants the native sharp intuition that converts ordinary opportunities into substantial wealth over time.",
            "remedies": [
                "Worship Lord Vishnu with tulsi leaves every Thursday morning.",
                "Donate yellow sweets to children of a school on every Thursday.",
                "Recite Vishnu Sahasranama or Bhagavad Gita on Thursdays.",
                "Distribute books, notebooks, and yellow sweets to needy students annually.",
            ],
        },
        6: {
            "prediction": "Jupiter in the sixth house produces a brave, principled fighter for justice who defeats enemies through truth and steady persistence. The native succeeds in legal, advisory, medical, or service-oriented professions. Maternal uncles are generally helpful, especially in legal matters. Loans taken are repaid easily, but loans given should be documented carefully. Skin, liver, and weight-related ailments may appear after forty. The native should avoid taking sides in family disputes, as Jupiter's wisdom here is most effective when remaining neutral. Charity in the form of food or education for the poor strengthens the placement enormously.",
            "remedies": [
                "Donate yellow sweets, turmeric, and gram dal at a temple every Thursday.",
                "Feed yellow food (gram dal, banana) to a cow every Thursday morning.",
                "Avoid eating non-vegetarian food on Thursdays.",
                "Recite Hanuman Chalisa or Vishnu Sahasranama on Thursday evenings.",
            ],
        },
        7: {
            "prediction": "Jupiter in the seventh house grants a wise, virtuous, and often well-educated spouse who brings spiritual depth to the marriage. Business partnerships in education, finance, advisory work, or religious enterprises prosper. Marriage may be slightly delayed but yields lifelong contentment when it comes. The spouse often hails from a family of good reputation and influences the native toward generosity and religious practice. Health of the spouse remains generally good. Travel with the spouse to pilgrimage sites brings unusual blessings. Avoid moralising with the spouse in public; private guidance preserves the dignity that this placement otherwise grants.",
            "remedies": [
                "Worship Lord Vishnu with the spouse on every Thursday evening.",
                "Donate yellow sweets and turmeric at a temple before marriage discussions.",
                "Visit a major pilgrimage site with the spouse at least once every five years.",
                "Apply a saffron tilak on the forehead before any business meeting.",
            ],
        },
        8: {
            "prediction": "Jupiter in the eighth house grants long life, philosophical insight, and gain through inheritance, insurance, or trust funds. The native is interested in occult, research, and metaphysical subjects and may become a quiet authority in such fields. Sudden gains through unusual sources are possible but inconsistent. Liver, weight, and metabolic issues may appear after forty. Inheritance disputes are usually resolved in the native's favour, though slowly. The native should avoid risky speculation, as Jupiter here protects from total loss but cannot guarantee profit. Spiritual practice undertaken with sincerity yields extraordinary peace and gradual financial stability.",
            "remedies": [
                "Donate yellow cloth, gram dal, and turmeric at a temple every Thursday.",
                "Recite Vishnu Sahasranama on Thursday evenings for protection.",
                "Avoid borrowing from in-laws or family friends.",
                "Visit a temple of Bhairava or Shiva on the eighth lunar day each month.",
            ],
        },
        9: {
            "prediction": "Jupiter in its pukka ghar produces an extraordinarily fortunate native blessed by the father's good karma and the wisdom of elders. Education proceeds brilliantly, often abroad or in prestigious institutions. The native rises in advisory, legal, religious, or educational professions and earns lasting respect in the community. Pilgrimages are frequent and transformative. Sons born are virtuous, though sometimes after a delay. Wealth accumulates through legitimate means and is shared generously. Pride in spiritual or scholarly matters is the chief warning here; humility multiplies the already generous blessings of this placement many times over.",
            "remedies": [
                "Worship Lord Vishnu and donate yellow items at a temple every Thursday.",
                "Touch the feet of the father and family teachers on every Thursday morning.",
                "Apply a saffron tilak on the forehead daily before leaving home.",
                "Visit a major pilgrimage site at least once every three years.",
            ],
        },
        10: {
            "prediction": "Jupiter in the tenth house grants a respected, advisory, or judicial career and steady rise through fairness rather than aggression. The native excels in law, education, finance, religious institutions, or government advisory roles. Father's blessings are decisive in early career. Subordinates respect the native deeply, and reputation for honesty becomes the chief professional asset. Health-wise, weight, liver, and joint issues may appear after fifty. Promotions arrive slowly but are extremely durable. The native should avoid lecturing colleagues unprompted, as Jupiter here is most effective when wisdom is requested rather than imposed.",
            "remedies": [
                "Apply a saffron tilak on the forehead before leaving for work.",
                "Donate yellow sweets, turmeric, and gram dal at a temple every Thursday.",
                "Distribute sweets to subordinates on every promotion or major success.",
                "Recite Vishnu Sahasranama every Thursday morning for steady career growth.",
            ],
        },
        11: {
            "prediction": "Jupiter in the eleventh house brings noble friends, steady fulfilment of ambitions, and significant gain through elders, teachers, and advisors. Income grows reliably through legitimate channels, and one major source of earnings often comes from advisory or educational work. Elder siblings prosper and assist with wisdom and material support. Children, when they arrive, become a continuing source of joy. Hearing, joint, and weight-related issues may appear after fifty. Friendships built on shared values endure for decades. Avoid lending money to younger relatives without clear terms; misunderstanding here erodes Jupiter's otherwise generous flow of income.",
            "remedies": [
                "Donate yellow sweets, gram dal, and turmeric at a temple every Thursday.",
                "Apply a saffron tilak on the forehead daily before leaving home.",
                "Touch the feet of elder siblings and family teachers on every Thursday.",
                "Recite Vishnu Sahasranama every Thursday morning for continuous gain.",
            ],
        },
        12: {
            "prediction": "Jupiter in the twelfth house grants spiritual depth, charitable inclination, and gain through foreign lands, monasteries, or large institutions. The native may live abroad for long periods or work in advisory roles for charities, hospitals, or religious organisations. Sleep is peaceful and dreams are often prophetic. Hidden expenses on religious causes, education, and elders are continuous but spiritually rewarding. Weight, liver, and foot issues may appear after fifty. Donations made anonymously yield extraordinary results here. The native should avoid moralising in public, as Jupiter in the twelfth works best through silent example rather than active preaching.",
            "remedies": [
                "Donate yellow sweets, turmeric, and gram dal at a temple before any foreign journey.",
                "Apply a saffron tilak on the forehead daily before leaving home.",
                "Recite Vishnu Sahasranama every Thursday evening for protection during travel.",
                "Visit a pilgrimage site once every three years to recharge the placement.",
            ],
        },
    },
    "Venus": {
        1: {
            "prediction": "Venus in the first house produces an attractive, charming, and aesthetically refined native who draws admirers easily. The native is fond of beauty, music, art, vehicles, and luxurious surroundings, often making a living through fashion, entertainment, hospitality, or beauty industries. Marriage is harmonious and the spouse adds substantially to wealth. Health is generally good, though kidney, urinary, and reproductive issues may appear if Venus is afflicted. The chief warning is against vanity and over-indulgence in pleasure, which can dissipate the considerable charm and fortune that this placement otherwise grants throughout life.",
            "remedies": [
                "Donate white sweets, white cloth, and curd at a temple every Friday.",
                "Worship Goddess Lakshmi with white flowers every Friday evening.",
                "Wear a silver chain or silver ring for stability of fortune.",
                "Avoid wearing torn or dirty clothes, especially on Fridays.",
            ],
        },
        2: {
            "prediction": "Venus in the second house grants accumulated wealth, sweet voice, and a family known for refinement and hospitality. The native enjoys fine food, beautiful clothes, and a comfortable home, often inheriting jewellery or art from the family. Speech is musical and often persuasive in business. Education benefits from the mother's or maternal aunt's encouragement. Throat, dental, and reproductive issues may appear after forty. Marriage strengthens the financial position remarkably. Family savings tend to grow through investment in jewellery, art, or property, and selling such inherited items in haste later proves regrettable.",
            "remedies": [
                "Donate white sweets, sugar, and curd at a temple every Friday morning.",
                "Worship Goddess Lakshmi with white flowers and recite the Lakshmi mantra.",
                "Drink water from a silver glass for forty consecutive days.",
                "Place a small silver coin in the family safe and refresh it during Diwali.",
            ],
        },
        3: {
            "prediction": "Venus in the third house grants artistic talent, charm in writing, and bonds with sisters or female cousins that prove materially helpful. The native succeeds in music, fashion, design, entertainment, or media professions. Short journeys, particularly for artistic or romantic reasons, are frequent. Income flows from creative work and partnerships with women. Throat, lungs, and reproductive issues may appear after forty. Romantic involvements before marriage are common but should not become public scandal. The native should avoid mixing romance with business partnerships, as such combinations typically end with the loss of both relationships permanently.",
            "remedies": [
                "Donate white sweets and curd to women at a temple every Friday.",
                "Gift silver bangles or silver chains to younger sisters on their birthdays.",
                "Recite the Sri Suktam on Friday mornings for prosperity.",
                "Avoid singing or performing in public on Saturdays.",
            ],
        },
        4: {
            "prediction": "Venus in the fourth house grants a beautiful home filled with art, music, vehicles, and the steady presence of joyful guests. The mother is refined, often artistic, and adds to the family's social standing. Properties, vehicles, and luxury items accumulate throughout life. Education in arts, design, or hospitality suits well. Domestic harmony is generally strong, though excess of comfort can soften ambition. Reproductive, urinary, and chest issues may appear after fifty. Hospitality given generously multiplies blessings; ostentatious display attracts envy and erodes the very harmony that destiny grants in this placement.",
            "remedies": [
                "Place fresh white flowers in the home every Friday and refresh them weekly.",
                "Donate white sweets, curd, and rice at a temple every Friday morning.",
                "Serve your mother with your own hands at least one meal each Friday.",
                "Plant a jasmine or rose at home and care for it personally.",
            ],
        },
        5: {
            "prediction": "Venus in the fifth house grants beautiful, talented children and an artistic, romantic temperament that wins admirers easily. The native excels in arts, entertainment, design, fashion, or hospitality. Romantic life before marriage is rich but sometimes complicated by indecision. Speculative gains in art, fashion, or entertainment are possible but should be balanced with steady income. Children, especially daughters, are often gifted in music or visual arts. Reproductive and urinary issues may appear if Venus is afflicted. Devotional practice combined with artistic pursuit grants the native a refined intuition that distinguishes him from rivals.",
            "remedies": [
                "Worship Goddess Lakshmi with white flowers every Friday evening.",
                "Donate white sweets and curd to children at a temple on Fridays.",
                "Gift silver coins to children of close relatives on their birthdays.",
                "Avoid lending or borrowing money on Fridays.",
            ],
        },
        6: {
            "prediction": "Venus in the sixth house weakens the planet's natural ease and creates difficulties in marriage, particularly disputes that test the spouse's patience. The native may earn through hospitality, food, beauty, or service-oriented businesses. Maternal uncles either help significantly or oppose openly. Reproductive, urinary, and skin issues are common health concerns. Pets, particularly cats or female animals, suit the household. The native should avoid lending money to women relatives, as such transactions often end in dispute. Charity given quietly to women in distress strengthens the placement and gradually heals marital friction.",
            "remedies": [
                "Donate white sweets, curd, and rice to a temple kitchen every Friday.",
                "Avoid wearing torn or stained clothes, especially on Fridays.",
                "Feed a white cow or female calf with green fodder every Friday.",
                "Recite the Sri Suktam on Friday evenings for harmony in marriage.",
            ],
        },
        7: {
            "prediction": "Venus in its pukka ghar grants a beautiful, loving spouse and a marriage that becomes the source of both happiness and material prosperity. The native succeeds in business partnerships, especially in fashion, hospitality, art, jewellery, or entertainment. Marriage usually arrives at the right time and brings substantial improvement to the financial picture. The spouse often comes from a refined family. Travel with the spouse for business or pleasure is frequent and profitable. Reproductive and urinary issues may appear after forty-five. Loyalty and tenderness sustain the marriage; secret affairs here ruin everything that destiny otherwise grants generously.",
            "remedies": [
                "Gift the wife white silk clothes or silver ornaments on every anniversary.",
                "Worship Goddess Lakshmi with the spouse on Friday evenings.",
                "Donate white sweets, sugar, and curd at a temple before marriage discussions.",
                "Avoid harsh speech with the spouse, especially on Fridays.",
            ],
        },
        8: {
            "prediction": "Venus in the eighth house grants long life, sensual charm, and gain through inheritance, insurance, or the spouse's family. The native is drawn to occult, research, and intimate emotional connections. Hidden romantic involvements, however, almost always create scandals here, so discretion and fidelity are essential. Reproductive, urinary, and hormonal issues may appear after thirty-five. Inheritance often arrives through the spouse or in-laws. Sudden gains through unusual sources are possible. The native should avoid borrowing from in-laws, as such loans rarely come without strings that later strain the marriage and family peace.",
            "remedies": [
                "Donate white cloth, sugar, and curd at a temple every Friday.",
                "Worship Goddess Lakshmi with white flowers every Friday evening.",
                "Avoid extramarital romantic involvement strictly throughout life.",
                "Visit a Bhairava temple on the eighth lunar day each month.",
            ],
        },
        9: {
            "prediction": "Venus in the ninth house grants a fortunate, refined, and well-travelled native whose love of beauty extends to philosophy, art, and culture. Higher education, often abroad, proceeds smoothly. Income flows from teaching, advisory work, hospitality, fashion, or international trade in luxury goods. The father may be artistic or refined in temperament. Long journeys for cultural or romantic reasons are frequent. Marriage often takes place during or after a long journey. Reproductive and joint issues may appear after fifty. Charitable acts performed for women, artists, or the elderly multiply blessings in unexpected ways.",
            "remedies": [
                "Donate white sweets, curd, and yellow cloth at a temple every Friday.",
                "Worship Goddess Lakshmi with white flowers on Friday mornings.",
                "Visit a major pilgrimage site, especially with the spouse, every few years.",
                "Apply a saffron tilak on the forehead before any major journey.",
            ],
        },
        10: {
            "prediction": "Venus in the tenth house grants a successful career in art, fashion, hospitality, entertainment, design, beauty, jewellery, or luxury industries. The native rises through charm, refinement, and ability to please clients. Father's profession often influences the early career. Subordinates respect the native's elegance and fairness. Female colleagues and clients play important roles in advancement. Reproductive and joint issues may appear after fifty. Reputation built through quality and refinement endures; ostentatious display attracts envy and erodes the goodwill that destiny otherwise grants generously throughout the working years here.",
            "remedies": [
                "Place fresh white flowers on the work desk every Friday.",
                "Donate white sweets, sugar, and curd at a temple every Friday.",
                "Apply a small bindi of sandalwood on the forehead before important meetings.",
                "Avoid signing major contracts on Saturdays.",
            ],
        },
        11: {
            "prediction": "Venus in the eleventh house brings refined friends, multiple income streams, and steady fulfilment of romantic and material wishes. The native gains through art, fashion, hospitality, beauty industries, and partnerships with women. Elder siblings, particularly sisters, prosper and assist generously. Income grows steadily, with sudden gains around festive seasons. Marriage often arrives through influential friends. Reproductive, urinary, and joint issues may appear after fifty. Friendships with refined, artistic women bring lifelong joy and material support. Avoid extravagant gifts to friends, as such gestures sometimes attract envy rather than the gratitude expected.",
            "remedies": [
                "Donate white sweets and curd at a temple every Friday morning.",
                "Worship Goddess Lakshmi with white flowers every Friday evening.",
                "Gift silver coins or chains to younger sisters on their birthdays.",
                "Avoid lending money to friends on Fridays.",
            ],
        },
        12: {
            "prediction": "Venus in the twelfth house grants spiritual love, charitable temperament, and significant expenses on luxury, beauty, comfort, and pleasure. The native may live abroad and gain through foreign trade in luxury goods, art, or hospitality. Marriage often involves a partner from a distant place or different culture. Sleep is comfortable and dreams are often pleasant. Hidden romantic involvements should be strictly avoided here, as scandals destroy reputation built over decades. Reproductive and urinary issues may appear after forty. Donations made anonymously to artists, women, or the elderly bring unexpected blessings.",
            "remedies": [
                "Donate white sweets, curd, and white cloth at a temple before any foreign journey.",
                "Worship Goddess Lakshmi with white flowers every Friday evening.",
                "Avoid extramarital romantic involvement strictly throughout life.",
                "Place a small silver vessel of water at the bedside and refresh it daily.",
            ],
        },
    },
    "Saturn": {
        1: {
            "prediction": "Saturn in the first house produces a serious, hardworking, and disciplined native who looks older than his years and matures emotionally early. Childhood is often difficult, with delays in education and recognition until the early thirties. The native succeeds through persistence rather than charm and rises in fields requiring patience: law, administration, engineering, mining, or labour management. Health concerns include joint pain, dental issues, and chronic complaints from middle age. Marriage may be delayed but proves stable. Father's relationship is often distant or strained. After thirty-six, the placement begins to deliver its considerable promised rewards.",
            "remedies": [
                "Feed jaggery and gram flour to a black dog every Saturday for forty-three weeks.",
                "Donate black sesame, mustard oil, and a black cloth at a Shani temple on Saturdays.",
                "Light a mustard oil lamp before a Shani idol every Saturday evening.",
                "Avoid wearing red or white clothes on Saturdays; prefer dark blue or black.",
            ],
        },
        2: {
            "prediction": "Saturn in the second house creates slow but steady accumulation of wealth, often after considerable struggle in early adulthood. Family wealth may dissipate or face dispute, and the native often rebuilds it through patient effort. Speech is measured and sometimes harsh, which costs the native warmth in relationships. Education proceeds with delays. Eye, dental, and throat complaints are common. Inheritance, when it arrives, is often entangled in legal proceedings. Marriage may bring financial responsibilities for the spouse's family. Discipline in spending and saving converts Saturn's hardship into substantial old-age security here.",
            "remedies": [
                "Donate black sesame, mustard oil, and a black blanket at a Shani temple on Saturdays.",
                "Feed jaggery to a black cow every Saturday for sixteen weeks.",
                "Drink water from a silver glass and avoid harsh speech at the dining table.",
                "Recite Shani Stotra eleven times every Saturday evening.",
            ],
        },
        3: {
            "prediction": "Saturn in the third house grants exceptional courage developed through hardship and the ability to outlast all rivals through sheer endurance. Younger siblings may face health or career delays, and the native often becomes their guardian. Writing, research, engineering, mining, and long-term planning suit well. Short journeys may be tiring or delayed. Health-wise, ears, shoulders, and the nervous system need care. Income grows slowly but reliably. The native should avoid impulsive ventures, as Saturn here rewards methodical, long-term effort with extraordinary stability after the age of thirty-five.",
            "remedies": [
                "Donate black sesame and mustard oil at a Shani temple every Saturday.",
                "Feed black gram and jaggery to crows every Saturday morning.",
                "Recite Hanuman Chalisa eleven times on Saturdays for protection.",
                "Avoid lending sharp tools or weapons to others, even briefly.",
            ],
        },
        4: {
            "prediction": "Saturn in the fourth house disturbs domestic peace, causes delays in property acquisition, and creates emotional distance from the mother. The native may live away from the birthplace for long periods. Vehicles, when acquired, last unusually long but require frequent maintenance. Education often proceeds through hardship. The mother's health needs continuous care, particularly in joints and chest. The home may be inherited only after considerable family dispute. Frequent change of residence is common until the early forties, after which a stable home with deep roots becomes possible and brings lasting peace.",
            "remedies": [
                "Place a small Shani idol in the south-west corner of the home and offer mustard oil weekly.",
                "Donate black sesame, mustard oil, and a black blanket at a Shani temple on Saturdays.",
                "Serve your mother with your own hands at least one meal each Saturday.",
                "Avoid keeping broken or rusted iron items inside the home.",
            ],
        },
        5: {
            "prediction": "Saturn in the fifth house brings delays in conception, challenges with children, and a serious approach to education and creative work. The first child may arrive late or face health concerns in childhood. The native excels in long-term research, philosophy, history, geology, or strategic planning. Speculative gains are unreliable; steady professional income suits far better. Romantic life before marriage is restrained or marked by older partners. Stomach and joint complaints may appear. Devotional practice begun in youth grants surprising creative breakthroughs and gradually softens the placement's natural austerity over decades.",
            "remedies": [
                "Donate black sesame, mustard oil, and a black cloth at a Shani temple every Saturday.",
                "Recite Hanuman Chalisa eleven times every Tuesday and Saturday.",
                "Feed jaggery and gram flour to a black dog every Saturday for forty-three weeks.",
                "Avoid speculative trading on Saturdays.",
            ],
        },
        6: {
            "prediction": "Saturn in the sixth house grants outstanding ability to defeat enemies through persistence, win court cases through patient documentation, and rise in service through reliable performance. Maternal uncles may either help significantly or remain emotionally distant. Service-class income is steady, with promotions arriving slowly but durably. Health concerns include joint pain, chronic skin issues, and digestive complaints from middle age. Pets, especially black animals or working dogs, suit the household. The native should avoid impulsive litigation, as Saturn here favours long, well-prepared cases over hasty action and rewards patient strategy with assured victory.",
            "remedies": [
                "Feed jaggery and gram flour to a black dog every Saturday for forty-three weeks.",
                "Donate black sesame, mustard oil, and a black blanket at a Shani temple on Saturdays.",
                "Light a mustard oil lamp before a Shani idol every Saturday evening.",
                "Avoid eating non-vegetarian food on Saturdays.",
            ],
        },
        7: {
            "prediction": "Saturn in the seventh house delays marriage but produces a stable, mature, and faithful spouse, often older or more responsible than the native. Business partnerships endure but require patience and clear documentation. The native succeeds in long-term ventures, especially those involving land, mining, machinery, or large institutions. Travel for business is frequent but tiring. Health of the spouse remains generally good but slow to recover from illness. Marriage usually takes place after the age of twenty-eight. Sweet speech and reliable conduct strengthen the marriage; impatience here erodes the very stability that Saturn otherwise grants.",
            "remedies": [
                "Marry only after the age of twenty-eight for stability.",
                "Donate black sesame, mustard oil, and a black blanket at a Shani temple on Saturdays.",
                "Recite Hanuman Chalisa eleven times every Saturday evening with the spouse.",
                "Avoid signing partnership deeds on Saturdays.",
            ],
        },
        8: {
            "prediction": "Saturn in its pukka ghar grants long life, occult insight, and gain through research, inheritance, insurance, or work in mining, archaeology, or forensic fields. The native is drawn to mystical and metaphysical subjects and may become a quiet authority. Sudden expenses related to chronic illness in the family are possible. Inheritance often arrives after long delay. Health concerns include chronic joint, digestive, and circulatory issues. The native should avoid risky speculation and underground dealings. Spiritual practice undertaken with discipline grants extraordinary peace and protects from the placement's natural tendency toward isolation and prolonged hardship.",
            "remedies": [
                "Donate black sesame, mustard oil, and a black blanket at a Shani temple on Saturdays.",
                "Recite Mahamrityunjaya mantra one hundred and eight times every Saturday.",
                "Feed jaggery and gram flour to a black dog every Saturday for forty-three weeks.",
                "Visit a Shani or Bhairava temple on the eighth lunar day each month.",
            ],
        },
        9: {
            "prediction": "Saturn in the ninth house grants a serious, principled, and somewhat austere temperament with a deep respect for tradition. The father may be strict, distant, or absent in influence. Higher education proceeds with delays but ultimately leads to recognition in scholarly or judicial fields. Long journeys are tiring but professionally rewarding. Religious practice is austere and methodical rather than emotional. Hip, thigh, and joint complaints may appear after fifty. Pilgrimages undertaken with sincerity bring tangible relief. The native should avoid lecturing on morality publicly, as Saturn here works best through quiet example rather than active preaching.",
            "remedies": [
                "Donate black sesame, mustard oil, and a black blanket at a Shani temple on Saturdays.",
                "Touch the feet of the father every Saturday morning if he is alive.",
                "Visit a Shani temple on the ninth lunar day each month.",
                "Recite Hanuman Chalisa eleven times every Saturday evening.",
            ],
        },
        10: {
            "prediction": "Saturn in its second pukka ghar grants a powerful, enduring career built on discipline, patience, and reliability. The native rises through long service, often in government, law, engineering, mining, administration, or large institutions. Recognition arrives slowly but lasts decades. Subordinates respect the native's fairness and fear his standards. Father's profession often shapes the early career. Health concerns include hypertension, joint pain, and chronic overwork. The native should avoid ambitious shortcuts, as Saturn here punishes such attempts severely. After the age of thirty-six, the placement delivers extraordinary professional standing and lasting public respect.",
            "remedies": [
                "Place a small Shani yantra at the workplace facing west.",
                "Donate black sesame, mustard oil, and a black blanket at a Shani temple every Saturday.",
                "Distribute simple meals to labourers or watchmen on every promotion.",
                "Recite Shani Stotra every Saturday evening for steady career growth.",
            ],
        },
        11: {
            "prediction": "Saturn in the eleventh house brings powerful, often older friends and senior advisors who help the native rise through patient effort. Income grows slowly but reliably, with major gains arriving only after the age of thirty-six. Elder siblings prosper and assist generously, though sometimes after their own struggle. Wishes are fulfilled, but only after persistent effort and apparent delays. Hearing, joint, and circulatory issues may appear after fifty. Friendships endure for decades when built on trust and shared work. Avoid borrowing from elder relatives, as such debts strain the most valuable relationships built over years.",
            "remedies": [
                "Donate black sesame, mustard oil, and a black blanket at a Shani temple every Saturday.",
                "Feed jaggery and gram flour to a black dog every Saturday for forty-three weeks.",
                "Avoid lending or borrowing money on Saturdays.",
                "Recite Shani Stotra every Saturday evening for steady gain.",
            ],
        },
        12: {
            "prediction": "Saturn in the twelfth house brings significant expenses through chronic illness, hidden enemies, litigation, and prolonged stays in foreign lands or remote areas. Sleep is often disturbed, and the native may suffer from joint pain, eye complaints, and digestive issues from middle age. Foreign residence and work in solitary, research-oriented, or institutional roles suit well. Hidden adversaries cause harm through bureaucratic delay rather than open conflict. Spiritual practice, especially involving silence and meditation, tames the placement remarkably. Charity given quietly to the elderly, disabled, or imprisoned brings unexpected protection during the native's most difficult years.",
            "remedies": [
                "Donate black sesame, mustard oil, and a black blanket at a Shani temple every Saturday.",
                "Light a mustard oil lamp before a Shani idol every Saturday evening.",
                "Feed jaggery and gram flour to a black dog every Saturday for forty-three weeks.",
                "Avoid keeping broken iron, rusted tools, or torn shoes inside the home.",
            ],
        },
    },
    "Rahu": {
        1: {
            "prediction": "Rahu in the first house grants an unconventional, magnetic personality that stands out in any crowd, often connected to foreign matters, technology, or unusual professions. The native rises suddenly and unexpectedly, sometimes through means his family does not fully understand. Childhood may be marked by health scares or misdiagnosis, particularly involving the head or skin. Marriage to a foreigner or a person of different background is possible. The native should avoid shortcuts, addictions, and deceit, as Rahu here punishes such shortcuts with equally sudden falls. Clean conduct preserves the unusual magnetism that destiny grants.",
            "remedies": [
                "Donate barley, mustard oil, and a black blanket at a temple on Saturdays.",
                "Wear a silver chain around the neck for grounding the placement.",
                "Avoid consuming alcohol, tobacco, or recreational drugs strictly throughout life.",
                "Feed wheat flour mixed with jaggery to ants every morning for forty-three days.",
            ],
        },
        2: {
            "prediction": "Rahu in the second house creates fluctuating family wealth, sudden financial windfalls followed by equally sudden losses, and a tendency toward speech that surprises even the native himself. Income may flow from foreign trade, technology, photography, or unconventional businesses. Family disputes over money are common, particularly involving in-laws. Speech is sometimes deceptive without intention; the native should pause before answering serious questions. Eye, dental, and throat complaints are common. Inheritance, when it arrives, is often entangled in legal complications. Avoiding lies in financial matters preserves both wealth and reputation here for the long term.",
            "remedies": [
                "Donate barley, jaggery, and a coconut at a temple on Saturdays.",
                "Drink water from a silver glass for forty consecutive days.",
                "Avoid speaking lies in financial transactions strictly.",
                "Feed wheat flour balls (atta laddoos) to fish in a flowing river.",
            ],
        },
        3: {
            "prediction": "Rahu in the third house grants exceptional courage, ambition, and ability to thrive in unconventional or technology-driven careers. The native succeeds in writing, technology, foreign trade, aviation, photography, or pioneering ventures. Younger siblings may face delays or be physically distant, often living abroad. Short journeys are frequent and usually profitable. Health concerns include nervous tension, ear complaints, and shoulder injuries. The native should beware of impulsive decisions in correspondence, as Rahu here amplifies the impact of written words considerably. Charitable acts performed quietly multiply the placement's natural power for sudden professional advancement.",
            "remedies": [
                "Donate a coconut and barley at a temple on Saturdays.",
                "Wear a silver ring on the middle finger of the right hand.",
                "Feed wheat flour mixed with jaggery to ants every morning.",
                "Avoid keeping broken electronic items at home for long periods.",
            ],
        },
        4: {
            "prediction": "Rahu in the fourth house creates restlessness in the home, frequent change of residence, and emotional distance from the mother during certain phases of life. The native may live abroad for long periods or own properties in foreign lands. The mother's health needs careful attention, particularly regarding mysterious or hard-to-diagnose ailments. Vehicles change often. Domestic peace is disturbed by hidden emotional currents that the native himself sometimes cannot identify. Educational delays in the early years are common. Cultivating a stable daily routine and meditation tames the placement's natural restlessness considerably over time.",
            "remedies": [
                "Place a silver pot of water in the north-east corner of the home and refresh it daily.",
                "Donate barley, mustard oil, and a coconut at a temple on Saturdays.",
                "Serve your mother with your own hands at least one meal each Saturday.",
                "Avoid keeping idols of deceased ancestors in the bedroom.",
            ],
        },
        5: {
            "prediction": "Rahu in the fifth house creates challenges with conception or with the firstborn child's health, often resolved through medical intervention or spiritual practice. The native is intellectually unconventional, drawn to technology, occult studies, or speculative ventures. Speculative gains are dramatic but inconsistent; disciplined methods are essential. Romantic life before marriage is intense and sometimes secretive. Children, when they arrive, often have unusual talents in technology, arts, or research. Stomach and nervous complaints are typical. Devotional practice undertaken seriously after the age of twenty-eight grants surprising creative breakthroughs and softens the placement's restless intensity.",
            "remedies": [
                "Donate a coconut, barley, and yellow cloth at a temple on Saturdays.",
                "Worship Lord Ganesha before any examination, conception attempt, or speculation.",
                "Avoid speculative trading or gambling on Saturdays.",
                "Feed wheat flour balls to fish in a flowing river on every full moon.",
            ],
        },
        6: {
            "prediction": "Rahu in the sixth house grants extraordinary ability to defeat enemies through unconventional strategy, rise in service through unusual specialisations, and earn through technology, foreign companies, or hidden trades. Maternal uncles either help significantly or oppose openly. Health concerns include mysterious skin ailments, allergies, and digestive issues that doctors struggle to diagnose. Pets brought home, especially exotic or unusual breeds, may cause health problems. The native should avoid lending money to colleagues, as Rahu here turns such transactions into sources of conflict. Service in foreign companies or remote locations brings sudden professional advancement.",
            "remedies": [
                "Donate barley, mustard oil, and a black blanket at a temple on Saturdays.",
                "Feed wheat flour mixed with jaggery to ants every Saturday morning.",
                "Avoid keeping cats or exotic pets in the bedroom.",
                "Recite Durga Saptashati on Saturdays for protection from hidden enemies.",
            ],
        },
        7: {
            "prediction": "Rahu in the seventh house creates an unconventional marriage, often to a foreigner, a person of different culture, or someone met through technology or unusual circumstances. The spouse is independent, often involved in foreign trade, technology, or research. Business partnerships involve foreign collaborators or unconventional sectors and yield sudden gains followed by sudden losses. Marriage may be delayed, hasty, or unusual in form. Health of the spouse may involve mysterious or hard-to-diagnose ailments. Travel abroad is frequent. Loyalty and honesty in marriage protect against the placement's natural tendency toward sudden, dramatic upheaval here.",
            "remedies": [
                "Marry only after the age of twenty-eight for stability.",
                "Donate a coconut, barley, and a blue or black cloth at a temple on Saturdays.",
                "Avoid signing partnership deeds on Saturdays or during eclipses.",
                "Recite Durga Saptashati on Saturdays for harmony in marriage.",
            ],
        },
        8: {
            "prediction": "Rahu in the eighth house grants research ability, occult insight, and gain through inheritance, insurance, or sudden windfalls from unusual sources. The native may face mysterious health issues, accidents, or surgeries that require careful management. Inheritance often arrives through unexpected means or after legal complications. The native is drawn to occult, mystical, or forensic subjects and may earn through such fields. Foreign residence is likely. Hidden enemies cause harm through indirect means. Spiritual practice, particularly mantras for protection, tames the placement remarkably. Avoid risky speculation and underground dealings strictly throughout life.",
            "remedies": [
                "Donate a coconut, barley, and a black cloth at a temple on Saturdays.",
                "Recite Mahamrityunjaya mantra one hundred and eight times every Saturday.",
                "Avoid surgery on Saturdays or during eclipses unless it is an emergency.",
                "Visit a Bhairava temple on the eighth lunar day each month.",
            ],
        },
        9: {
            "prediction": "Rahu in the ninth house creates a complicated relationship with religion, the father, and traditional beliefs. The native may be drawn to foreign philosophies, unconventional spiritual paths, or scientific approaches to traditional questions. Long journeys, especially abroad, are frequent and often life-changing. Higher education abroad or in unconventional fields is likely. The father's health needs attention, particularly hip and circulatory issues. Religious practice undertaken sincerely brings unusually fast spiritual progress. The native should avoid ridiculing traditional beliefs publicly, as Rahu here punishes such arrogance with sudden falls in social standing.",
            "remedies": [
                "Donate barley, jaggery, and a saffron cloth at a temple on Saturdays.",
                "Touch the feet of the father every Saturday morning if he is alive.",
                "Visit a major pilgrimage site once every three years.",
                "Recite Vishnu Sahasranama every Thursday for spiritual stability.",
            ],
        },
        10: {
            "prediction": "Rahu in the tenth house grants sudden professional rise through unconventional means, often in technology, foreign companies, photography, aviation, media, or innovative sectors. Recognition arrives quickly but requires constant maintenance through clean conduct. Father's profession may be unconventional or absent in influence. Subordinates and colleagues respect the native's innovative ability but watch carefully for ethical lapses. Health concerns include hypertension, nervous tension, and overwork. The native should avoid shortcuts and questionable practices, as Rahu here punishes such conduct with sudden public falls. Honest, innovative effort leads to extraordinary professional standing in mid-life.",
            "remedies": [
                "Place a silver coin on the work desk and refresh it monthly.",
                "Donate barley, mustard oil, and a coconut at a temple on Saturdays.",
                "Avoid accepting expensive gifts from clients or superiors.",
                "Recite Durga Saptashati every Saturday for steady career growth.",
            ],
        },
        11: {
            "prediction": "Rahu in the eleventh house brings powerful, often unconventional friends and significant gain through technology, foreign trade, social networks, and innovative ventures. Income flows through multiple unusual streams, with sudden windfalls around eclipses or during long-distance travel. Elder siblings may live abroad or be involved in unconventional professions. Wishes are fulfilled rapidly but require continuous effort to maintain. Friendships built through online or foreign connections prove materially significant. Hearing and circulatory issues may appear after fifty. Honesty in dealings with friends preserves the unusual gains that destiny grants generously here throughout life.",
            "remedies": [
                "Donate barley, jaggery, and a coconut at a temple on Saturdays.",
                "Wear a silver chain around the neck for stability of gains.",
                "Avoid lending money to friends on Saturdays without written agreement.",
                "Feed wheat flour mixed with jaggery to ants every morning for forty-three days.",
            ],
        },
        12: {
            "prediction": "Rahu in its pukka ghar grants spiritual depth combined with significant expenses on foreign travel, technology, hidden charitable causes, and unusual investments. The native often lives abroad and may earn through foreign companies, research, or behind-the-scenes work. Sleep is often disturbed by vivid, sometimes prophetic dreams. Hidden enemies cause harm through bureaucratic delay rather than open conflict. Eye, foot, and nervous complaints may appear after forty. Spiritual practice, particularly involving silence and mantra, yields extraordinary progress. Charity given anonymously to foreign causes or distant strangers brings unexpected protection during difficult years.",
            "remedies": [
                "Donate barley, mustard oil, and a coconut at a temple before any foreign journey.",
                "Sleep with the head facing east and avoid the south-west direction strictly.",
                "Recite Durga Saptashati on Saturdays for protection during travel.",
                "Avoid keeping idols of unfamiliar deities or unusual artefacts in the bedroom.",
            ],
        },
    },
    "Ketu": {
        1: {
            "prediction": "Ketu in the first house creates a mystical, somewhat detached, and unusually intuitive native who often appears wiser than his years. Childhood may be marked by health concerns or feelings of being misunderstood by the family. The native is drawn to spirituality, occult subjects, research, or solitary professions from an early age. Marriage may be delayed or to a partner from a very different background. Health concerns include skin issues, headaches, and mysterious ailments that resist conventional diagnosis. Sons born to the native may face health challenges in their early years. Spiritual practice tames the placement.",
            "remedies": [
                "Donate a multicoloured blanket and sesame seeds at a temple on Tuesdays.",
                "Wear a silver chain around the neck for grounding the placement.",
                "Feed a stray dog with sweet bread every Tuesday for forty-three weeks.",
                "Avoid keeping idols of fierce deities in the bedroom.",
            ],
        },
        2: {
            "prediction": "Ketu in the second house creates fluctuating family wealth, secretive speech, and a tendency to lose accumulated savings through unexpected expenses on relatives or hidden causes. The native may speak less than expected, and what he does say sometimes carries unusual depth or mysticism. Eye, dental, and speech-related issues may appear from middle age. Education may proceed through unconventional means. Inheritance, when it arrives, is often modest or comes after disputes. The native should avoid lending money to in-laws, as such transactions almost always end with quiet, slow loss rather than open conflict.",
            "remedies": [
                "Donate sesame seeds, a multicoloured cloth, and a coconut at a temple on Tuesdays.",
                "Drink water from a silver glass for forty consecutive days.",
                "Avoid harsh speech at the dining table, especially about relatives.",
                "Feed sweet bread to a stray dog every Tuesday for forty-three weeks.",
            ],
        },
        3: {
            "prediction": "Ketu in the third house grants courage developed through inner reflection rather than outward aggression, intuitive writing ability, and an interest in mystical or research-oriented subjects. Younger siblings may live abroad, follow unusual professions, or face health challenges. Short journeys are frequent and often have spiritual or research purposes. Income flows from writing, research, technology, or behind-the-scenes work. Health concerns include nervous tension, ear complaints, and shoulder injuries. The native should avoid impulsive correspondence, particularly written communication sent during emotional turbulence, as such messages later cause unexpected complications.",
            "remedies": [
                "Donate sesame seeds and a multicoloured cloth at a temple on Tuesdays.",
                "Feed sweet bread to a stray dog every Tuesday for forty-three weeks.",
                "Recite Ganesha Atharvashirsha every Tuesday for protection.",
                "Avoid keeping pet birds or exotic animals in the bedroom.",
            ],
        },
        4: {
            "prediction": "Ketu in the fourth house creates emotional detachment from the home and the mother during certain phases of life, frequent change of residence, and a tendency to live abroad or in unusual settings. The mother's health needs careful attention, particularly regarding chronic or mysterious ailments. Vehicles bring more trouble than joy. Domestic peace is disturbed by hidden emotional currents the native himself sometimes cannot identify. Properties acquired in haste may be lost through unexpected circumstances. Spiritual practice undertaken at home strengthens the placement and gradually creates the inner stability that the outer environment cannot provide.",
            "remedies": [
                "Place a silver pot of water in the north-east corner of the home and refresh it daily.",
                "Donate sesame seeds, a multicoloured cloth, and a coconut at a temple on Tuesdays.",
                "Serve your mother with your own hands at least one meal each Tuesday.",
                "Avoid keeping idols of deceased ancestors in the bedroom.",
            ],
        },
        5: {
            "prediction": "Ketu in the fifth house creates challenges with sons, particularly the firstborn male child's health or behaviour, often resolved through medical intervention or spiritual practice. The native is intuitively intelligent, drawn to mystical studies, occult research, or speculative ventures. Speculative gains are unreliable; spiritual practice yields far better returns. Romantic life before marriage may involve secrecy or unusual circumstances. Children, when they arrive, often have unusual talents but require careful guidance. Stomach and nervous complaints are common. Mantra recitation undertaken seriously grants surprising creative and intuitive breakthroughs over the years.",
            "remedies": [
                "Worship Lord Ganesha before any examination or important decision.",
                "Donate sesame seeds, a multicoloured cloth, and yellow sweets at a temple on Tuesdays.",
                "Feed sweet bread to a stray dog every Tuesday for forty-three weeks.",
                "Avoid speculative trading or gambling on Tuesdays.",
            ],
        },
        6: {
            "prediction": "Ketu in its pukka ghar grants extraordinary ability to defeat enemies through unconventional means, rise in service through specialised skills, and earn through medicine, research, technology, or healing professions. Maternal uncles either help significantly or remain emotionally distant. Health concerns include mysterious skin ailments, allergies, and digestive issues that doctors struggle to diagnose. Pets, especially dogs, suit the household and prove protective. The native should avoid lending money to colleagues, as such transactions create unexpected complications. Service in healing, research, or spiritual professions brings unusual professional satisfaction throughout life.",
            "remedies": [
                "Donate sesame seeds, a multicoloured cloth, and a coconut at a temple on Tuesdays.",
                "Feed sweet bread to a stray dog every Tuesday for forty-three weeks.",
                "Recite Hanuman Chalisa eleven times every Tuesday evening.",
                "Avoid keeping cats in the bedroom.",
            ],
        },
        7: {
            "prediction": "Ketu in the seventh house creates an unconventional marriage, often to a partner with strong spiritual inclinations or a very different background. The spouse may be detached, mysterious, or focused on inner pursuits rather than worldly success. Business partnerships rarely flourish; the native does best working alone or in research-oriented collaboration. Marriage may be delayed or arrive through unusual circumstances. Health of the spouse may involve mysterious or hard-to-diagnose ailments. Travel abroad with the spouse is possible. Loyalty, patience, and shared spiritual practice protect the marriage from the placement's natural tendency toward emotional drift.",
            "remedies": [
                "Marry only after the age of twenty-eight for stability.",
                "Donate sesame seeds, a multicoloured cloth, and a coconut at a temple on Tuesdays.",
                "Worship Lord Ganesha with the spouse before any major decision.",
                "Avoid signing partnership deeds on Tuesdays or during eclipses.",
            ],
        },
        8: {
            "prediction": "Ketu in the eighth house grants extraordinary research ability, occult insight, and gain through inheritance, insurance, or sudden windfalls from unusual sources. The native may face mysterious health issues, accidents, or surgeries that require careful management. Inheritance often arrives through unexpected means or after legal complications. The native is deeply drawn to occult, mystical, or forensic subjects. Foreign residence is likely. Hidden enemies cause harm through indirect means rather than open conflict. Spiritual practice, particularly mantras for protection, tames the placement remarkably. Avoid risky speculation, underground dealings, and dangerous sports throughout life.",
            "remedies": [
                "Donate sesame seeds, a multicoloured cloth, and a coconut at a temple on Tuesdays.",
                "Recite Mahamrityunjaya mantra one hundred and eight times every Tuesday.",
                "Avoid surgery on Tuesdays or during eclipses unless it is an emergency.",
                "Visit a Bhairava or Ganesha temple on the eighth lunar day each month.",
            ],
        },
        9: {
            "prediction": "Ketu in the ninth house creates a deeply spiritual, philosophical, and somewhat unconventional approach to religion and traditional beliefs. The father may be distant, absent in influence, or pursue an unusual spiritual path himself. Higher education in philosophy, religion, or occult subjects suits well. Long journeys, especially to remote pilgrimage sites or for spiritual purposes, are frequent and transformative. The native may become a teacher of spiritual subjects in later life. Hip, thigh, and joint complaints may appear after fifty. Charity given quietly to spiritual seekers or wandering ascetics multiplies blessings remarkably here.",
            "remedies": [
                "Donate sesame seeds, a multicoloured cloth, and saffron at a temple on Tuesdays.",
                "Visit a major pilgrimage site, especially a remote one, every few years.",
                "Touch the feet of the father every Tuesday morning if he is alive.",
                "Recite Ganesha Atharvashirsha every Tuesday morning.",
            ],
        },
        10: {
            "prediction": "Ketu in the tenth house grants a successful career in research, technology, healing, occult, or behind-the-scenes professions where deep specialisation is valued. Recognition arrives through quiet excellence rather than open self-promotion. Father's profession may be unconventional or absent in influence. Subordinates respect the native's depth and quiet authority. Promotions arrive through unusual circumstances. Health concerns include nervous tension, mysterious chronic complaints, and overwork. The native should avoid office politics, as Ketu here works best when the native focuses on substance rather than visibility, gradually building an unusual professional reputation over decades.",
            "remedies": [
                "Place a small Ganesha idol on the work desk and offer flowers weekly.",
                "Donate sesame seeds, a multicoloured cloth, and a coconut at a temple on Tuesdays.",
                "Avoid accepting expensive gifts from superiors or business partners.",
                "Recite Hanuman Chalisa every Tuesday evening for steady career growth.",
            ],
        },
        11: {
            "prediction": "Ketu in the eleventh house brings unusual friends, often from spiritual, research, or foreign backgrounds, and gain through unconventional ventures, hidden investments, or behind-the-scenes work. Income flows through multiple streams that do not always make sense to outsiders. Elder siblings may live abroad, follow unusual professions, or be drawn to spiritual paths. Wishes are fulfilled, but in unexpected forms that the native must learn to recognise. Hearing and nervous complaints may appear after fifty. Friendships built on shared spiritual or research interests endure for decades; superficial friendships dissolve quickly here.",
            "remedies": [
                "Donate sesame seeds, a multicoloured cloth, and a coconut at a temple on Tuesdays.",
                "Wear a silver chain around the neck for stability of gains.",
                "Avoid lending money to friends on Tuesdays without written agreement.",
                "Feed sweet bread to a stray dog every Tuesday for forty-three weeks.",
            ],
        },
        12: {
            "prediction": "Ketu in the twelfth house grants extraordinary spiritual depth, intuition, and a natural inclination toward meditation, monastic life, or service to the dying and the sick. The native may live abroad or work in monasteries, hospitals, ashrams, or charitable institutions. Sleep is often filled with vivid, sometimes prophetic dreams. Hidden enemies cause harm through bureaucratic delay rather than open conflict. Eye, foot, and nervous complaints may appear after forty. Donations made anonymously to spiritual causes, the dying, or wandering ascetics bring unexpected blessings and grant extraordinary peace in the final phase of life.",
            "remedies": [
                "Donate sesame seeds, a multicoloured cloth, and a coconut at a temple before any foreign journey.",
                "Recite Ganesha Atharvashirsha every Tuesday morning.",
                "Sleep with the head facing east and avoid the south-west direction strictly.",
                "Visit a remote pilgrimage site at least once every five years.",
            ],
        },
    },
}
