"""
Template text data for Kundli report generation.
Pre-written interpretive text for each Lagna, Nakshatra, planet-in-house, etc.
Based on classical Vedic astrology texts (Brihat Parashara Hora Shastra, Phaladeepika).
"""

# ── LAGNA (Ascendant) DATA ───────────────────────────────────────────────────
# One entry per zodiac sign. Keys: health, temperament, character, career,
# occupation, hobbies, love, finance, education

LAGNA_DATA = {
    "Aries": {
        "health": "Aries rules the head and face. You are prone to headaches, migraines, and sinus issues. You have a strong constitution and recover quickly from illness. Be mindful of injuries to the head and face, and avoid excessive heat and spicy food.",
        "temperament": "You are bold, energetic, and pioneering. As a natural leader, you take initiative and are not afraid of challenges. You can be impulsive and impatient at times, but your enthusiasm and courage carry you through. You possess a competitive spirit and thrive when given independence.",
        "character": "You are straightforward, honest, and direct in your communication. You have a strong will and determination. You are generous and warm-hearted but can be quick-tempered. Your adventurous spirit makes you eager to explore new territories and ideas.",
        "career": "You excel in roles that require leadership, initiative, and courage. Military, police, sports, surgery, engineering, and entrepreneurship suit you well. You work best independently and may find routine jobs stifling.",
        "occupation": "Careers in defense, athletics, emergency services, or any field requiring quick decision-making and physical energy will suit you. You could also excel as a surgeon, firefighter, or adventure sports instructor.",
        "hobbies": "You enjoy physical activities, sports, adventure travel, and competitive games. Martial arts, hiking, and outdoor activities appeal to your energetic nature.",
        "love": "You are passionate and intense in love. You fall in love quickly and express your feelings openly. You need a partner who can match your energy and give you space for independence. Your relationships are exciting but may face challenges due to your impatience.",
        "finance": "You are a risk-taker with money and can earn well through bold investments. However, impulsive spending can be a challenge. You earn quickly but need discipline to save. Property and real estate investments tend to be favorable.",
    },
    "Taurus": {
        "health": "Taurus rules the throat, neck, and thyroid. You may be prone to throat infections, thyroid issues, and neck pain. You have good stamina but tend toward weight gain. A balanced diet and regular exercise are essential for maintaining your health.",
        "temperament": "You are patient, reliable, and determined. You value stability and security above all. While slow to anger, once provoked, your temper can be formidable. You are practical and grounded, preferring a steady approach to life.",
        "character": "You are loyal, dependable, and have a strong sense of duty. You appreciate beauty, comfort, and the finer things in life. You can be stubborn and resistant to change, but this also gives you remarkable persistence in achieving your goals.",
        "career": "You thrive in careers related to finance, banking, agriculture, food, luxury goods, art, and music. Your practical nature makes you excellent in business management and real estate. You prefer stable, well-paying jobs over risky ventures.",
        "occupation": "Banking, accounting, agriculture, hospitality, interior design, fashion, and the culinary arts are ideal fields. You could also succeed as a jeweler, perfumer, or in any profession dealing with luxury items.",
        "hobbies": "You enjoy gardening, cooking, music, art collecting, and nature walks. Activities that engage your senses and provide comfort appeal to you. You may also enjoy pottery, painting, or wine tasting.",
        "love": "You are a devoted and romantic partner. You seek stability and long-term commitment in relationships. You express love through physical affection and material gestures. Jealousy and possessiveness can be challenges you need to manage.",
        "finance": "You are naturally good with money and tend to accumulate wealth steadily. You prefer safe investments and tangible assets like property and gold. You are generous but also know how to save for the future.",
    },
    "Gemini": {
        "health": "Gemini rules the arms, hands, shoulders, and lungs. You may be prone to respiratory issues, nervous tension, and problems with hands and arms. Your nervous energy can lead to anxiety and insomnia. Breathing exercises and meditation will benefit you greatly.",
        "temperament": "You are intellectually curious, versatile, and communicative. You have a quick wit and can adapt to any situation. Your dual nature means you can see both sides of any argument. You may struggle with consistency and can be scattered in your focus.",
        "character": "You are charming, sociable, and articulate. You have a gift for languages and communication. You are always learning and sharing knowledge. Your versatility is your strength, though others may see you as superficial or inconsistent.",
        "career": "You excel in communication-related fields: writing, journalism, teaching, marketing, public relations, and sales. Your intellectual agility makes you suited for technology, trading, and consulting roles.",
        "occupation": "Journalism, authoring, teaching, broadcasting, interpreting, marketing, and IT consulting are ideal. You could also thrive as a travel guide, comedian, or social media professional.",
        "hobbies": "You enjoy reading, writing, puzzles, board games, social media, and learning new languages. You love variety and may have many hobbies simultaneously. Travel and socializing are essential for your well-being.",
        "love": "You are witty and flirtatious in love. You need intellectual stimulation in a relationship. Communication is key for you, and you seek a partner who is both a lover and a best friend. You may struggle with commitment if bored.",
        "finance": "You can earn from multiple sources simultaneously. You are clever with money but may spend impulsively on gadgets, books, and travel. Diversified investments suit you better than putting all eggs in one basket.",
    },
    "Cancer": {
        "health": "Cancer rules the chest, breasts, and stomach. You are prone to digestive issues, water retention, and emotional eating. Your health is strongly tied to your emotional state. Stress management and a regular eating schedule are crucial for you.",
        "temperament": "You are nurturing, intuitive, and deeply emotional. You are fiercely protective of your family and loved ones. Your moods can fluctuate with the lunar cycle. You have an excellent memory and can be sentimental about the past.",
        "character": "You are caring, empathetic, and deeply connected to your roots. You have strong family values and create a warm, welcoming home. You can be overly sensitive and may retreat into your shell when hurt. Your intuition is remarkably accurate.",
        "career": "You excel in caregiving roles: nursing, counseling, childcare, hospitality, and real estate. Your intuitive nature makes you good in psychology, social work, and the food industry. You are a natural homemaker and interior decorator.",
        "occupation": "Healthcare, nursing, social work, hotel management, catering, marine-related work, and childcare are ideal. You could also succeed in history, archaeology, or antique dealing.",
        "hobbies": "You enjoy cooking, home decoration, gardening, swimming, and collecting memorabilia. Family gatherings and nurturing activities bring you joy. Photography and scrapbooking appeal to your sentimental nature.",
        "love": "You are deeply devoted and nurturing in love. You seek emotional security and a stable home life. You express love through care and protection. Your sensitivity means you can be easily hurt, and you need a partner who understands your emotional depth.",
        "finance": "You are careful with money and tend to save for the future and your family's security. You earn well in real estate, food, and hospitality. You may inherit property or wealth from your mother's side.",
    },
    "Leo": {
        "health": "Leo rules the heart, spine, and upper back. You may be prone to heart palpitations, back pain, and circulatory issues. You have a strong vitality but must guard against overexertion. Regular cardiovascular exercise and a heart-healthy diet are important.",
        "temperament": "You are confident, dramatic, and naturally charismatic. You love being the center of attention and have a regal bearing. You are generous, warm-hearted, and fiercely loyal. Your pride can sometimes be your downfall.",
        "character": "You are bold, creative, and have a natural flair for leadership. You are generous to a fault and love to entertain and inspire others. You have high standards for yourself and others. Your ego needs constant nourishment, and flattery works well on you.",
        "career": "You shine in leadership roles, entertainment, politics, management, and any field where you can be in the spotlight. Creative arts, acting, directing, and luxury brand management suit your personality perfectly.",
        "occupation": "Government service, politics, entertainment, event management, luxury retail, and senior management positions are ideal. You could excel as a CEO, film director, or creative director.",
        "hobbies": "You enjoy theater, performing arts, dancing, fashion, and attending grand events. You love luxury experiences, fine dining, and activities that allow you to showcase your talents.",
        "love": "You are passionate, generous, and dramatic in love. You shower your partner with gifts and affection. You need admiration and loyalty from your partner. Your romantic nature makes relationships exciting, but you can be demanding.",
        "finance": "You earn well and spend lavishly. You have expensive tastes and enjoy the finer things in life. You are generous with money, sometimes to your own detriment. Investments in gold, entertainment, and speculative ventures appeal to you.",
    },
    "Virgo": {
        "health": "Virgo rules the intestines, digestive system, and nervous system. You are prone to digestive disorders, food sensitivities, and anxiety. You may be a hypochondriac at times. A clean diet, regular routine, and stress management are essential for your well-being.",
        "temperament": "You are analytical, detail-oriented, and methodical. You have high standards and a strong work ethic. You can be critical and perfectionist, which may strain relationships. Your practical nature makes you excellent at problem-solving.",
        "character": "You are intelligent, modest, and service-oriented. You have a sharp eye for detail and an ability to organize and systematize. You are helpful and reliable but can worry excessively. Your humility is genuine, and you prefer to work behind the scenes.",
        "career": "You excel in healthcare, research, analysis, editing, accounting, and quality control. Your attention to detail makes you perfect for data analysis, auditing, and scientific research. You prefer methodical, structured work environments.",
        "occupation": "Medicine, pharmacy, nutrition, accounting, editing, software development, research science, and veterinary medicine are ideal. You also thrive in administrative and organizational roles.",
        "hobbies": "You enjoy reading, health and wellness activities, gardening, crossword puzzles, and organizing. You may be interested in herbalism, yoga, and dietary science. Volunteering for charitable causes brings you satisfaction.",
        "love": "You are loyal and devoted in love but may struggle to express emotions openly. You show love through acts of service and practical support. You seek a partner who appreciates your dedication and understands your need for order.",
        "finance": "You are careful and prudent with money. You budget meticulously and save diligently. You earn steadily through hard work and rarely take financial risks. Health-related investments and savings plans work well for you.",
    },
    "Libra": {
        "health": "Libra rules the kidneys, lower back, and skin. You may be prone to kidney issues, lower back pain, and skin conditions. Your health benefits from balance in all areas of life. Avoid excessive sugar and maintain good hydration.",
        "temperament": "You are charming, diplomatic, and have a strong sense of justice. You seek harmony and balance in all aspects of life. You can be indecisive and may avoid conflict at all costs. Your aesthetic sense is highly refined.",
        "character": "You are sociable, fair-minded, and have excellent taste. You value relationships and partnerships deeply. You are a natural peacemaker and mediator. Your need for approval and harmony can sometimes prevent you from taking a firm stand.",
        "career": "You excel in law, diplomacy, mediation, art, fashion, and public relations. Your social skills make you ideal for partnerships and collaborative work. Careers in beauty, design, and luxury goods also suit you well.",
        "occupation": "Law, diplomacy, fashion design, interior design, counseling, and hospitality are ideal. You could also thrive as a judge, art dealer, wedding planner, or HR professional.",
        "hobbies": "You enjoy art, music, fashion, socializing, and attending cultural events. You love beauty and aesthetics in all forms. Ballroom dancing, poetry, and visiting art galleries appeal to your refined tastes.",
        "love": "You are romantic, charming, and seek the ideal partnership. You are happiest when in a committed relationship. You are thoughtful and considerate but may struggle with decision-making in love. You need a partner who appreciates your romantic nature.",
        "finance": "You earn well through partnerships and collaborative ventures. You may spend freely on beauty, fashion, and social events. Financial partnerships and joint ventures are favorable for you. You benefit from having a financial advisor.",
    },
    "Scorpio": {
        "health": "Scorpio rules the reproductive organs and excretory system. You are prone to issues related to these areas, as well as infections and chronic conditions. You have remarkable regenerative powers and can recover from serious illness. Regular detoxification is beneficial.",
        "temperament": "You are intense, passionate, and deeply perceptive. You have a magnetic personality and a powerful presence. You are fiercely determined and can be secretive. Your emotional depth is unmatched, and you experience life with great intensity.",
        "character": "You are resourceful, brave, and a true survivor. You have an uncanny ability to read people and situations. You are loyal to those you trust but can be vengeful when betrayed. Your willpower and determination are your greatest strengths.",
        "career": "You excel in research, investigation, psychology, surgery, and anything requiring deep analysis. Financial management, insurance, and occult sciences also suit you. You thrive in roles where you can exercise control and make transformative changes.",
        "occupation": "Detective work, forensic science, psychology, surgery, research, mining, insurance, and the occult are ideal. You could also succeed in secret intelligence, pharmaceuticals, or crisis management.",
        "hobbies": "You enjoy mysteries, research, diving, martial arts, and studying the occult. You are drawn to activities that involve depth, transformation, and uncovering hidden truths. Intense physical activities help you release emotional energy.",
        "love": "You are deeply passionate and possessive in love. You seek total emotional and physical union with your partner. Trust is paramount for you, and betrayal is unforgivable. Your love life is intense and transformative.",
        "finance": "You have good financial instincts and can accumulate wealth through investments, inheritance, and joint finances. You are good at managing other people's money. Insurance, real estate, and research-based investments favor you.",
    },
    "Sagittarius": {
        "health": "Sagittarius rules the hips, thighs, and liver. You are prone to hip injuries, liver problems, and sciatic nerve issues. Your love for food and drink can affect your liver. Regular exercise and moderation in diet are important for your well-being.",
        "temperament": "You are optimistic, philosophical, and love freedom. You have a broad worldview and an insatiable curiosity about life and its meaning. You are generous, jovial, and inspiring. Your bluntness can sometimes offend others.",
        "character": "You are honest, straightforward, and have a strong moral compass. You are a natural teacher and philosopher. You love travel, adventure, and learning about different cultures. Your restlessness may make it hard to settle in one place.",
        "career": "You excel in education, law, publishing, religion, travel, and international business. Your philosophical nature makes you suited for consulting, mentoring, and spiritual guidance. You thrive in roles that offer freedom and variety.",
        "occupation": "Teaching, professorships, legal practice, publishing, travel industry, religious leadership, and philosophy are ideal. You could also succeed as an ambassador, explorer, or motivational speaker.",
        "hobbies": "You enjoy travel, horseback riding, archery, philosophy, and outdoor sports. You love learning new things and exploring different cultures. Reading, attending lectures, and engaging in debates bring you joy.",
        "love": "You are fun-loving, generous, and adventurous in love. You need a partner who shares your love for freedom and exploration. You may struggle with commitment if you feel confined. An intellectual and adventurous partner is ideal for you.",
        "finance": "You are lucky with money and tend to attract wealth through your optimism and connections. You can be generous to a fault and may overspend on travel and education. Long-term investments and international ventures favor you.",
    },
    "Capricorn": {
        "health": "Capricorn rules the joints, hair, teeth, skin, and nervous system. You are prone to joint problems, dental issues, and skin conditions. You do not readily yield to disease, but once sick, you tend to hold onto symptoms. Accidents involving broken bones, sprains, and dislocations are possible, especially involving the knees.",
        "temperament": "You are ambitious, disciplined, and have a strong sense of responsibility. You are practical and conservative in your approach. You are self-centered at times, cunning, secretive, and determined. You have strong work ethic, materialistic tendencies, and great respect for authority. You are serious, dedicated to duty, self-disciplined, and realistic.",
        "character": "You are practical, capable, and very tidy by nature. You love order and are methodical. It is possible that these qualities are highly developed in you, and while attending to minute details, you may lose some of the larger opportunities of life. You are sensitive and generous. You are a hesitant person, though you have qualities for making your way in the world. You are calculative and realistic, always wanting to achieve something.",
        "career": "Since you like to unite both sides of an argument, law and justice are good fields for you. You could do well as a labour mediator and in positions where you maintain peace and harmony. Try to stay clear of professions requiring instant and constant decisions.",
        "occupation": "Your desire for benefiting mankind will find scope in the medical profession or nursing. You would fulfill duties as a manager or supervisor with courage and kindness. In the literary and artistic field, you can become an excellent author or actor.",
        "hobbies": "Reading, painting, drama, and pastimes requiring artistic and literary feeling occupy your mind. You may develop an interest in spiritualism or the supernatural. Travel attracts you. For indoor games like table-tennis, carom, and badminton, you will have time.",
        "love": "You never forget friends and have a large circle of acquaintances. You will choose a partner from this large circle, often surprising those who know you best. Marriage will be comfortable, but other diversions may take your interests away from home.",
        "finance": "In financial matters, you will largely be the arbitrator of your own destiny. If you belong to the higher plane your natural gifts entitle you to occupy, you will always find wealth and gain high position, but you will never be satisfied. You will be generous in money matters.",
    },
    "Aquarius": {
        "health": "Aquarius rules the ankles, calves, and circulatory system. You are prone to circulatory problems, varicose veins, and ankle injuries. Your nervous system can be sensitive. Adequate sleep, regular exercise, and avoiding excessive screen time are important.",
        "temperament": "You are independent, humanitarian, and intellectually advanced. You are a visionary who thinks ahead of your time. You value freedom and originality above all. You can be detached and eccentric, which may confuse those around you.",
        "character": "You are progressive, open-minded, and socially conscious. You care deeply about humanity and social justice. You are inventive and original in your thinking. Your detached nature can make you seem aloof, but you genuinely care about the greater good.",
        "career": "You excel in technology, science, social work, humanitarian organizations, and innovation. Your forward-thinking nature makes you ideal for research, invention, and reform. You thrive in unconventional work environments.",
        "occupation": "Technology, engineering, space science, social activism, NGO work, and invention are ideal. You could also succeed as an astrologer, programmer, or in renewable energy fields.",
        "hobbies": "You enjoy technology, science fiction, social networking, humanitarian work, and attending workshops. You love learning about new technologies and futuristic concepts. Group activities and community service bring you satisfaction.",
        "love": "You are friendly and open-minded in love but may struggle with emotional intimacy. You need intellectual compatibility and shared ideals in a relationship. You value friendship as the foundation of romance. You need space and independence within a relationship.",
        "finance": "You earn well through technology, innovation, and group enterprises. You may spend on humanitarian causes and technological gadgets. Unconventional investments and cryptocurrency may attract you. Friends may play a role in your financial gains.",
    },
    "Pisces": {
        "health": "Pisces rules the feet, lymphatic system, and immune system. You are prone to foot problems, allergies, and immune-related issues. Your sensitivity makes you susceptible to absorbing others' energies. Rest, meditation, and time near water are healing for you.",
        "temperament": "You are compassionate, intuitive, and deeply spiritual. You have a rich inner world and vivid imagination. You are empathetic to the point of absorbing others' emotions. You can be dreamy and escapist when reality becomes too harsh.",
        "character": "You are gentle, kind, and selfless. You have a natural artistic and spiritual inclination. You are adaptable and can be all things to all people. Your boundaries may be weak, making you vulnerable to being taken advantage of. Your intuition borders on psychic ability.",
        "career": "You excel in arts, music, healing, spirituality, and any field requiring imagination and compassion. Your intuitive nature makes you suited for counseling, therapy, and creative arts. You thrive in environments that allow creative expression.",
        "occupation": "Music, art, film, photography, spiritual healing, counseling, marine biology, and charitable work are ideal. You could also succeed as a hospital worker, prison reformer, or meditation teacher.",
        "hobbies": "You enjoy music, art, swimming, meditation, and daydreaming. You love being near water and may enjoy fishing, sailing, or visiting aquariums. Spiritual practices, poetry, and creative visualization bring you peace.",
        "love": "You are deeply romantic and idealistic in love. You tend to put your partner on a pedestal and may be disappointed by reality. You need a partner who appreciates your sensitivity and protects your emotional boundaries. Your love is selfless and unconditional.",
        "finance": "You may have an inconsistent relationship with money, sometimes abundant and sometimes lacking. You are generous and may give away more than you can afford. Creative pursuits, healing arts, and spiritual work can bring financial rewards. Water-related businesses may be profitable.",
    },
}


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


# ── PLANET IN HOUSE (9 planets × 12 houses) ─────────────────────────────────
# Keys: [planet][house_number] → {benefic, malefic, remedies}

PLANET_IN_HOUSE = {
    "Sun": {
        1: {"benefic": "You are confident, authoritative, and have a commanding personality. You enjoy good health and have a strong constitution. You are a natural leader.", "malefic": "You may be overly proud, domineering, or self-centered. There could be issues with the father or authority figures.", "remedies": ["Offer water to the Sun at sunrise daily.", "Wear a Ruby gemstone after consulting an astrologer."]},
        2: {"benefic": "You come from a respectable family and have a dignified speech. You earn well through government or authoritative positions.", "malefic": "There may be disputes in family life and challenges with accumulating wealth. Eye problems are possible.", "remedies": ["Donate wheat and jaggery on Sundays.", "Maintain good relations with your father."]},
        3: {"benefic": "You are courageous, valiant, and have a strong will. Your younger siblings may be successful. You are good in communication.", "malefic": "Relations with siblings may be strained. You may be overly aggressive in your approach.", "remedies": ["Offer water to the Sun daily.", "Help your siblings and maintain harmony."]},
        4: {"benefic": "You may own property and vehicles. Your mother is likely to be influential. You have a good domestic environment.", "malefic": "Mental peace may be disturbed. There could be challenges related to property and domestic happiness.", "remedies": ["Serve your mother and elders.", "Donate red clothes or copper on Sundays."]},
        5: {"benefic": "You are intelligent, creative, and may gain through speculation. Your children will be successful. You have good intuition.", "malefic": "There could be delays or issues related to children. Speculative losses are possible.", "remedies": ["Worship Lord Shiva on Sundays.", "Feed jaggery to monkeys."]},
        6: {"benefic": "You overcome enemies easily and have good resistance to disease. You excel in competitive situations.", "malefic": "You may face health issues related to the stomach or heart. Workplace conflicts are possible.", "remedies": ["Feed jaggery and wheat to cows.", "Offer water to the Sun with red flowers."]},
        7: {"benefic": "Your spouse may be from a distinguished family. You gain through partnerships and have good social connections.", "malefic": "Marital life may face challenges due to ego clashes. Your partner may be dominating.", "remedies": ["Respect your spouse and avoid ego in relationships.", "Offer water to the Sun daily."]},
        8: {"benefic": "You have interest in occult sciences and may gain through inheritance. You have strong regenerative powers.", "malefic": "Health issues, especially related to bones and eyes, are possible. Relations with the father may be troubled.", "remedies": ["Donate red cloth and copper on Sundays.", "Recite Aditya Hridaya Stotra."]},
        9: {"benefic": "You are religious, fortunate, and respected by society. Your father is likely influential. You benefit from long journeys.", "malefic": "Relations with the father or guru may be strained. Religious beliefs may fluctuate.", "remedies": ["Respect your father and teachers.", "Visit religious places regularly."]},
        10: {"benefic": "Benefits and favours from government, good health, and financially stronger. You will get a government job and comforts of vehicles and servants. You will always be suspicious about others.", "malefic": "If Saturn is in the 4th house, the father may face early challenges. If the 4th house is empty, government favours may be limited.", "remedies": ["Never wear blue or black clothes.", "Throw a copper coin in a river for 43 days.", "Abstain from liquor and meat."]},
        11: {"benefic": "You gain through influential friends and government connections. Your income is substantial and comes from multiple sources.", "malefic": "Gains may be inconsistent. Elder siblings may face challenges.", "remedies": ["Maintain good relations with elder siblings.", "Offer water to the Sun at sunrise."]},
        12: {"benefic": "You are spiritually inclined and may find peace through meditation. You may settle abroad.", "malefic": "Financial losses, eye problems, and separation from family are possible.", "remedies": ["Donate wheat and jaggery to the needy.", "Practice meditation regularly."]},
    },
    "Moon": {
        1: {"benefic": "You are attractive, emotional, and sensitive. You have a caring personality and people are drawn to you.", "malefic": "You may be overly emotional and indecisive. Mood swings can affect your productivity.", "remedies": ["Wear a Pearl gemstone.", "Drink water from a silver glass."]},
        2: {"benefic": "You have a sweet voice and good family life. You are wealthy and enjoy good food.", "malefic": "Financial fluctuations and family disputes may occur. Speech may be inconsistent.", "remedies": ["Keep a silver ball in your pocket.", "Respect your mother."]},
        3: {"benefic": "You are brave, adventurous, and have good relations with siblings. You are skilled in communication.", "malefic": "Mental restlessness and unnecessary travel may occur. Relations with siblings may be unstable.", "remedies": ["Maintain good relations with your mother.", "Donate white cloth on Mondays."]},
        4: {"benefic": "You enjoy domestic happiness, property, and vehicles. You are emotionally content and have a good relationship with your mother.", "malefic": "Mental peace may be disturbed due to overthinking. Property disputes are possible.", "remedies": ["Serve your mother with devotion.", "Keep a silver piece at home."]},
        5: {"benefic": "You are intelligent, romantic, and have creative talents. Your children bring you happiness.", "malefic": "Emotional ups and downs in love life. Worry about children's welfare.", "remedies": ["Worship Goddess Lakshmi on Mondays.", "Donate white sweets to children."]},
        6: {"benefic": "You overcome enemies through emotional intelligence. Good for service-related careers.", "malefic": "Digestive and emotional health issues. Enemies may create trouble through gossip.", "remedies": ["Feed birds with rice and water.", "Donate milk to temples."]},
        7: {"benefic": "You attract a caring and nurturing spouse. Partnerships bring emotional fulfillment.", "malefic": "Marital life may face emotional turbulence. Over-dependency on the partner.", "remedies": ["Keep a silver idol of your deity.", "Offer milk at a Shiva temple."]},
        8: {"benefic": "Strong intuition and interest in occult sciences. You may gain through inheritance.", "malefic": "Emotional health may suffer. Chronic health issues related to water or chest are possible.", "remedies": ["Donate white cloth and rice on Mondays.", "Recite Chandra mantra regularly."]},
        9: {"benefic": "You are spiritually inclined and fortunate. Pilgrimage and long travels bring blessings.", "malefic": "Relationship with the mother may be distant. Religious beliefs may fluctuate.", "remedies": ["Serve your mother.", "Visit religious places near water."]},
        10: {"benefic": "Very successful and productive period. You gain fame and recognition in your career. Public dealing brings gains.", "malefic": "Career may have frequent changes. Public image may fluctuate.", "remedies": ["Keep water in a silver vessel at your workplace.", "Respect women in your workplace."]},
        11: {"benefic": "This house is strongly influenced by Jupiter and Saturn. You have many friends and gain through social connections. Financial gains are abundant.", "malefic": "The Moon here faces the combined power of Saturn and Ketu, which may weaken emotional stability. Relations with mother may be strained.", "remedies": ["Offer milk in a temple and donate milk liberally.", "Heat a piece of gold and put it in milk before drinking."]},
        12: {"benefic": "Spiritual inclination is strong. You find peace in solitude and meditation.", "malefic": "Sleep disturbances and mental anxiety. Financial losses through emotional decisions.", "remedies": ["Keep a glass of water near your head while sleeping.", "Donate white cloth to poor women."]},
    },
    "Mars": {
        1: {"benefic": "You are energetic, courageous, and physically strong. You have a competitive spirit and natural leadership.", "malefic": "You may be aggressive, impatient, and prone to accidents. Scars on the head or face are possible.", "remedies": ["Recite Hanuman Chalisa daily.", "Wear a Red Coral gemstone."]},
        2: {"benefic": "You earn well through your own efforts and have a strong voice. Good for military or surgical careers.", "malefic": "Harsh speech may create family discord. Financial disputes within the family.", "remedies": ["Speak politely and control your temper.", "Donate red lentils on Tuesdays."]},
        3: {"benefic": "You are courageous, valiant, and a champion. You will have lots of patience and will gather fame. You are physically and mentally fit. Good relations with siblings, especially beneficial for younger brothers.", "malefic": "Mars may make you harsh in words. Problems for brothers, especially younger brothers, and disharmony in relations.", "remedies": ["Help your siblings financially.", "Donate blood on Tuesdays if health permits."]},
        4: {"benefic": "You own property and have a strong foundation. Your mother is likely to be a strong personality.", "malefic": "Domestic peace may be disturbed. Property disputes and vehicle accidents are possible.", "remedies": ["Offer sindoor to Hanuman on Tuesdays.", "Keep a piece of red cloth under your pillow."]},
        5: {"benefic": "You are intelligent, athletic, and good in speculation. Your children will be energetic and successful.", "malefic": "Anxiety due to ill health of family members. Fruitless travel should be avoided. Unnecessary expenses possible.", "remedies": ["Worship Lord Kartikeya.", "Donate sweets to children on Tuesdays."]},
        6: {"benefic": "You defeat enemies easily and have excellent immunity. Great for military, police, and surgical careers.", "malefic": "Injuries, accidents, and conflicts with coworkers possible. Blood-related health issues.", "remedies": ["Feed jaggery to monkeys on Tuesdays.", "Donate red lentils."]},
        7: {"benefic": "Your spouse is energetic and dynamic. Partnerships with courageous people favor you.", "malefic": "Marital conflicts due to aggression. Spouse may be dominating. This placement creates Manglik Dosha.", "remedies": ["Worship Lord Hanuman together with your spouse.", "Donate red cloth on Tuesdays."]},
        8: {"benefic": "Strong willpower and ability to handle crises. Interest in research and occult.", "malefic": "Accidents, surgeries, and chronic health issues possible. Financial losses through disputes.", "remedies": ["Recite Hanuman Chalisa daily.", "Donate blood if health permits."]},
        9: {"benefic": "You are adventurous, religious, and gain through travel. Your father is likely a strong personality.", "malefic": "Disputes with father or spiritual teachers. Hasty actions may create problems.", "remedies": ["Respect your father and elders.", "Visit Hanuman temples on Tuesdays."]},
        10: {"benefic": "Excellent for career success. You are ambitious, hardworking, and rise to leadership positions.", "malefic": "Conflicts with authorities and workplace disputes. Career may face sudden ups and downs.", "remedies": ["Offer sindoor to Hanuman on Tuesdays.", "Donate jaggery and red lentils."]},
        11: {"benefic": "You gain through courageous actions and influential friends. High income and material success.", "malefic": "Disputes with elder siblings. Gains may come through conflicts.", "remedies": ["Help your elder siblings.", "Donate red lentils on Tuesdays."]},
        12: {"benefic": "Good for spiritual pursuits and foreign travel. You have strong willpower for meditation.", "malefic": "Financial losses, hospitalization, and hidden enemies. Sleep disturbances.", "remedies": ["Recite Hanuman Chalisa before sleeping.", "Keep a red handkerchief under your pillow."]},
    },
    "Mercury": {
        1: {"benefic": "You are intelligent, youthful, and have excellent communication skills. Quick learner and good with languages.", "malefic": "Nervous energy, anxiety, and skin issues. Overthinking and indecisiveness.", "remedies": ["Wear an Emerald gemstone.", "Feed green moong dal to birds."]},
        2: {"benefic": "Sweet and persuasive speech. Excellent for business and trade. You accumulate wealth through intelligence.", "malefic": "Speech may be manipulative. Financial losses through wrong calculations.", "remedies": ["Donate green cloth on Wednesdays.", "Keep a bronze vessel of water at home."]},
        3: {"benefic": "Excellent communication skills and good relations with siblings. Success in writing, media, and technology.", "malefic": "Nervous anxiety and restlessness. Too many short trips without results.", "remedies": ["Help your siblings in education.", "Donate green vegetables on Wednesdays."]},
        4: {"benefic": "Good education, domestic happiness, and property. Your mother is intelligent and supportive.", "malefic": "Mental restlessness at home. Frequent changes of residence.", "remedies": ["Serve your mother.", "Plant trees and take care of greenery around home."]},
        5: {"benefic": "Highly intelligent, good in studies, and creative. Children are intelligent. Good for speculation and investments.", "malefic": "Overthinking about children. Speculative losses due to wrong analysis.", "remedies": ["Worship Lord Vishnu on Wednesdays.", "Donate green fruits to children."]},
        6: {"benefic": "You defeat enemies through intelligence. Good for healthcare, accounting, and analytical work.", "malefic": "Nervous health issues and workplace stress. Enemies may use words against you.", "remedies": ["Feed green grass to cows.", "Donate green cloth on Wednesdays."]},
        7: {"benefic": "Intelligent and communicative spouse. Successful business partnerships.", "malefic": "Marital miscommunication. Multiple partnerships or relationships.", "remedies": ["Communicate openly with your spouse.", "Donate green items on Wednesdays."]},
        8: {"benefic": "Good for research, investigation, and occult studies. Strong analytical mind.", "malefic": "Nervous disorders and skin problems. Financial losses through fraud.", "remedies": ["Donate green moong dal on Wednesdays.", "Recite Vishnu Sahasranama."]},
        9: {"benefic": "Scholarly, religious, and fortunate. Success in higher education and publishing.", "malefic": "Disputes with teachers. Over-intellectualization of spirituality.", "remedies": ["Respect your teachers and gurus.", "Donate books to students."]},
        10: {"benefic": "This year presents you with a taxing work schedule but will reward you with good career progress. Excellent period for success. Corporation from family is seen. You can make great progress professionally and win over your enemies.", "malefic": "Workplace stress and communication issues with superiors. Frequent job changes.", "remedies": ["Offer rice and milk in religious places.", "Avoid consumption of eggs, meat, and liquor."]},
        11: {"benefic": "Good income through business, trade, and intellectual pursuits. Many friends who help in gains.", "malefic": "Financial losses through wrong advice from friends. Communication issues with elder siblings.", "remedies": ["Maintain honest friendships.", "Donate green cloth on Wednesdays."]},
        12: {"benefic": "Good for foreign travel, spiritual learning, and working in isolation. Research and writing favor you.", "malefic": "Mental anxiety, sleep issues, and financial losses. Difficulty in decision-making.", "remedies": ["Meditate regularly.", "Keep an Emerald near your bed."]},
    },
    "Jupiter": {
        1: {"benefic": "You are wise, generous, and have a large personality. You are respected in society and have good health.", "malefic": "Weight gain and liver issues. Over-optimism may lead to poor judgment.", "remedies": ["Wear a Yellow Sapphire gemstone.", "Apply turmeric tilak on forehead."]},
        2: {"benefic": "Wealthy, well-spoken, and come from a good family. Excellent for banking and finance careers.", "malefic": "Overindulgence in food and spending. Family disputes over money.", "remedies": ["Donate yellow items on Thursdays.", "Visit temples regularly."]},
        3: {"benefic": "Good relations with siblings and neighbors. You are brave and communicative with wisdom.", "malefic": "Laziness in efforts. Siblings may not be cooperative.", "remedies": ["Help your siblings in their pursuits.", "Donate yellow cloth on Thursdays."]},
        4: {"benefic": "Great domestic happiness, good education, and property. Your mother is religious and kind.", "malefic": "Excessive attachment to home and comfort. Weight-related issues.", "remedies": ["Serve your mother and keep the home clean.", "Plant a Peepal tree."]},
        5: {"benefic": "You should have a good nature viewable by all. You have firm faith in God. You are religious with pure thoughts. You have kindness and modesty as your qualities. Counted amongst intelligent, virtuous, and noble people. You are a good speaker and master in making policies.", "malefic": "Over-confidence in speculation. Expectations from children may not be met.", "remedies": ["Worship Lord Vishnu on Thursdays.", "Donate yellow sweets to Brahmins."]},
        6: {"benefic": "You overcome enemies through wisdom. Good health and ability to manage debts.", "malefic": "Liver and digestive issues. Legal disputes may drain finances.", "remedies": ["Donate yellow lentils on Thursdays.", "Feed bananas to needy people."]},
        7: {"benefic": "Fortunate in marriage. Spouse is wise, religious, and supportive. Business partnerships flourish.", "malefic": "Spouse may be overly preachy. Weight gain after marriage.", "remedies": ["Respect your spouse's wisdom.", "Worship together on Thursdays."]},
        8: {"benefic": "Interest in occult and spiritual knowledge. May gain through inheritance.", "malefic": "Financial setbacks and health challenges. Relations with in-laws may be difficult.", "remedies": ["Donate turmeric and yellow lentils on Thursdays.", "Recite Vishnu mantras."]},
        9: {"benefic": "Extremely fortunate. Strong spiritual inclination and respect in society. Father is influential and religious.", "malefic": "Over-confidence in spiritual matters. Orthodoxy may create conflicts.", "remedies": ["Maintain humility in spiritual practice.", "Serve saints and sages."]},
        10: {"benefic": "Excellent career success, government favor, and social recognition. You rise to high positions.", "malefic": "Career growth may plateau. Conflicts with superiors over ethical matters.", "remedies": ["Apply turmeric tilak before going to work.", "Donate yellow items on Thursdays."]},
        11: {"benefic": "Abundant income and fulfillment of desires. Many helpful and wise friends.", "malefic": "Over-spending on charitable causes. Expectations from friends not met.", "remedies": ["Be generous but within your means.", "Donate to religious institutions."]},
        12: {"benefic": "Strong spiritual inclination. Success abroad and in charitable work. Peaceful end of life.", "malefic": "Financial losses through bad investments. Lack of worldly success.", "remedies": ["Practice meditation and yoga.", "Donate to spiritual organizations."]},
    },
    "Venus": {
        1: {"benefic": "You are attractive, charming, and have refined tastes. Good for arts, beauty, and luxury-related careers.", "malefic": "Over-indulgence in pleasures. Vanity and superficiality.", "remedies": ["Wear a Diamond or White Sapphire.", "Donate white items on Fridays."]},
        2: {"benefic": "Sweet speech, good family life, and wealth. You enjoy fine food, art, and luxury.", "malefic": "Over-spending on luxuries. Family disputes over lifestyle choices.", "remedies": ["Donate white rice and sugar on Fridays.", "Keep silver items at home."]},
        3: {"benefic": "Artistic talents, good relations with siblings, and success in creative communication.", "malefic": "Siblings may be demanding. Over-socializing affects productivity.", "remedies": ["Support artistic talents of siblings.", "Donate white cloth on Fridays."]},
        4: {"benefic": "Beautiful home, luxury vehicles, and a happy domestic life. Good relationship with mother.", "malefic": "Excessive attachment to material comforts. Mother may face health issues.", "remedies": ["Donate white items to women.", "Keep your home clean and beautiful."]},
        5: {"benefic": "Romantic, creative, and talented in arts. Children are beautiful and talented.", "malefic": "Over-indulgence in romance. Unrealistic expectations in love.", "remedies": ["Worship Goddess Lakshmi on Fridays.", "Donate white sweets."]},
        6: {"benefic": "You overcome enemies through charm and diplomacy. Good health and attractive appearance.", "malefic": "Reproductive health issues. Workplace romantic complications.", "remedies": ["Donate white items on Fridays.", "Maintain professional boundaries."]},
        7: {"benefic": "Beautiful and loving spouse. Successful business partnerships, especially in creative fields.", "malefic": "Multiple relationships or attractions. Over-dependency on spouse.", "remedies": ["Be loyal to your spouse.", "Donate white items together."]},
        8: {"benefic": "Gains through marriage and partnerships. Interest in tantric arts and mysticism.", "malefic": "Reproductive health issues. Financial losses through relationships.", "remedies": ["Donate white cloth on Fridays.", "Worship Goddess Durga."]},
        9: {"benefic": "Venus in this house brings riches but only after hard labour. Your efforts may not be proportionally rewarded. The period requires patience and persistence.", "malefic": "Dearth of people, money, wealth, and property may be experienced. If Venus is with malefic planets, intoxication tendencies may develop from a young age.", "remedies": ["Bury silver and honey in the foundation of the house.", "Wear silver bangles with red colour on them.", "Bury a silver piece under a Neem tree for 43 days."]},
        10: {"benefic": "Success in arts, entertainment, fashion, and luxury industries. Famous and well-respected.", "malefic": "Career may be affected by romantic scandals. Over-focus on appearance.", "remedies": ["Donate white items on Fridays.", "Worship Goddess Lakshmi."]},
        11: {"benefic": "High income through creative ventures. Beautiful and supportive friends. Desires are fulfilled.", "malefic": "Over-spending on social gatherings. Unrealistic financial expectations.", "remedies": ["Be generous with friends but maintain boundaries.", "Donate white rice on Fridays."]},
        12: {"benefic": "Good for spiritual practice and foreign settlement. Luxurious beds and good sleep.", "malefic": "Financial losses through indulgence. Secret relationships.", "remedies": ["Practice contentment.", "Donate white cloth to poor women."]},
    },
    "Saturn": {
        1: {"benefic": "You are disciplined, hardworking, and build lasting achievements. Long life and strong character.", "malefic": "Health issues, delayed success, and a serious demeanor. Childhood may be difficult.", "remedies": ["Recite Hanuman Chalisa on Saturdays.", "Donate black sesame and mustard oil."]},
        2: {"benefic": "Wealth through discipline and hard work. Conservative with money.", "malefic": "Family disputes, harsh speech, and dental issues. Financial hardship in early life.", "remedies": ["Feed crows on Saturdays.", "Donate black lentils."]},
        3: {"benefic": "Courageous, determined, and successful through persistent effort. Good longevity.", "malefic": "Strained relations with siblings. Shoulder and arm issues.", "remedies": ["Help your younger siblings.", "Donate black cloth on Saturdays."]},
        4: {"benefic": "Property ownership through hard work. Deep thinker with a philosophical mind.", "malefic": "Domestic unhappiness and cold relations with mother. Mental depression.", "remedies": ["Serve your mother.", "Donate milk and curd on Saturdays."]},
        5: {"benefic": "Disciplined approach to creativity. Children are responsible. Good for research.", "malefic": "Delayed progeny. Disappointment from children. Pessimistic outlook.", "remedies": ["Worship Lord Shani on Saturdays.", "Donate black sesame to temples."]},
        6: {"benefic": "Victory over enemies. Strong in competitive situations. Good for legal matters.", "malefic": "Chronic health issues. Long-standing enmities and legal disputes.", "remedies": ["Feed dogs and crows on Saturdays.", "Donate mustard oil."]},
        7: {"benefic": "Late but stable marriage. Spouse is mature and responsible.", "malefic": "Delayed marriage. Marital coldness and communication gaps.", "remedies": ["Be patient with your spouse.", "Donate black cloth on Saturdays."]},
        8: {"benefic": "Long life and interest in occult sciences. Gains through inheritance.", "malefic": "Chronic health issues, accidents, and financial setbacks. Period of darkness before transformation.", "remedies": ["Recite Shani mantras.", "Donate iron items on Saturdays."]},
        9: {"benefic": "Success in law, philosophy, and religious leadership. Father is disciplined.", "malefic": "Strained relations with father and teachers. Delayed fortune.", "remedies": ["Respect your father and elders.", "Visit Shani temples on Saturdays."]},
        10: {"benefic": "Great career achievements through persistent hard work. Rise to positions of authority, though slowly.", "malefic": "Career obstacles and slow progress. Conflicts with authority figures.", "remedies": ["Work honestly and patiently.", "Donate black sesame on Saturdays."]},
        11: {"benefic": "Steady income through disciplined effort. Long-lasting friendships and elder siblings support you.", "malefic": "Financial gains come slowly. Friends may be unreliable.", "remedies": ["Help the underprivileged.", "Donate black lentils on Saturdays."]},
        12: {"benefic": "Saturn gives good results in this house. You will not have enemies. You will have many houses. Your family and business will increase. You will be very influential.", "malefic": "Spiritual isolation and financial losses. Hospitalization and hidden enemies.", "remedies": ["Practice meditation.", "Donate to old-age homes and orphanages."]},
    },
    "Rahu": {
        1: {"benefic": "You have a magnetic personality and strong ambition. You can achieve great worldly success.", "malefic": "Confusion about identity. Health issues and deceptive behavior. Mental restlessness.", "remedies": ["Keep a piece of silver with you.", "Donate black sesame on Saturdays."]},
        2: {"benefic": "If Rahu is benefic, you get money, prestige, and live like royalty. Long life. Wealth comes through unconventional means.", "malefic": "You may be poor and have bad family life. Intestinal disorders. Unable to save money. Losses through theft possible.", "remedies": ["Keep a solid silver ball in your pocket.", "Wear things associated with Jupiter like gold and saffron.", "Keep cordial relations with your mother."]},
        3: {"benefic": "Great courage and ability to take risks. Success in media, technology, and communication.", "malefic": "Strained relations with siblings. Risky adventures without result.", "remedies": ["Maintain good relations with siblings.", "Donate blue or black cloth."]},
        4: {"benefic": "Gain through foreign property and unconventional means. Interest in technology at home.", "malefic": "Volatility and lack of direction in career. Troubles with friends and relatives. Fighting and disputes in life. Working conditions not satisfactory. Danger of accidents.", "remedies": ["Do not adopt undesirable means for quick monetary gains.", "Keep the home clean and well-ventilated."]},
        5: {"benefic": "Unconventional intelligence and creativity. Children may be unique and talented.", "malefic": "Confusion about progeny. Wrong speculative decisions. Obsessive behavior.", "remedies": ["Worship Goddess Saraswati.", "Donate to educational institutions."]},
        6: {"benefic": "Victory over enemies through unconventional means. Success in foreign lands.", "malefic": "Hidden enemies and chronic health issues. Digestive problems.", "remedies": ["Donate to hospitals.", "Feed stray animals."]},
        7: {"benefic": "Foreign spouse or unconventional partnerships. Success in international business.", "malefic": "Marital deception and instability. Multiple relationships.", "remedies": ["Be transparent in relationships.", "Donate blue cloth on Saturdays."]},
        8: {"benefic": "Interest in occult, tantra, and mystical knowledge. May gain through insurance or inheritance.", "malefic": "Sudden health crises. Financial losses through fraud. Fear of the unknown.", "remedies": ["Recite Durga Saptashati.", "Donate black lentils on Saturdays."]},
        9: {"benefic": "Interest in foreign cultures and philosophies. Unconventional spiritual path.", "malefic": "Disrespect to father and teachers. Irreligious tendencies.", "remedies": ["Respect all religious traditions.", "Visit holy places of different faiths."]},
        10: {"benefic": "Great career success through unconventional means. Success in technology and foreign companies.", "malefic": "Career instability and reputation issues. Sudden rise and fall.", "remedies": ["Work with integrity.", "Donate to charitable organizations."]},
        11: {"benefic": "Gains through foreign connections. Large social network and unconventional friends.", "malefic": "Deceptive friends. Gains through dubious means.", "remedies": ["Choose friends wisely.", "Donate to social causes."]},
        12: {"benefic": "Spiritual progress through unconventional means. Success abroad.", "malefic": "Insomnia, mental anxiety, and financial losses. Hidden enemies abroad.", "remedies": ["Practice meditation.", "Donate food to the needy."]},
    },
    "Ketu": {
        1: {"benefic": "Strong spiritual inclination and past-life wisdom. Intuitive and perceptive.", "malefic": "Confusion about identity. Health issues and isolation. Mysterious personality.", "remedies": ["Worship Lord Ganesha.", "Donate brown or grey items."]},
        2: {"benefic": "Detachment from material wealth leading to spiritual riches. Mystical speech.", "malefic": "Financial losses and family discord. Speech problems and eye issues.", "remedies": ["Donate saffron-colored items.", "Feed dogs."]},
        3: {"benefic": "Courageous with spiritual warrior qualities. Good for martial arts and esoteric studies.", "malefic": "Strained relations with siblings. Ear and arm problems.", "remedies": ["Maintain harmony with siblings.", "Donate grey cloth."]},
        4: {"benefic": "Detachment from worldly comforts leading to inner peace. Interest in spiritual homes.", "malefic": "Domestic unhappiness. Detachment from mother. Property losses.", "remedies": ["Serve your mother.", "Donate to temples."]},
        5: {"benefic": "Past-life intelligence and spiritual creativity. Interest in meditation and mantras.", "malefic": "Confusion about children. Losses in speculation. Academic challenges.", "remedies": ["Worship Lord Ganesha.", "Donate to children's organizations."]},
        6: {"benefic": "Victory over enemies through spiritual means. Good healing abilities.", "malefic": "Mysterious health issues. Hidden enemies working against you.", "remedies": ["Recite Ganesha mantras.", "Donate to animal shelters."]},
        7: {"benefic": "Spouse with spiritual qualities. Past-life karmic relationships.", "malefic": "Marital detachment and misunderstandings. Unexplained relationship problems.", "remedies": ["Be present and attentive with your spouse.", "Worship together."]},
        8: {"benefic": "Ketu gives some good results here. You will be brave and hard-working. You take work seriously. Deep interest in games. You stay happy and are a modest person with financial profit. You may also get money from the government.", "malefic": "You may keep company of bad people. You may be shrewd or greedy. Sometimes work done by you may be morally questionable.", "remedies": ["Recite Ganesha Atharvashirsha.", "Donate grey blankets to the needy."]},
        9: {"benefic": "Deep spiritual knowledge from past lives. Interest in ancient wisdom and mysticism.", "malefic": "Disrespect to father and gurus. Confusion about spiritual path.", "remedies": ["Respect your father and spiritual teachers.", "Study ancient scriptures."]},
        10: {"benefic": "Spiritual approach to career. Success in healing, research, and mystical fields.", "malefic": "Career confusion and lack of direction. Sudden career changes.", "remedies": ["Find your true calling through meditation.", "Donate to spiritual organizations."]},
        11: {"benefic": "Spiritual friendships and detachment from material gains. Unique income sources.", "malefic": "Losses through friends. Unfulfilled desires.", "remedies": ["Choose spiritual companions.", "Donate grey items."]},
        12: {"benefic": "Excellent for spiritual liberation. Strong meditation and moksha potential.", "malefic": "Complete detachment from worldly life. Financial losses. Hospitalization.", "remedies": ["Practice regular meditation.", "Visit spiritual retreats."]},
    },
}


# ── DASHA PREDICTIONS ────────────────────────────────────────────────────────

DASHA_PREDICTIONS = {
    "Sun": "During the Sun Mahadasha, you will experience a period of authority, power, and self-expression. Government connections and father figures play important roles. Health, vitality, and confidence are highlighted. Leadership opportunities arise, and your true nature shines through. Be mindful of ego and pride during this period.",
    "Moon": "During the Moon Mahadasha, emotions, intuition, and family matters take center stage. This is a period of emotional growth, nurturing, and domestic happiness. Your mother's influence is strong. Travel, especially over water, is favorable. Mental peace comes through spiritual practices and caring for others.",
    "Mars": "During the Mars Mahadasha, energy, courage, and ambition are at their peak. This is a period of action, competition, and achievement. Property matters, siblings, and technical skills are highlighted. Guard against aggression, accidents, and impulsive decisions. Physical fitness and sports bring positive results.",
    "Mercury": "During the Mercury Mahadasha, intelligence, communication, and learning are emphasized. This is an excellent period for education, business, writing, and intellectual pursuits. Your analytical abilities are sharp. Financial gains through trade and commerce are possible. Be mindful of nervous tension and overthinking.",
    "Jupiter": "During the Jupiter Mahadasha, wisdom, growth, and fortune expand. This is generally the most favorable period, bringing prosperity, spiritual growth, and recognition. Higher education, religious activities, and charitable work bring blessings. Children and family life flourish. Be careful of overconfidence and weight gain.",
    "Venus": "During the Venus Mahadasha, love, beauty, comfort, and luxury are highlighted. This is a period of romantic relationships, artistic expression, and material enjoyment. Marriage, partnerships, and social life are active. Financial gains through creative ventures and luxury goods are possible. Avoid overindulgence.",
    "Saturn": "During the Saturn Mahadasha, discipline, patience, and hard work are required. This period tests your resilience and builds lasting foundations. Career growth comes slowly but surely. Health may require attention. This period teaches valuable life lessons through challenges. Persistence and integrity lead to lasting success.",
    "Rahu": "During the Rahu Mahadasha, ambition, worldly desires, and unconventional paths are highlighted. This is a period of material growth but also confusion and illusion. Foreign connections and technology play important roles. Sudden changes and unexpected events are common. Stay grounded and avoid shortcuts.",
    "Ketu": "During the Ketu Mahadasha, spirituality, detachment, and past-life karma are emphasized. This is a period of introspection, spiritual growth, and letting go of material attachments. Mysterious events and sudden transformations occur. Healing abilities and intuition are heightened. Meditation and spiritual practices bring peace.",
}


# ── SADESATI PHASE DESCRIPTIONS ──────────────────────────────────────────────

SADESATI_PHASES = {
    "Rising": "This is the starting period of Shani's Sade Sati. Saturn transits your 12th house from the Moon. It generally indicates financial loss, problems from hidden enemies, aimless travel, disputes, and challenges. Relationship with colleagues may not be smooth and they may create problems in your work environment. You may face challenges on your domestic front creating pressure and tension. Exercise control over spending. Long distance travels may not be fruitful. Saturn's nature is of delay and dejection, but generally you will get results eventually. Take this period as a learning period, put in hard work, and things will fall in place. Avoid high risks in business matters.",
    "Peak": "This is the peak of Shani's Sade Sati. Generally this phase is the most difficult. Saturn transiting over natal Moon indicates health problems, character assassination, problems from relatives and friends, mental tension, and financial difficulties. Your patience and endurance will be tested to the maximum. Focus on maintaining your health, both physical and mental. Spiritual practices and service to others can ease the effects. This too shall pass, and the lessons learned will serve you well.",
    "Setting": "This is the final phase of Shani's Sade Sati. Saturn transits your 2nd house from the Moon. While challenges begin to ease, financial matters and family relationships still need attention. Speech and dietary habits should be monitored. This period marks the gradual end of Saturn's intense influence. The wisdom and strength gained during Sade Sati will serve as valuable assets for your future growth.",
}


# ── GHATAK (Malefic indicators by Lagna sign) ────────────────────────────────

GHATAK = {
    "Aries": {"bad_day": "Saturday", "bad_nakshatra": "Swati", "bad_rashi": "Aquarius", "bad_tithi": "2, 7, 12", "bad_yoga": "Siddha", "bad_planets": "Saturn"},
    "Taurus": {"bad_day": "Sunday", "bad_nakshatra": "Vishakha", "bad_rashi": "Pisces", "bad_tithi": "3, 8, 13", "bad_yoga": "Vyatipata", "bad_planets": "Sun"},
    "Gemini": {"bad_day": "Monday", "bad_nakshatra": "Anuradha", "bad_rashi": "Aries", "bad_tithi": "4, 9, 14", "bad_yoga": "Brahma", "bad_planets": "Moon"},
    "Cancer": {"bad_day": "Tuesday", "bad_nakshatra": "Jyeshtha", "bad_rashi": "Taurus", "bad_tithi": "5, 10, 15", "bad_yoga": "Atiganda", "bad_planets": "Mars"},
    "Leo": {"bad_day": "Wednesday", "bad_nakshatra": "Mula", "bad_rashi": "Gemini", "bad_tithi": "1, 6, 11", "bad_yoga": "Sukarman", "bad_planets": "Mercury"},
    "Virgo": {"bad_day": "Thursday", "bad_nakshatra": "Purva Ashadha", "bad_rashi": "Cancer", "bad_tithi": "2, 7, 12", "bad_yoga": "Dhriti", "bad_planets": "Jupiter"},
    "Libra": {"bad_day": "Friday", "bad_nakshatra": "Uttara Ashadha", "bad_rashi": "Leo", "bad_tithi": "3, 8, 13", "bad_yoga": "Shoola", "bad_planets": "Venus"},
    "Scorpio": {"bad_day": "Saturday", "bad_nakshatra": "Shravana", "bad_rashi": "Virgo", "bad_tithi": "4, 9, 14", "bad_yoga": "Ganda", "bad_planets": "Saturn"},
    "Sagittarius": {"bad_day": "Sunday", "bad_nakshatra": "Dhanishtha", "bad_rashi": "Libra", "bad_tithi": "5, 10, 15", "bad_yoga": "Vriddhi", "bad_planets": "Sun"},
    "Capricorn": {"bad_day": "Friday", "bad_nakshatra": "Revati", "bad_rashi": "Taurus", "bad_tithi": "1, 6, 11", "bad_yoga": "Brahma", "bad_planets": "Mercury"},
    "Aquarius": {"bad_day": "Monday", "bad_nakshatra": "Ashwini", "bad_rashi": "Gemini", "bad_tithi": "2, 7, 12", "bad_yoga": "Vishkambha", "bad_planets": "Moon"},
    "Pisces": {"bad_day": "Tuesday", "bad_nakshatra": "Bharani", "bad_rashi": "Cancer", "bad_tithi": "3, 8, 13", "bad_yoga": "Priti", "bad_planets": "Mars"},
}


# ── FAVOURABLE POINTS (by Lagna sign) ────────────────────────────────────────

FAVOURABLE = {
    "Aries": {"lucky_numbers": "9", "good_numbers": "1, 3, 5, 9", "evil_numbers": "2, 6, 8", "lucky_days": "Tuesday, Saturday, Friday", "good_planets": "Mars, Jupiter, Sun", "lucky_metal": "Copper", "lucky_stone": "Red Coral", "varna": "Kshatriya", "yoni": "Mesha", "gana": "Devta", "nadi": "Aadi"},
    "Taurus": {"lucky_numbers": "6", "good_numbers": "2, 4, 6, 8", "evil_numbers": "1, 5, 7", "lucky_days": "Friday, Wednesday, Saturday", "good_planets": "Venus, Mercury, Saturn", "lucky_metal": "Silver", "lucky_stone": "Diamond", "varna": "Vaishya", "yoni": "Gau", "gana": "Manushya", "nadi": "Madhya"},
    "Gemini": {"lucky_numbers": "5", "good_numbers": "3, 5, 7, 9", "evil_numbers": "2, 4, 6", "lucky_days": "Wednesday, Friday, Thursday", "good_planets": "Mercury, Venus, Saturn", "lucky_metal": "Gold", "lucky_stone": "Emerald", "varna": "Shudra", "yoni": "Sarpa", "gana": "Devta", "nadi": "Antya"},
    "Cancer": {"lucky_numbers": "2", "good_numbers": "1, 2, 4, 7", "evil_numbers": "3, 5, 8", "lucky_days": "Monday, Thursday, Sunday", "good_planets": "Moon, Mars, Jupiter", "lucky_metal": "Silver", "lucky_stone": "Pearl", "varna": "Bramhin", "yoni": "Shwan", "gana": "Devta", "nadi": "Aadi"},
    "Leo": {"lucky_numbers": "1", "good_numbers": "1, 3, 5, 9", "evil_numbers": "2, 6, 8", "lucky_days": "Sunday, Tuesday, Wednesday", "good_planets": "Sun, Mars, Jupiter", "lucky_metal": "Gold", "lucky_stone": "Ruby", "varna": "Kshatriya", "yoni": "Mushak", "gana": "Manushya", "nadi": "Madhya"},
    "Virgo": {"lucky_numbers": "5", "good_numbers": "2, 4, 5, 8", "evil_numbers": "1, 3, 9", "lucky_days": "Wednesday, Friday, Monday", "good_planets": "Mercury, Venus, Saturn", "lucky_metal": "Bronze", "lucky_stone": "Emerald", "varna": "Vaishya", "yoni": "Gau", "gana": "Devta", "nadi": "Antya"},
    "Libra": {"lucky_numbers": "6", "good_numbers": "2, 6, 7, 8", "evil_numbers": "1, 5, 9", "lucky_days": "Friday, Wednesday, Saturday", "good_planets": "Venus, Mercury, Saturn", "lucky_metal": "Silver", "lucky_stone": "Diamond", "varna": "Shudra", "yoni": "Mriga", "gana": "Manushya", "nadi": "Aadi"},
    "Scorpio": {"lucky_numbers": "9", "good_numbers": "1, 3, 7, 9", "evil_numbers": "2, 4, 6", "lucky_days": "Tuesday, Thursday, Sunday", "good_planets": "Mars, Jupiter, Moon", "lucky_metal": "Copper", "lucky_stone": "Red Coral", "varna": "Bramhin", "yoni": "Mriga", "gana": "Rakshasa", "nadi": "Madhya"},
    "Sagittarius": {"lucky_numbers": "3", "good_numbers": "1, 3, 5, 8", "evil_numbers": "2, 6, 7", "lucky_days": "Thursday, Tuesday, Sunday", "good_planets": "Jupiter, Sun, Mars", "lucky_metal": "Gold", "lucky_stone": "Yellow Sapphire", "varna": "Kshatriya", "yoni": "Ashwa", "gana": "Devta", "nadi": "Antya"},
    "Capricorn": {"lucky_numbers": "4", "good_numbers": "2, 4, 5, 8", "evil_numbers": "1, 7, 9", "lucky_days": "Thursday, Tuesday", "good_planets": "Jupiter, Mars, Moon", "lucky_metal": "Gold", "lucky_stone": "Red Coral", "varna": "Bramhin", "yoni": "Mriga", "gana": "Devta", "nadi": "Madhya"},
    "Aquarius": {"lucky_numbers": "8", "good_numbers": "2, 4, 6, 8", "evil_numbers": "1, 3, 9", "lucky_days": "Saturday, Friday, Wednesday", "good_planets": "Saturn, Venus, Mercury", "lucky_metal": "Iron", "lucky_stone": "Blue Sapphire", "varna": "Shudra", "yoni": "Ashwa", "gana": "Manushya", "nadi": "Aadi"},
    "Pisces": {"lucky_numbers": "3", "good_numbers": "1, 3, 7, 9", "evil_numbers": "2, 5, 8", "lucky_days": "Thursday, Tuesday, Sunday", "good_planets": "Jupiter, Moon, Mars", "lucky_metal": "Gold", "lucky_stone": "Yellow Sapphire", "varna": "Bramhin", "yoni": "Gau", "gana": "Devta", "nadi": "Antya"},
}


# ── BHAVA (House) Analysis ─────────────────────────────────────────────────────

BHAVA_DATA = {
    1: {
        "name": "First House (Lagna / Ascendant)",
        "signification": "Self, Personality, Physical Body, Health, Vitality",
        "description": "The First House, known as the Lagna or Ascendant, is the most important house in the birth chart. It represents your physical body, overall health, personality, temperament, and how you present yourself to the world. The sign on the cusp of this house and any planets placed here significantly shape your character and life direction.\n\nA strong First House gives good health, confidence, and a magnetic personality. Benefic planets here bestow charm, intelligence, and success in life. Malefic planets may create health challenges or a combative nature, but can also give tremendous willpower and determination. The lord of the First House and its placement reveal the overall direction and quality of life.",
    },
    2: {
        "name": "Second House (Dhana Bhava)",
        "signification": "Wealth, Family, Speech, Food, Right Eye",
        "description": "The Second House governs accumulated wealth, family lineage, speech, and food habits. It is one of the primary houses for financial prosperity and is called Dhana Bhava (House of Wealth). This house also rules the face, right eye, and oral cavity.\n\nBenefic planets in the Second House bestow eloquent speech, a harmonious family life, and steady wealth accumulation. The native may enjoy good food and have a pleasant voice. Malefic planets here can create harsh speech, family disputes, or difficulties in saving money. The lord of the Second House and its dignity determine the native's financial stability and relationship with family.",
    },
    3: {
        "name": "Third House (Sahaja Bhava)",
        "signification": "Siblings, Courage, Communication, Short Journeys, Efforts",
        "description": "The Third House represents younger siblings, courage, valor, mental strength, and all forms of communication. It governs short travels, writing, media, and the use of hands. This house shows your initiative, self-effort, and ability to take bold actions.\n\nA strong Third House with benefic influences gives excellent communication skills, good relationships with siblings, and the courage to pursue goals. The native may excel in writing, journalism, or performing arts. Malefic planets here can give restlessness, strained sibling relationships, or hearing problems, but also immense physical courage and athletic ability.",
    },
    4: {
        "name": "Fourth House (Sukha Bhava)",
        "signification": "Mother, Home, Property, Vehicles, Emotional Peace",
        "description": "The Fourth House is the house of domestic happiness, mother, property, vehicles, and emotional well-being. Known as Sukha Bhava (House of Happiness), it represents your roots, homeland, and inner peace. This house governs real estate, agriculture, and formal education.\n\nBenefic planets in the Fourth House bless the native with a loving mother, comfortable home, vehicles, and deep emotional satisfaction. There may be ancestral property and a strong connection to one's homeland. Malefic planets can create domestic disturbances, property disputes, or emotional turbulence, but may also give determination to build wealth from scratch.",
    },
    5: {
        "name": "Fifth House (Putra Bhava)",
        "signification": "Children, Intelligence, Creativity, Romance, Past Merit",
        "description": "The Fifth House governs children, intelligence, creativity, romance, and past-life merits (Purva Punya). It is one of the most auspicious houses, representing your creative expression, speculative gains, and higher learning. This house also rules the stomach and digestive system.\n\nA strong Fifth House with benefic planets gives intelligent and obedient children, sharp intellect, success in creative pursuits, and gains from speculation or investments. The native may have a strong spiritual inclination and good fortune from past-life merits. Malefic influences can delay childbirth, create digestive issues, or lead to poor investment decisions.",
    },
    6: {
        "name": "Sixth House (Ripu Bhava)",
        "signification": "Enemies, Disease, Debts, Service, Daily Work",
        "description": "The Sixth House represents enemies, diseases, debts, obstacles, and daily work or service. While it is classified as a Dusthana (difficult house), it also governs the ability to overcome challenges, compete, and serve others. This house rules the immune system and healing abilities.\n\nBenefic planets in the Sixth House give victory over enemies, good health, and success in competitive fields like law, medicine, or sports. The native may excel in service-oriented professions. Malefic planets here can actually be beneficial (Vipareet Raja Yoga), giving the strength to destroy obstacles. However, they may also indicate chronic health issues, legal troubles, or debt accumulation.",
    },
    7: {
        "name": "Seventh House (Kalatra Bhava)",
        "signification": "Marriage, Spouse, Partnership, Business, Foreign Travel",
        "description": "The Seventh House is the house of marriage, spouse, partnerships, and all forms of one-on-one relationships. It governs business partnerships, foreign travel, and public dealings. This house sits directly opposite the Ascendant and represents how others perceive you.\n\nBenefic planets in the Seventh House bless the native with a loving, supportive spouse and successful partnerships. Marriage brings happiness and prosperity. The native may excel in business and enjoy foreign travel. Malefic planets can create marital difficulties, delays in marriage, or challenging business partnerships, but may also give a strong, independent spouse.",
    },
    8: {
        "name": "Eighth House (Ayur Bhava)",
        "signification": "Longevity, Transformation, Occult, Inheritance, Sudden Events",
        "description": "The Eighth House governs longevity, death, transformation, occult sciences, inheritance, and sudden unexpected events. It represents hidden wealth, insurance, spouse's finances, and deep research. This house is associated with mysteries, secrets, and the unknown.\n\nBenefic planets in the Eighth House can give long life, sudden gains through inheritance or insurance, and deep interest in occult or spiritual sciences. The native may have healing abilities or psychic intuition. Malefic planets here can create health crises, accidents, or chronic ailments, but also give tremendous resilience and the ability to transform through adversity.",
    },
    9: {
        "name": "Ninth House (Dharma Bhava)",
        "signification": "Fortune, Father, Religion, Higher Education, Long Journeys",
        "description": "The Ninth House is the most auspicious house in the chart, representing fortune, dharma (righteous path), father, guru, higher education, and long-distance travel. Known as the house of Bhagya (luck), it governs philosophy, religion, law, and spiritual wisdom.\n\nA strong Ninth House with benefic planets is one of the greatest blessings in a birth chart. It gives good fortune, a wise father, opportunities for higher education, and spiritual growth. The native may travel abroad, receive blessings from teachers, and lead a righteous life. Malefic planets can create difficulties with father, obstacles in higher education, or challenges with faith and belief systems.",
    },
    10: {
        "name": "Tenth House (Karma Bhava)",
        "signification": "Career, Profession, Status, Authority, Fame",
        "description": "The Tenth House represents career, profession, social status, authority, and public reputation. Known as Karma Bhava, it shows your life's work, achievements, and contribution to society. This house governs government, administration, and the relationship with authority figures.\n\nBenefic planets in the Tenth House give a successful career, high social standing, and recognition for achievements. The native may hold positions of authority and earn fame through professional accomplishments. Strong planets here can indicate government positions, leadership roles, or entrepreneurial success. Malefic planets may create career obstacles or controversies but can also drive intense ambition.",
    },
    11: {
        "name": "Eleventh House (Labha Bhava)",
        "signification": "Gains, Income, Friends, Elder Siblings, Aspirations",
        "description": "The Eleventh House governs gains, income, profits, friendships, elder siblings, and the fulfillment of desires. Known as Labha Bhava (House of Gains), it represents networking, social circles, and financial growth beyond regular income. This house shows your ability to manifest aspirations.\n\nBenefic planets in the Eleventh House give excellent financial gains, a strong social network, supportive friends, and the fulfillment of desires. The native may have influential connections and benefit from group activities. This is one of the best houses for wealth accumulation. Malefic planets here can create unreliable friendships or strained relationships with elder siblings, but may still give substantial material gains.",
    },
    12: {
        "name": "Twelfth House (Vyaya Bhava)",
        "signification": "Expenses, Losses, Foreign Lands, Spirituality, Liberation",
        "description": "The Twelfth House represents expenses, losses, foreign lands, spirituality, liberation (moksha), and the subconscious mind. While often considered challenging, it is the house of final emancipation and spiritual transcendence. It governs sleep, dreams, hospitals, and isolated places.\n\nBenefic planets in the Twelfth House give spiritual inclination, foreign travel or settlement, charitable nature, and peaceful sleep. The native may find success in foreign lands or in spiritual/healing professions. Jupiter here is especially auspicious, promising spiritual growth and eventual liberation. Malefic planets can create excessive expenses, sleep disorders, or feelings of isolation, but may also drive deep spiritual seeking.",
    },
}
