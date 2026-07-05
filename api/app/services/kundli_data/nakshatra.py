"""Nakshatra + Nakshatra-pada interpretive text.

Split out of the former 1895-line kundli_data.py god-module (data only).
Re-exported via kundli_data/__init__.py so imports are unchanged."""



# ── NAKSHATRA DATA (27 nakshatras) ───────────────────────────────────────────

NAKSHATRA_DATA = {
    0: {
        "name": "Ashwini",
        "lord": "Ketu",
        "prediction": "You are quick, energetic, and always eager to start new things. You have a natural healing ability and a youthful appearance that stays with you throughout life. You are adventurous and love speed and movement. Your intelligence is sharp and you grasp things quickly. You are independent and prefer to lead rather than follow. Healthcare, transportation, and new ventures are favorable for you.",
    },
    1: {
        "name": "Bharani",
        "lord": "Venus",
        "prediction": "You are dutiful, responsible, and carry burdens with grace. You have strong creative abilities and a deep connection to the cycles of life. You are passionate and determined, with a strong sense of morality. You may face many transformations in life that make you stronger. Creative arts, law, and healthcare are favorable fields.",
    },
    2: {
        "name": "Krittika",
        "lord": "Sun",
        "prediction": "You are sharp, determined, and have a fiery temperament. You are a natural leader with a commanding presence. You are truthful and straightforward, sometimes to the point of being harsh. You have strong appetites and a love for food. Military, cooking, tailoring, and fire-related industries suit you well.",
    },
    3: {
        "name": "Rohini",
        "lord": "Moon",
        "prediction": "You are attractive, charming, and have a magnetic personality. You love beauty, luxury, and the finer things in life. You are creative and have good taste in art, music, and fashion. You are emotionally rich and seek comfort and stability. Agriculture, fashion, cosmetics, and entertainment are favorable fields.",
    },
    4: {
        "name": "Mrigashira",
        "lord": "Mars",
        "prediction": "You are curious, searching, and always seeking knowledge. You have a gentle nature despite Mars being your lord. You are creative and have a talent for music and writing. You may travel frequently in search of new experiences. Research, travel, textiles, and writing are favorable careers.",
    },
    5: {
        "name": "Ardra",
        "lord": "Rahu",
        "prediction": "You have a sharp intellect and can penetrate to the core of any matter. You may experience significant transformations and upheavals in life that ultimately lead to growth. You are analytical and research-oriented. You can be emotionally turbulent but have great resilience. Technology, research, pharmaceuticals, and electronics suit you.",
    },
    6: {
        "name": "Punarvasu",
        "lord": "Jupiter",
        "prediction": "You have the ability to bounce back from adversity with renewed optimism. You are philosophical, generous, and have a positive outlook on life. You are intellectually gifted and make an excellent teacher. You value home and family deeply. Education, counseling, publishing, and spiritual work are favorable.",
    },
    7: {
        "name": "Pushya",
        "lord": "Saturn",
        "prediction": "You are nourishing, protective, and have a strong sense of duty. This is considered one of the most auspicious nakshatras. You are disciplined, hardworking, and devoted to your goals. You have a calm, composed demeanor that others find reassuring. Government service, dairy, education, and religious work favor you.",
    },
    8: {
        "name": "Ashlesha",
        "lord": "Mercury",
        "prediction": "You are intelligent, perceptive, and have a magnetic quality. You are skilled in communication and can be persuasive. You have deep emotional awareness and psychological insight. You may be secretive and keep your true feelings hidden. Medicine, psychology, astrology, and research suit you well.",
    },
    9: {
        "name": "Magha",
        "lord": "Ketu",
        "prediction": "You have a regal bearing and strong ancestral connections. You are proud, ambitious, and seek positions of authority and respect. You have a deep connection to your lineage and traditions. You are generous and command respect from others. Government, administration, history, and ancestral businesses favor you.",
    },
    10: {
        "name": "Purva Phalguni",
        "lord": "Venus",
        "prediction": "You are creative, charming, and love life's pleasures. You have a natural talent for the arts and entertainment. You are generous, warm-hearted, and enjoy socializing. You seek comfort and luxury and have refined tastes. Entertainment, arts, hospitality, and creative fields are favorable.",
    },
    11: {
        "name": "Uttara Phalguni",
        "lord": "Sun",
        "prediction": "You are helpful, charitable, and have leadership qualities. You are reliable and always willing to extend a helping hand. You have a strong sense of social responsibility and work for the welfare of others. You gain respect through your service and integrity. Social work, management, counseling, and government service suit you.",
    },
    12: {
        "name": "Hasta",
        "lord": "Moon",
        "prediction": "You are skilled with your hands and have a talent for craftsmanship. You are resourceful, adaptable, and quick-witted. You have a pleasant personality and a good sense of humor. You are detail-oriented and can master any manual skill. Handicrafts, healing, magic, and skilled trades are favorable.",
    },
    13: {
        "name": "Chitra",
        "lord": "Mars",
        "prediction": "You have a strong aesthetic sense and appreciate beauty in all forms. You are creative, dynamic, and have a striking appearance. You are skilled in architecture, design, and visual arts. You may face challenges in personal relationships but achieve great success professionally. Design, architecture, jewelry, and fashion suit you.",
    },
    14: {
        "name": "Swati",
        "lord": "Rahu",
        "prediction": "You are independent, flexible, and able to adapt to changing circumstances. You value freedom and may resist being tied down. You are diplomatic and skilled in business and trade. You are self-made and achieve success through your own efforts. Business, trade, travel, and independent ventures favor you.",
    },
    15: {
        "name": "Vishakha",
        "lord": "Jupiter",
        "prediction": "You are determined, goal-oriented, and have incredible focus. You are willing to sacrifice personal comfort to achieve your ambitions. You are intelligent and have a philosophical bent of mind. You may face periods of isolation but ultimately achieve great success. Research, religion, politics, and goal-oriented careers suit you.",
    },
    16: {
        "name": "Anuradha",
        "lord": "Saturn",
        "prediction": "You have profound faith in God. This is the reason why you do not get upset in any difficult situation. Hurdles may come in life, but they will not shake you from your path because you are a hard worker. You will start earning at a very young age. Your nature is quite strugglesome. For mental peace, you have to put regular efforts. As you are quite straightforward, you say everything that comes to your mind. Whenever you try to help someone, you do it with all your heart. You do not show off. As you stay quite serious about your aim, you manage to be successful after many hurdles. Business skills are carried by you from your childhood. If you work in a job, you will make all your seniors favor you. You are disciplined and give importance to principles of life.",
    },
    17: {
        "name": "Jyeshtha",
        "lord": "Mercury",
        "prediction": "You are intellectual, protective, and have a commanding presence. You take on responsibilities naturally and protect those who depend on you. You are courageous and resourceful, especially in times of crisis. You may face rivalry from others but overcome it through intelligence. Administration, defense, communication, and leadership roles suit you.",
    },
    18: {
        "name": "Mula",
        "lord": "Ketu",
        "prediction": "You are a seeker of truth who wants to get to the root of all matters. You may experience sudden reversals and transformations that ultimately lead to spiritual growth. You are philosophically inclined and question established beliefs. You have a rebellious streak and cannot be controlled. Research, medicine, herbal sciences, and spiritual pursuits favor you.",
    },
    19: {
        "name": "Purva Ashadha",
        "lord": "Venus",
        "prediction": "You are optimistic, invincible, and have a purifying influence on others. You are ambitious and have the ability to inspire and motivate people. You are persuasive and have strong convictions. You are drawn to water and may benefit from water-related activities. Shipping, aquaculture, entertainment, and public speaking suit you.",
    },
    20: {
        "name": "Uttara Ashadha",
        "lord": "Sun",
        "prediction": "You have an enduring quality that brings ultimate victory. You are patient, principled, and achieve success through persistent effort. You are respected for your integrity and fairness. You may rise to positions of great authority later in life. Government, law, defense, and leadership positions favor you.",
    },
    21: {
        "name": "Shravana",
        "lord": "Moon",
        "prediction": "You are an excellent listener and learner. You acquire knowledge through listening and observation. You are well-connected and skilled in communication and media. You have a scholarly disposition and value education highly. Teaching, media, counseling, and travel industries favor you.",
    },
    22: {
        "name": "Dhanishtha",
        "lord": "Mars",
        "prediction": "You are wealthy, musical, and have a talent for rhythm and beats. You are generous and enjoy sharing your abundance. You are ambitious and can excel in both material and spiritual pursuits. Music, real estate, surgery, and sports are favorable fields.",
    },
    23: {
        "name": "Shatabhisha",
        "lord": "Rahu",
        "prediction": "You are a healer with deep knowledge of mystical arts. You are independent, secretive, and prefer solitude. You have a keen interest in alternative medicine and astrology. You are truthful and do not compromise on your principles. Medicine, pharmaceuticals, astrology, and technology suit you.",
    },
    24: {
        "name": "Purva Bhadrapada",
        "lord": "Jupiter",
        "prediction": "You have a dual nature — passionate yet spiritual. You are intense and capable of great sacrifice for higher ideals. You are intelligent, philosophical, and drawn to mystical knowledge. You may undergo significant spiritual transformation. Spiritual teaching, astrology, research, and philanthropy favor you.",
    },
    25: {
        "name": "Uttara Bhadrapada",
        "lord": "Saturn",
        "prediction": "You are wise, disciplined, and have deep spiritual insight. You are compassionate and work for the welfare of others. You have excellent self-control and endurance. You are trustworthy and keep secrets well. Charity, counseling, yoga, and spiritual pursuits favor you.",
    },
    26: {
        "name": "Revati",
        "lord": "Mercury",
        "prediction": "You are creative, nurturing, and have a love for animals and the natural world. You are gentle, kind, and have a protective nature. You are drawn to spiritual and creative pursuits. You may have the ability to provide safe passage and guidance to others. Creative arts, animal husbandry, travel, and spiritual work favor you.",
    },
}


# ── NAKSHATRA × PADA (27 nakshatras × 4 padas = 108 entries) ────────────────
# Each pada falls in a specific Navamsa (D9) sign, which gives that pada its
# distinctive sub-flavor on top of the parent nakshatra's nature. Lookup:
# NAKSHATRA_PADA_DATA[nakshatra_num][pada_num] → paragraph string.

NAKSHATRA_PADA_DATA = {
    0: {  # Ashwini
        1: "Pada 1 (Aries navamsa): You are the pure pioneer of Ashwini, charging into new ventures with raw speed and competitive fire. Aries navamsa doubles the Mars-like courage, making you a natural starter, athlete, or first-responder type. Patience is your weak spot, but few can match your initiative.",
        2: "Pada 2 (Taurus navamsa): You carry Ashwini's healing impulse but channel it through steady, sensory hands — medicine, food, bodywork, or anything tangible suits you. Taurus navamsa softens the rush, giving you persistence and an eye for comfort and beauty. Loved ones find you reliable beneath the restless surface.",
        3: "Pada 3 (Gemini navamsa): You are the curious explorer of Ashwini, quick-witted and endlessly inquisitive about how things work. Gemini navamsa makes you a natural communicator, teacher, or trader who thrives on variety and short journeys. Focus is your challenge — many ideas, less follow-through.",
        4: "Pada 4 (Cancer navamsa): You are the most emotionally tuned Ashwini, drawn to caring professions, nursing, or family-anchored work. Cancer navamsa exalts your healing instinct and gives a protective, almost maternal quality to your speed. You move fast when those you love are at stake.",
    },
    1: {  # Bharani
        1: "Pada 1 (Leo navamsa): You carry Bharani's transformative weight with regal flair, often stepping into leadership roles that demand emotional courage. Leo navamsa adds charisma, creative drive, and a need to be seen for what you carry. Pride and passion shape both your career and your loves.",
        2: "Pada 2 (Virgo navamsa): You are the practical caretaker of Bharani, methodical about the burdens you choose to bear — health, service, detail-rich work suits you. Virgo navamsa tempers the Venus sensuality with discipline and a sharp critical eye. You give much but expect order in return.",
        3: "Pada 3 (Libra navamsa): You channel Bharani's intensity through partnerships and aesthetics, often working in art, design, counselling, or law. Libra navamsa makes you charming and diplomatic, yet inwardly you wrestle with strong desires and the cost of pleasing others. Relationships are your central stage.",
        4: "Pada 4 (Scorpio navamsa): You are Bharani at full volume — secretive, magnetic, and unafraid of life's darker chapters. Scorpio navamsa amplifies the themes of birth, death, and transformation, drawing you toward research, occult studies, or crisis work. Love runs deep but possessive.",
    },
    2: {  # Krittika
        1: "Pada 1 (Sagittarius navamsa): You wield Krittika's fiery sharpness with philosophical breadth, making you a natural teacher, preacher, or principled critic. Sagittarius navamsa expands your sense of purpose and gives you a wandering, truth-seeking streak. You cut through illusion in the name of higher ideals.",
        2: "Pada 2 (Capricorn navamsa): You are the disciplined achiever of Krittika, climbing through structured fields like military, administration, or engineering. Capricorn navamsa adds patience and ambition to the Sun's leadership, making your rise slow but unshakeable. Duty often outweighs warmth.",
        3: "Pada 3 (Aquarius navamsa): You apply Krittika's incisive mind to unconventional fields — technology, reform, or social causes that demand a sharp blade. Aquarius navamsa gives a detached, future-leaning intellect that questions every authority, even your own. Friendships matter more than family expectations.",
        4: "Pada 4 (Pisces navamsa): You soften Krittika's flame with intuition and compassion, often drawn to spiritual teaching, art, or healing. Pisces navamsa blurs the razor's edge into something more forgiving, but you can still cut sharply when truth demands it. Inner life is rich and dreamlike.",
    },
    3: {  # Rohini
        1: "Pada 1 (Aries navamsa): You carry Rohini's beauty and charm with surprising boldness and independence. Aries navamsa makes you assertive in love and ambitious in creative or business pursuits, often leading rather than following. You enjoy comfort but will fight to build it on your own terms.",
        2: "Pada 2 (Taurus navamsa): You are the quintessential Rohini — sensual, artistic, deeply tied to land, food, music, and the pleasures of stable life. Taurus navamsa doubles the Moon's love of beauty, giving you magnetic appeal and a steady, possessive heart. Wealth tends to accumulate naturally.",
        3: "Pada 3 (Gemini navamsa): You blend Rohini's charm with intellectual playfulness, making you a gifted communicator, writer, or performer. Gemini navamsa adds wit and curiosity to the natural beauty, drawing many admirers and conversations. Constancy in love can be a quiet challenge.",
        4: "Pada 4 (Cancer navamsa): You are deeply nurturing, family-centred, and emotionally intuitive — Rohini's fertile core in its purest form. Cancer navamsa, where the Moon is exalted, gives you remarkable empathy and a strong pull toward home, motherhood, or caregiving work. Memories shape you profoundly.",
    },
    4: {  # Mrigashira
        1: "Pada 1 (Leo navamsa): You are the proud seeker of Mrigashira, restless for experiences that match your sense of self-worth. Leo navamsa adds creative flair and a desire for recognition, making you well suited to performance, design, or leadership in exploratory fields. Curiosity wears a confident face.",
        2: "Pada 2 (Virgo navamsa): You channel Mrigashira's seeking nature into careful research, analysis, or skilled craft. Virgo navamsa sharpens your discrimination and gives you a quiet perfectionism, often in writing, science, or healing. You prefer depth over noise in both work and love.",
        3: "Pada 3 (Libra navamsa): You search for the perfect partner, the perfect setting, the perfect aesthetic — Mrigashira's gentle questing meets Venusian refinement. Libra navamsa makes you graceful, sociable, and drawn to the arts or counselling. Indecision is the price of seeing every angle.",
        4: "Pada 4 (Scorpio navamsa): You are the most intense Mrigashira, hunting beneath surfaces for hidden truths. Scorpio navamsa adds psychological depth and emotional secrecy to the gentle deer, making you well suited to investigation, therapy, or the occult. Loyalty in love is fierce and unconditional.",
    },
    5: {  # Ardra
        1: "Pada 1 (Sagittarius navamsa): You experience Ardra's storms as searches for meaning, often becoming a philosopher, teacher, or restless traveller. Sagittarius navamsa lifts the tear into a quest for truth, giving you an expansive, sometimes preachy, intellect. Crises tend to deepen your worldview.",
        2: "Pada 2 (Capricorn navamsa): You channel Ardra's intensity into hard, structured work — engineering, business, or any field that rewards endurance under pressure. Capricorn navamsa gives you ambition and grit, but you carry burdens silently. Success comes through long climbs over many obstacles.",
        3: "Pada 3 (Aquarius navamsa): You are the most innovative Ardra, drawn to technology, science, or social transformation. Aquarius navamsa channels Rahu's electricity into futuristic thinking, often making you ahead of your peers. You feel deeply but appear cool and intellectually detached.",
        4: "Pada 4 (Pisces navamsa): You experience Ardra's tears as compassion for the world's pain, often turning toward healing, mysticism, or art. Pisces navamsa dissolves boundaries, giving you intuitive depth and a tendency to absorb others' moods. Solitude restores what crowds drain.",
    },
    6: {  # Punarvasu
        1: "Pada 1 (Aries navamsa): You embody Punarvasu's optimism with pioneering energy, always ready to begin again after setbacks. Aries navamsa adds courage and a sportsman's spirit, suiting you to leadership in education, travel, or new ventures. Your faith in fresh starts is contagious.",
        2: "Pada 2 (Taurus navamsa): You carry Punarvasu's wisdom into stable, productive work — agriculture, finance, teaching, or anything that grows over time. Taurus navamsa grounds Jupiter's expansion into tangible wealth and family comfort. You are gentle, generous, and quietly devoted.",
        3: "Pada 3 (Gemini navamsa): You are the philosophical communicator of Punarvasu, naturally suited to teaching, writing, or guiding others through change. Gemini navamsa, ruled by Mercury, doubles the intellectual breadth and gives you a love of stories and short journeys. You make complex ideas friendly.",
        4: "Pada 4 (Cancer navamsa): You are deeply nurturing and family-oriented — Punarvasu's homecoming theme in its softest form. Cancer navamsa, where Jupiter is exalted, fills you with wisdom-tinged compassion and a love of tradition. You are the emotional anchor others return to.",
    },
    7: {  # Pushya
        1: "Pada 1 (Leo navamsa): You wear Pushya's nurturing nature with leadership flair, often becoming the protective head of a family, team, or community. Leo navamsa adds confidence, generosity, and a love of being appreciated for what you give. Public roles suit you well.",
        2: "Pada 2 (Virgo navamsa): You are the most service-driven Pushya, methodical and devoted to caring work — medicine, teaching, dietetics, or detailed administration. Virgo navamsa sharpens your discernment and gives you a quietly perfectionist heart. You nurture by getting the small things right.",
        3: "Pada 3 (Libra navamsa): You channel Pushya's warmth into partnerships, counselling, and creating beautiful, harmonious spaces. Libra navamsa makes you diplomatic and aesthetically refined, drawn to fields like hospitality, design, or human resources. Marriage and close alliances shape your path.",
        4: "Pada 4 (Scorpio navamsa): You nurture with intensity and depth, often supporting others through their hardest passages. Scorpio navamsa adds psychological insight and emotional secrecy to Pushya's caring nature, suiting you to therapy, research, or crisis work. Trust, once given, runs absolute.",
    },
    8: {  # Ashlesha
        1: "Pada 1 (Sagittarius navamsa): You channel Ashlesha's hypnotic intelligence into philosophy, teaching, or strategic counsel. Sagittarius navamsa softens the serpent's coil with optimism and broad vision, making you a persuasive guide. You see through people quickly but prefer expansive over cynical.",
        2: "Pada 2 (Capricorn navamsa): You are the strategist of Ashlesha — patient, calculating, and quietly ambitious. Capricorn navamsa channels Mercury's cunning into long-term professional climbs, often in business, politics, or research. You play the long game better than most.",
        3: "Pada 3 (Aquarius navamsa): You apply Ashlesha's depth to unconventional or technical fields — coding, research, analysis, or covert work. Aquarius navamsa cools the emotional intensity into intellectual detachment, giving you a unique, sometimes eccentric outlook. Friendships can be intense but selective.",
        4: "Pada 4 (Pisces navamsa): You are the mystical Ashlesha, drawn to the occult, dreams, and the hidden currents of life. Pisces navamsa softens the serpent into something almost shamanic, suiting you to healing, art, or spiritual practice. Boundaries blur easily — solitude is medicine.",
    },
    9: {  # Magha
        1: "Pada 1 (Aries navamsa): You carry Magha's regal authority with bold, pioneering energy, often stepping into leadership early. Aries navamsa fuels ambition and a willingness to fight for your throne, suiting you to entrepreneurship, military, or competitive fields. Ancestral pride runs strong.",
        2: "Pada 2 (Taurus navamsa): You channel Magha's nobility into tangible legacy — wealth, land, art, or family enterprises that last generations. Taurus navamsa grounds the Ketu intensity into steady accumulation and refined taste. You honour ancestors by building something they would recognise.",
        3: "Pada 3 (Gemini navamsa): You are the eloquent ambassador of Magha, using words and ideas to uphold tradition and influence others. Gemini navamsa adds intellectual sparkle and versatility, suiting you to writing, teaching, or politics. Lineage matters, but you retell its stories in modern language.",
        4: "Pada 4 (Cancer navamsa): You are deeply tied to family roots and ancestral memory — Magha's most emotional pada. Cancer navamsa adds nurturing instincts and a strong sense of belonging, often making home or heritage your central project. Caring for elders and traditions feels natural.",
    },
    10: {  # Purva Phalguni
        1: "Pada 1 (Leo navamsa): You embody Purva Phalguni's pleasure-loving spirit with full theatrical confidence. Leo navamsa amplifies Venus into a magnetic, performance-ready persona, well suited to entertainment, fashion, or creative leadership. Romance and recognition are major themes.",
        2: "Pada 2 (Virgo navamsa): You channel Purva Phalguni's creativity into refined craft and skilled work — design, beauty, hospitality, or healing arts. Virgo navamsa adds discernment and a quiet perfectionism to the playful nature. You take pleasure seriously and make it look effortless.",
        3: "Pada 3 (Libra navamsa): You are Venus doubled — graceful, romantic, and naturally drawn to partnership and the arts. Libra navamsa makes you a diplomat and aesthete, suited to design, counselling, or anything involving harmony between people. Love shapes your story more than career.",
        4: "Pada 4 (Scorpio navamsa): You experience Purva Phalguni's romance with intensity, secrecy, and emotional depth. Scorpio navamsa transforms casual pleasure into transformative passion, suiting you to performing arts, occult studies, or therapy. Love is rarely lukewarm.",
    },
    11: {  # Uttara Phalguni
        1: "Pada 1 (Sagittarius navamsa): You combine Uttara Phalguni's sense of duty with broad philosophical vision, making you a principled leader, teacher, or counsellor. Sagittarius navamsa adds optimism and ethical clarity to the Sun's authority. Friendships and contracts are guided by higher ideals.",
        2: "Pada 2 (Capricorn navamsa): You are the organised contract-keeper, climbing steadily through structured careers like law, administration, or finance. Capricorn navamsa intensifies Uttara Phalguni's reliability and patience, making you the person others trust with serious responsibilities. Marriage tends toward the practical.",
        3: "Pada 3 (Aquarius navamsa): You apply Uttara Phalguni's service ethic to humanitarian, technological, or social causes. Aquarius navamsa adds an unconventional, future-leaning streak that values fairness over personal gain. Friendships often outshine romance in importance.",
        4: "Pada 4 (Pisces navamsa): You serve with compassion and quiet devotion, drawn to caring professions, healing, or spiritual community. Pisces navamsa softens the Sun's authority into gentle generosity, sometimes at the cost of clear personal boundaries. You give more than you ask.",
    },
    12: {  # Hasta
        1: "Pada 1 (Aries navamsa): You apply Hasta's craft and skill with bold initiative, often starting your own ventures or leading hands-on teams. Aries navamsa adds drive and competitive edge to manual or technical mastery. You build quickly and dislike waiting for permission.",
        2: "Pada 2 (Taurus navamsa): You are the master craftsperson of Hasta — patient, sensual, and devoted to creating beautiful, useful things. Taurus navamsa grounds the Moon's skill into tangible art, food, agriculture, or fine craft. Wealth grows through what your hands shape.",
        3: "Pada 3 (Gemini navamsa): You combine Hasta's manual dexterity with intellectual quickness, suiting you to writing, design, technology, or detailed analytical work. Gemini navamsa, ruled by Mercury (Hasta's own lord), makes this pada doubly skilled with both hands and mind. Communication is a gift.",
        4: "Pada 4 (Cancer navamsa): You bring Hasta's craft into nurturing, home-based, or caring expressions — cooking, healing, teaching children, or family business. Cancer navamsa adds emotional sensitivity and intuitive timing to your skilled hands. Tradition and memory inform your work.",
    },
    13: {  # Chitra
        1: "Pada 1 (Leo navamsa): You shine as Chitra's brilliant designer — confident, creative, and drawn to the spotlight. Leo navamsa amplifies the jewel-like quality, suiting you to architecture, fashion, performance, or any visible creative leadership. Style is your signature.",
        2: "Pada 2 (Virgo navamsa): You channel Chitra's artistic eye into precise, technical, or healing fields — graphic design, surgery, engineering, or fine craft. Virgo navamsa sharpens the perfectionist streak and gives you remarkable attention to detail. Beauty meets function in your work.",
        3: "Pada 3 (Libra navamsa): You are the designer of harmony itself, drawn to interior design, fashion, partnerships, or diplomatic roles. Libra navamsa softens Mars's intensity into refined Venusian taste, making you charming and aesthetically gifted. Relationships often shape your creative direction.",
        4: "Pada 4 (Scorpio navamsa): You experience Chitra's brilliance as intensity and depth, often in transformative or mysterious creative fields. Scorpio navamsa adds psychological insight and a magnetic, slightly hidden style, suiting you to film, photography, research, or the occult arts. Your beauty has shadow in it.",
    },
    14: {  # Swati
        1: "Pada 1 (Sagittarius navamsa): You embody Swati's freedom-loving spirit with philosophical breadth, often becoming a teacher, traveller, or independent advisor. Sagittarius navamsa expands the wind into long journeys and broad worldviews. You dislike confinement of any kind.",
        2: "Pada 2 (Capricorn navamsa): You channel Swati's independence into structured ambition — entrepreneurship, business, or self-made professional climbs. Capricorn navamsa grounds Rahu's restlessness into long-term goals and disciplined work. You succeed by your own design, not inherited paths.",
        3: "Pada 3 (Aquarius navamsa): You are the most independent Swati, often a reformer, technologist, or social innovator. Aquarius navamsa doubles the unconventional streak, giving you an original mind and a global, almost detached, outlook. Friendships matter, but freedom matters more.",
        4: "Pada 4 (Pisces navamsa): You experience Swati's independence as spiritual or artistic seeking, drawn to mysticism, music, or work that crosses cultural boundaries. Pisces navamsa softens Rahu's edge into intuitive flow, suiting you to healing, art, or quiet behind-the-scenes service. Solitude renews you.",
    },
    15: {  # Vishakha
        1: "Pada 1 (Aries navamsa): You pursue Vishakha's goals with raw, competitive drive, often becoming a leader, athlete, or entrepreneur. Aries navamsa fuels Jupiter's ambition into bold action, suiting you to fields where being first matters. Patience is hard-won but achievable through purpose.",
        2: "Pada 2 (Taurus navamsa): You channel Vishakha's determination into stable, accumulating goals — wealth, property, family enterprise, or steady careers in finance and agriculture. Taurus navamsa grounds the dual focus into long-term build, giving you persistence and refined taste. Success is gradual but lasting.",
        3: "Pada 3 (Gemini navamsa): You apply Vishakha's goal-orientation to communication-rich fields — writing, teaching, marketing, or negotiation. Gemini navamsa adds intellectual quickness and versatility, allowing you to chase two ambitions at once. Networking is a natural strength.",
        4: "Pada 4 (Cancer navamsa): You pursue Vishakha's aims through family, emotional bonds, or nurturing professions like healthcare, education, or hospitality. Cancer navamsa, where Jupiter is exalted, deepens your wisdom and gives you a strong protective instinct toward those you serve. Goals become deeply personal.",
    },
    16: {  # Anuradha
        1: "Pada 1 (Leo navamsa): You bring Anuradha's friendship and devotion into leadership roles, often becoming the heart of any group. Leo navamsa adds confidence and generosity to Saturn's loyalty, suiting you to public roles, teaching, or creative direction. People follow you for warmth as much as authority.",
        2: "Pada 2 (Virgo navamsa): You channel Anuradha's devotion into precise, service-oriented work — healthcare, research, administration, or skilled craft. Virgo navamsa sharpens the disciplined nature and gives you a quiet perfectionism. Friendships are few but deeply maintained over decades.",
        3: "Pada 3 (Libra navamsa): You are Anuradha at its most relational — diplomatic, artistic, and naturally suited to partnerships and counselling. Libra navamsa softens Saturn's seriousness into Venusian charm, often drawing you to law, design, or human resources. Marriage and close alliances are central themes.",
        4: "Pada 4 (Scorpio navamsa): You experience Anuradha's devotion with intensity, secrecy, and transformative depth. Scorpio navamsa channels Saturn's loyalty into research, occult studies, or crisis-focused work. Friendships are few, fierce, and lifelong; betrayal cuts permanently.",
    },
    17: {  # Jyeshtha
        1: "Pada 1 (Sagittarius navamsa): You carry Jyeshtha's seniority with philosophical breadth, often becoming a respected teacher, counsellor, or principled elder. Sagittarius navamsa expands the courageous streak into ethical leadership and long journeys. You shoulder others' burdens through wisdom.",
        2: "Pada 2 (Capricorn navamsa): You are the disciplined elder of Jyeshtha, climbing slowly into positions of serious authority — administration, business, or government. Capricorn navamsa intensifies the burden-bearing nature, giving you grit and a quietly heavy responsibility complex. Recognition comes late but lasts.",
        3: "Pada 3 (Aquarius navamsa): You channel Jyeshtha's courage into reform, technology, or unconventional leadership. Aquarius navamsa cools the Mercury-driven mind into a strategic, future-leaning intellect, often placing you ahead of your peers. You protect outsiders and underdogs by instinct.",
        4: "Pada 4 (Pisces navamsa): You bear Jyeshtha's burdens with compassion and intuition, drawn to healing, spiritual leadership, or service to the suffering. Pisces navamsa softens the courageous streak into quiet sacrifice, often working behind the scenes. Solitude is essential to your strength.",
    },
    18: {  # Mula
        1: "Pada 1 (Aries navamsa): You investigate Mula's roots with bold, pioneering energy, often becoming a researcher, surgeon, or fearless explorer of new fields. Aries navamsa fuels Ketu's intensity into action, suiting you to work that demands courage in the face of uncertainty. You destroy old structures to build new ones.",
        2: "Pada 2 (Taurus navamsa): You channel Mula's depth into tangible, accumulating work — herbal medicine, agriculture, music, or research with practical outcomes. Taurus navamsa grounds Ketu's spiritual intensity into earthy persistence and a love of beauty. Material security matters more than expected.",
        3: "Pada 3 (Gemini navamsa): You apply Mula's investigative mind to writing, teaching, journalism, or analytical fields. Gemini navamsa adds intellectual versatility and verbal skill to the root-seeker, often making you a gifted communicator of difficult truths. Curiosity outweighs comfort.",
        4: "Pada 4 (Cancer navamsa): You explore Mula's roots through family history, ancestral patterns, and emotional psychology. Cancer navamsa softens the destructive streak into nurturing investigation, suiting you to therapy, traditional healing, or memoir-style creative work. Home is where your deepest research happens.",
    },
    19: {  # Purva Ashadha
        1: "Pada 1 (Leo navamsa): You embody Purva Ashadha's invincibility with regal confidence and creative flair. Leo navamsa amplifies Venus into theatrical, persuasive leadership, suiting you to public-facing careers in entertainment, politics, or hospitality. Pride is both your engine and occasional pitfall.",
        2: "Pada 2 (Virgo navamsa): You channel Purva Ashadha's pride into refined skill and meticulous craft — healing, fine art, hospitality, or detailed service work. Virgo navamsa tempers the invincibility with humility and analytical sharpness. You quietly outperform louder peers.",
        3: "Pada 3 (Libra navamsa): You are the diplomatic charmer of Purva Ashadha, drawn to partnerships, the arts, and aesthetic professions. Libra navamsa doubles the Venusian grace, giving you persuasive social skills and refined taste. Marriage is central to your sense of completion.",
        4: "Pada 4 (Scorpio navamsa): You experience Purva Ashadha's invincibility as emotional and psychological intensity, suiting you to research, therapy, performing arts, or transformative water-based work. Scorpio navamsa adds depth, secrecy, and unwavering loyalty in love. Few defeat you because you simply do not surrender.",
    },
    20: {  # Uttara Ashadha
        1: "Pada 1 (Sagittarius navamsa): You wear Uttara Ashadha's universal victory with philosophical breadth, often becoming a principled leader, teacher, or international figure. Sagittarius navamsa expands the Sun's integrity into ethical vision and long journeys. You win by being trustworthy.",
        2: "Pada 2 (Capricorn navamsa): You are the disciplined achiever of Uttara Ashadha, building lasting institutions through patient, structured effort. Capricorn navamsa intensifies the Sun's ambition into administrative or political mastery, often placing you in serious positions of authority later in life. Reputation is everything.",
        3: "Pada 3 (Aquarius navamsa): You channel Uttara Ashadha's integrity into reform, humanitarian work, or unconventional leadership. Aquarius navamsa cools the Sun's pride into principled detachment, suiting you to causes larger than personal gain. Recognition matters less than legacy.",
        4: "Pada 4 (Pisces navamsa): You experience Uttara Ashadha's victory through service, compassion, or spiritual leadership. Pisces navamsa softens the Sun's authority into intuitive generosity, often drawing you to healing, art, or quiet philanthropy. Your wins are usually invisible to the public.",
    },
    21: {  # Shravana
        1: "Pada 1 (Aries navamsa): You apply Shravana's listening and learning to bold, pioneering action, often becoming a teacher, communicator, or fast-rising professional. Aries navamsa fuels the Moon's receptivity into initiative, suiting you to leadership in education, media, or counselling. You learn quickly and act on it.",
        2: "Pada 2 (Taurus navamsa): You are Shravana at its most stable — a patient learner, traditional teacher, or musician who builds expertise over decades. Taurus navamsa grounds the Moon into steady accumulation of knowledge, wealth, and reputation. Family and community shape your path.",
        3: "Pada 3 (Gemini navamsa): You combine Shravana's listening skill with Gemini's verbal agility, making you a natural communicator, journalist, broadcaster, or teacher. Gemini navamsa amplifies the intellectual range and gives you a love of stories and short journeys. Information is your currency.",
        4: "Pada 4 (Cancer navamsa): You are deeply intuitive and family-rooted — Shravana's most emotional pada. Cancer navamsa, where the Moon rules, makes you a wise listener, traditional healer, or nurturing teacher. Memories and ancestral wisdom guide your decisions.",
    },
    22: {  # Dhanishtha
        1: "Pada 1 (Leo navamsa): You embody Dhanishtha's wealth and rhythm with regal confidence, often becoming a performer, leader, or successful entrepreneur. Leo navamsa amplifies Mars into charismatic ambition, suiting you to music, sports, or any field where presence matters. Generosity matches your appetite for success.",
        2: "Pada 2 (Virgo navamsa): You channel Dhanishtha's drive into precise, skilled work — finance, engineering, healthcare, or detailed craftsmanship. Virgo navamsa tempers Mars with discipline and analytical sharpness, making you efficient and quietly prosperous. You play the long financial game well.",
        3: "Pada 3 (Libra navamsa): You combine Dhanishtha's ambition with Venusian charm, suiting you to music, design, hospitality, or partnership-based business. Libra navamsa softens Mars into refined social skill, often making you the diplomatic face of wealthy ventures. Marriage tends toward the prosperous.",
        4: "Pada 4 (Scorpio navamsa): You experience Dhanishtha's drumbeat with intensity and depth — often in finance, research, military, or transformative creative fields. Scorpio navamsa, ruled by Mars (Dhanishtha's own lord), doubles the determination and gives you penetrating insight. Wealth and secrets accumulate together.",
    },
    23: {  # Shatabhisha
        1: "Pada 1 (Sagittarius navamsa): You channel Shatabhisha's healing mystery into philosophy, teaching, or cross-cultural exploration. Sagittarius navamsa expands Rahu's strangeness into a search for truth, suiting you to medicine, spiritual inquiry, or international work. You heal through perspective.",
        2: "Pada 2 (Capricorn navamsa): You apply Shatabhisha's mysterious depth to structured, ambitious careers — research, technology, administration, or large-scale healing systems. Capricorn navamsa grounds Rahu's eccentricity into disciplined, late-blooming success. Solitude fuels your work.",
        3: "Pada 3 (Aquarius navamsa): You are Shatabhisha at its most futuristic — innovative, humanitarian, and drawn to technology, astrology, or unconventional healing. Aquarius navamsa, ruled by Saturn (Shatabhisha's own lord), doubles the visionary detachment. You are often misunderstood until your time arrives.",
        4: "Pada 4 (Pisces navamsa): You experience Shatabhisha's healing as deep mystical or artistic work, drawn to mysticism, music, or hidden service to the suffering. Pisces navamsa dissolves Rahu's edge into intuitive flow, suiting you to dream-work, art therapy, or quiet retreat. Boundaries are necessary medicine.",
    },
    24: {  # Purva Bhadrapada
        1: "Pada 1 (Aries navamsa): You channel Purva Bhadrapada's fierce intensity into bold, pioneering action, often becoming an entrepreneur, reformer, or pressure-tested leader. Aries navamsa fuels Jupiter's transformative fire into competitive drive. You thrive in high-stakes environments where lesser nerves fail.",
        2: "Pada 2 (Taurus navamsa): You ground Purva Bhadrapada's intensity into stable, productive work — finance, real estate, traditional teaching, or long-term creative projects. Taurus navamsa softens the fierceness into persistent accumulation. You build slowly but with rare conviction.",
        3: "Pada 3 (Gemini navamsa): You apply Purva Bhadrapada's intensity to communication-rich fields — writing, journalism, teaching, or strategic analysis. Gemini navamsa adds intellectual versatility and verbal sharpness, making you a persuasive voice on intense subjects. Mental restlessness matches your inner fire.",
        4: "Pada 4 (Cancer navamsa): You experience Purva Bhadrapada's transformation through family, emotional depth, and protective instincts. Cancer navamsa, where Jupiter is exalted, softens the fierce streak into wise nurturing, often making you the steady anchor in turbulent households or causes. Compassion runs deep.",
    },
    25: {  # Uttara Bhadrapada
        1: "Pada 1 (Leo navamsa): You bring Uttara Bhadrapada's depth and wisdom into visible leadership, teaching, or creative roles. Leo navamsa adds confidence and generosity to Saturn's contemplative nature, often making you a charismatic guide or elder. Solitude balances your public presence.",
        2: "Pada 2 (Virgo navamsa): You channel Uttara Bhadrapada's wisdom into precise, healing, or analytical work — medicine, research, writing, or skilled service. Virgo navamsa sharpens the depth into practical mastery and a quiet perfectionism. You help others through careful, unglamorous expertise.",
        3: "Pada 3 (Libra navamsa): You combine Uttara Bhadrapada's depth with Venusian harmony, suiting you to counselling, art, partnership-based work, or spiritual community. Libra navamsa softens Saturn's seriousness into diplomatic grace, often drawing you to roles that mediate or bring beauty. Marriage is central to your unfolding.",
        4: "Pada 4 (Scorpio navamsa): You experience Uttara Bhadrapada's kundalini depth with intensity, secrecy, and transformative power. Scorpio navamsa channels Saturn's wisdom into research, mysticism, therapy, or crisis-focused work. Few see your true depth, and you prefer it that way.",
    },
    26: {  # Revati
        1: "Pada 1 (Sagittarius navamsa): You embody Revati's nourishing journey with philosophical breadth, often becoming a teacher, counsellor, or international traveller. Sagittarius navamsa expands Mercury's gentleness into ethical vision and broad horizons. You guide others to safe shores through wisdom.",
        2: "Pada 2 (Capricorn navamsa): You channel Revati's nurturing nature into structured, long-term service — administration, traditional healing, or institutional work. Capricorn navamsa grounds the dreamy quality into disciplined responsibility. Recognition comes slowly but settles deeply.",
        3: "Pada 3 (Aquarius navamsa): You apply Revati's compassion to humanitarian, technological, or unconventional service fields. Aquarius navamsa cools the gentle Mercury into principled detachment, suiting you to causes that cross cultural or social boundaries. Friendships span unusual circles.",
        4: "Pada 4 (Pisces navamsa): You are Revati at its most mystical — intuitive, compassionate, and drawn to spiritual, artistic, or healing work. Pisces navamsa, ruled by Jupiter, dissolves boundaries entirely, often making you a quiet caretaker of souls or animals. Endings and journeys are sacred to you.",
    },
}
