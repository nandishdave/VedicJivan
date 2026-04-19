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
        "education": "You are a quick learner but impatient with slow, methodical study. You excel in subjects that involve action, debate, and physical practice — engineering, sports science, military training, and surgery. You may abandon prolonged courses, so intensive bursts of focused study suit you better than long, drawn-out programs. Your concentration sharpens dramatically when the subject matter excites your competitive spirit.",
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
        "education": "You are a methodical, persistent, and thorough learner who retains what you study remarkably well. You prefer practical, applied subjects — finance, agriculture, fine arts, music, culinary arts, and architecture. You are slow to start but excellent at completion, and you benefit greatly from a calm, well-organized study environment. Distractions and disorder hurt your focus, so a steady routine is essential.",
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
        "education": "You are a brilliant and quick-witted student with a sharp intellect. Multiple interests can scatter your focus, but you absorb languages, literature, mathematics, and communication-based subjects with ease. You learn best in interactive settings — debates, group discussions, and hands-on projects. Avoid spreading yourself too thin across too many fields, and discipline yourself to finish what you start.",
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
        "education": "You are an emotionally engaged learner who studies best in a familiar, supportive environment. You excel in history, psychology, literature, home science, and any subject that involves caring for others. You have a strong memory and an intuitive grasp of what you study. Mood swings can affect your academic performance, so emotional stability and a peaceful study space are key to consistent results.",
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
        "education": "You are a confident and ambitious student who shines in subjects involving leadership, performing arts, politics, and management. You prefer recognition for your work and may struggle with subjects that demand quiet, behind-the-scenes effort. Public speaking and creative presentations come naturally to you. You learn best when you can see how the knowledge will translate into stature, achievement, or visible success.",
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
        "education": "You are a diligent, analytical, and detail-obsessed scholar. You excel in science, medicine, mathematics, accounting, and research. Your perfectionist nature means you study thoroughly, but it can also be derailed by anxiety and self-criticism. You benefit from clear schedules, methodical revision, and learning to accept that 'good enough' is sometimes better than chasing the unattainable perfect.",
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
        "education": "You are a balanced and harmonious learner who excels in arts, law, design, social sciences, and counseling. You learn well through partnership — study groups, peer discussions, and collaborative projects bring out your best. Indecisiveness can delay choosing a specialization, so trust your refined sense of judgment and commit. Beautiful surroundings and pleasant company aid your concentration significantly.",
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
        "education": "You are a deep, intense, and penetrating researcher who goes far beyond surface knowledge in any subject. You excel in research, medicine, psychology, occult sciences, and investigation. You prefer to master a few subjects in great depth rather than covering many superficially. You are often secretive about your study methods and may pursue knowledge that conventional curricula avoid.",
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
        "education": "You are a philosophical, curious, and broad-minded learner. You excel in higher education — law, philosophy, religion, foreign languages, and travel-related studies. You may be drawn to study abroad or in spiritual ashrams. Your love of freedom can make rigid academic structures challenging, so choose programs that allow exploration and connection between disciplines rather than narrow specialization.",
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
        "education": "You tend to keep wandering in various places, which is why the idea of studying for a prolonged period may not be entertained by you. But if you gain victory over your lethargic nature, you will perform well in your studies. You have a curious mind about unfamiliar things. Your imagination skills will grant you considerable success in your respective subjects. You should try to boost your concentration power so that you can perform better in examinations.",
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
        "education": "You are an innovative, original, and independent learner. You excel in technology, science, social sciences, and humanitarian studies. You may be ahead of your time and bored by conventional curricula. Group learning, online courses, and unconventional teaching methods suit you best. You learn most when you can connect ideas across disciplines and apply them to a larger social purpose.",
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
        "education": "You are an imaginative, intuitive, and absorptive learner. You excel in arts, music, spirituality, healing professions, and humanities. Your dreamy nature can interfere with structured study, so meditation and creative visualization help focus your mind. Inspiration matters more to you than rigid discipline. Choose subjects that allow you to engage your imagination and serve others, and academic success will follow naturally.",
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


# ── VARSHAPHAL — Muntha by Bhava (12 entries) ──────────────────────────────
# Muntha is a sensitive point in Tajik (annual) astrology that advances one
# sign per completed year of age, starting from the natal Lagna. Its bhava
# placement in the annual chart frames the dominant theme of the year.

MUNTHA_HOUSE_DATA = {
    1: "Muntha in 1st Bhav: A year focused squarely on yourself — health, identity, and personal initiatives take centre stage. New beginnings are favoured, and your willpower runs strong. Watch for impulsive decisions and pay attention to physical well-being, especially the head and face.",
    2: "Muntha in 2nd Bhav: Wealth, family matters, and your manner of speech come into focus this year. There may be steady financial accumulation and improved standing within the family, though arguments at home can flare up. Be mindful with your words; what you say carries unusual weight now.",
    3: "Muntha in 3rd Bhav: Courage, communication, and relationships with siblings dominate the year. You may take bold initiatives, undertake short journeys, and assert yourself more than usual. Writing, marketing, or any work that depends on your voice tends to do well.",
    4: "Muntha in 4th Bhav: Home, mother, and emotional security become the central themes. Property matters, vehicle changes, or a renovation of your living space are likely. Inner peace depends on resolving domestic issues — buried family tensions may rise to the surface for healing.",
    5: "Muntha in 5th Bhav: A creative, romantic, and intellectually rich year. Children, love affairs, learning, and speculative pursuits flourish. Avoid reckless gambling and overconfidence in investments. This is a good year to teach, study, or create.",
    6: "Muntha in 6th Bhav: Service, struggles, and overcoming opponents define the year. You may face debts, health challenges, or workplace conflicts, but you also gain the strength to overcome them. Discipline in diet and routine pays off; competitive endeavours go in your favour.",
    7: "Muntha in 7th Bhav: Partnerships — marital, business, or public — take centre stage. Marriage, contracts, or major collaborations are highly likely. Foreign travel and dealings with strangers increase. Mind your dealings with the spouse; harmony or friction here will colour the whole year.",
    8: "Muntha in 8th Bhav: A year of transformation, hidden matters, and unexpected change. Inheritance, insurance, occult studies, or research may bring gains, but sudden losses, surgery, or psychological turbulence can also surface. Approach the year with introspection rather than aggression.",
    9: "Muntha in 9th Bhav: Luck, dharma, higher learning, and long journeys come to the fore. Pilgrimages, spiritual study, university work, or interactions with mentors and gurus go well. Father-related matters and legal affairs see resolution. Generally one of the most fortunate Muntha placements.",
    10: "Muntha in 10th Bhav: Career, status, and public recognition are the year's defining themes. Promotion, professional change, or increased authority is likely, often coupled with extra responsibility. Reputation matters more than ever — guard against actions that could damage your standing.",
    11: "Muntha in 11th Bhav: Gains, fulfilled desires, and expanded social networks mark the year. Income tends to rise, friendships deepen, and long-pending wishes find resolution. Excellent for joining groups, launching networked ventures, or harvesting investments made earlier.",
    12: "Muntha in 12th Bhav: A year tilted toward expenses, foreign matters, spirituality, and behind-the-scenes work. Expect higher outflows, possible relocation or travel abroad, and a pull toward solitude or meditation. Hidden enemies may emerge — keep your plans private and focus on inner growth.",
}


# ── VARSHAPHAL — Mudda Dasha lord × Bhava (9 × 12 = 108 entries) ───────────
# During Varshaphal (annual horoscope), the Mudda Dasha sub-period predictions
# depend on the dasha lord's house placement in the ANNUAL chart (cast at the
# solar return), not the natal chart. Lookup:
# MUDDA_DASHA_BHAV_DATA[planet][bhav_number] → paragraph string.

MUDDA_DASHA_BHAV_DATA = {
    "Sun": {
        1: "Sun in Bhav 1 during this period: your vitality and personal authority will rise sharply, drawing attention from superiors and peers alike. Career visibility improves and people will look to you for direction, though pride or ego could strain a close relationship. Watch your blood pressure and eyes; favor light food and morning sun. A good window to launch a personal brand or step into a leadership role.",
        2: "Sun in Bhav 2 during this period: focus shifts to money, family standing and the words you choose. You may receive a salary hike, bonus or recognition through family lineage, but spending on status symbols can climb just as quickly. Speak with measured authority — harsh speech now creates lasting friction. Take care of teeth, throat and right eye; small dental or vision issues are best addressed early.",
        3: "Sun in Bhav 3 during this period: courage, initiative and short journeys define the months ahead. You will push past hesitation, take calculated risks, and possibly take charge of a sibling or younger colleague's situation. Communication and self-promotion go well, especially in writing or public speaking. Avoid overexertion of arms and shoulders; channel the surplus energy into structured exercise rather than impulsive arguments.",
        4: "Sun in Bhav 4 during this period: home and mother become the stage. There may be renovations, a vehicle purchase, or relocation tied to work, alongside some friction with elders over decisions. Emotional comfort can dip even as material comfort grows; carve out quiet evenings. Property matters favor formal agreements signed in daylight, and a long-pending domestic issue can finally be cleared with directness.",
        5: "Sun in Bhav 5 during this period: creativity, children and learning come into focus. Students perform well in exams and competitive selections; parents may celebrate a milestone for a child. Speculative gains are possible but volatile — keep position sizes small. A romantic relationship gains seriousness or, if already strained, faces a frank reckoning. Devotional practice and study of classical subjects feel especially rewarding now.",
        6: "Sun in Bhav 6 during this period: a strong year for defeating opponents, clearing debts and recovering from chronic complaints. Workload at the office rises but so does your standing among colleagues; expect a promotion or expanded responsibility. Legal and disciplinary matters tilt in your favor if you act with integrity. Guard against acidity, fevers and inflammation; routine matters more than intensity in workouts.",
        7: "Sun in Bhav 7 during this period: partnerships — marital and business — take centre stage and demand your direct engagement. A spouse or partner may seek more autonomy, or your own ego could clash with theirs; honest conversation prevents drift. Public dealings, contracts and travel for collaboration are favored. Avoid signing under pressure; let the other side reveal their hand first. Health of the partner deserves attention.",
        8: "Sun in Bhav 8 during this period: transformation, inheritance and hidden matters surface. You may receive ancestral money, insurance settlement or a sudden positional shift, but bureaucratic delays are likely. Research, occult studies and deep introspection bring genuine breakthroughs. Take father's health seriously and avoid risky travel or extreme sports. Old secrets — yours or others' — could come to light, so handle disclosures with care.",
        9: "Sun in Bhav 9 during this period: dharma, mentors and long journeys bless the year. You will feel pulled toward higher learning, pilgrimage or a new philosophical framework, and a senior figure may open doors that effort alone could not. Foreign travel for work or study is well-aspected. Father-related news tends to be significant. Teaching, publishing and ethical leadership all bring tangible rewards now.",
        10: "Sun in Bhav 10 during this period: one of the most powerful placements for career advancement. Recognition from authorities, government dealings, promotion or public success becomes very likely if you have prepared the ground. Work hours grow long and family time shrinks, so guard the balance. Reputation is your real asset this year — protect it from any shortcut. Honors, awards or media attention are realistically within reach.",
        11: "Sun in Bhav 11 during this period: gains, network and elder sibling matters dominate. Income from primary source rises, and influential friends actively support your goals. A long-held wish moves visibly closer. Be selective about which circles you join; one wrong alliance can dim your light. Recognition within professional bodies, clubs or associations is likely, and group leadership roles may land in your lap.",
        12: "Sun in Bhav 12 during this period: expenses, foreign matters and inner life come forward. Spending on travel, charity, medical care or a parent can climb, and visibility at work may temporarily reduce as you handle behind-the-scenes work. Sleep, eyes and overall vitality need protection — avoid late nights. A retreat, solo trip or quiet spiritual practice will restore you more than any social effort could.",
    },
    "Moon": {
        1: "Moon in Bhav 1 during this period: emotions colour everything you do, for better and worse. You become more approachable, intuitive and well-liked, and women in your circle play a supportive role. Mood swings are likely, so anchor yourself with sleep, water and a steady morning routine. Travel near water is enjoyable. Public-facing or creative work flourishes, but avoid making major decisions on a low-energy day.",
        2: "Moon in Bhav 2 during this period: family bonds, food and finances dominate. Income flows steadily, often through nurturing roles, hospitality or work connected to women. Speech becomes softer and more persuasive — useful in negotiations. Guard against emotional eating and impulse purchases. A family gathering, wedding or ritual is likely, and your maternal side of the family may feature prominently in good news.",
        3: "Moon in Bhav 3 during this period: short trips, siblings and creative communication lift your year. Writing, music and content work attract a warm response, and a sister or close friend offers timely support. Courage is moderate rather than fiery — you will act when comfortable, not before. Watch overthinking before bed. A new skill picked up casually now can become genuinely useful within months.",
        4: "Moon in Bhav 4 during this period: one of the most comforting placements. Home life is harmonious, mother's well-being improves, and you may upgrade your living space or vehicle. Emotional security feels restored after recent strain. Real estate dealings are favorable, especially properties near water. Avoid overattachment to past grievances; the year rewards softness over stubbornness, and a long-cherished domestic plan finally takes shape.",
        5: "Moon in Bhav 5 during this period: romance, children and creative joy bloom. Conception or news of a child is possible for those trying; existing children bring genuine pride. Studies, especially in arts or counselling, go well. Light speculation can pay off but stay modest. You will feel more romantic and playful than usual — a good year to invest in a relationship rather than test it.",
        6: "Moon in Bhav 6 during this period: emotional ups and downs at work and minor recurring health issues need attention. You may take on caregiving for a relative or pet, which is meaningful but draining. Debts can be repaid steadily; new loans should be avoided. Female colleagues or clients prove allies. Watch digestion, sleep and anxiety; gentle routines outperform intense interventions this year.",
        7: "Moon in Bhav 7 during this period: partnerships become more emotionally rich. Spouse's mood and well-being shape the household tone, and a single person may meet someone significant through social or family channels. Business partnerships with women are favored. Public dealings go smoothly when you lead with empathy. Avoid moodiness in negotiations — clarity now prevents misunderstandings that could echo for months.",
        8: "Moon in Bhav 8 during this period: emotional intensity, dreams and hidden matters surface. You may handle a sensitive family secret, an inheritance, or a deep psychological shift. Mother's health deserves a check-up. Avoid water-based adventures and risky travel. Healing modalities, therapy and journaling work especially well now, and a fear you have carried for years can finally lose its grip.",
        9: "Moon in Bhav 9 during this period: long travels, often connected with family, mother or pilgrimage, become a highlight. Faith deepens through experience rather than argument, and a teacher or elder offers exactly the perspective you need. Studies abroad or remote learning programs are favored. Publishing, teaching and culturally-rooted work attract attention. A trip to a riverside or coastal sacred site would be deeply restorative.",
        10: "Moon in Bhav 10 during this period: career gains a public, people-facing dimension. Roles in hospitality, healthcare, food, media or care work flourish, and women in authority support your rise. Reputation grows through warmth rather than aggression. Some changes in workplace or role are likely; ride the wave instead of resisting. Mother may take pride in a public milestone you achieve this year.",
        11: "Moon in Bhav 11 during this period: friends, networks and steady gains brighten the year. Income from multiple small streams adds up, and a long-held emotional wish — often related to family — gets fulfilled. Female friends are particularly supportive. Group activities, communities and clubs become a source of joy. Be selective with new acquaintances; not every warm face deserves your full trust just yet.",
        12: "Moon in Bhav 12 during this period: inner life, sleep and foreign matters come into focus. You may travel abroad, spend on a parent's care, or withdraw socially to recharge. Dreams become vivid and meaningful. Meditation, art and time near water heal more than any new venture would. Watch tendency toward melancholy; a small daily routine of light, movement and music keeps the mood steady.",
    },
    "Mars": {
        1: "Mars in Bhav 1 during this period: energy, courage and physical drive surge. You will push initiatives that have been stalled and may take a bold personal stand. Anger flares quickly though, and accidents, cuts or fevers are possible — channel the heat into exercise. Confidence is magnetic and others fall in line. A good window to start something demanding, provided you don't bulldoze the relationships around you.",
        2: "Mars in Bhav 2 during this period: finances and speech both heat up. Income can rise through bold action, but harsh words risk damaging family ties. Avoid lending money and signing under pressure. Dental work, throat issues or eye strain may need attention. Family conflicts over property or inheritance are possible; address them with facts rather than emotion. Disciplined budgeting protects the year's gains.",
        3: "Mars in Bhav 3 during this period: arguably one of Mars's best placements. Courage soars, initiatives succeed, and short trips bring tangible results. Relationships with siblings — especially younger ones — turn dynamic; some friction is possible, but so is genuine teamwork. Sales, sports, military and entrepreneurial efforts thrive. Hands, arms and shoulders need care during workouts. Self-promotion that felt awkward before now feels natural.",
        4: "Mars in Bhav 4 during this period: tensions at home and possible property disputes. A need to act decisively about your living situation arises; renovation, relocation or a vehicle change is likely. Mother's health and peace of mind deserve attention. Physical exertion pays off, but burning the candle too hard invites minor accidents. Resist slamming doors — both literal and metaphorical — when negotiations get heated.",
        5: "Mars in Bhav 5 during this period: passion, competition and risk dominate. Speculative ventures can win or lose big; small position sizes are wise. Children may be more headstrong than usual, especially sons. Romance is intense but argumentative. Sports, competitive exams and creative pitches do well. A miscarriage risk exists for couples expecting; medical caution and rest are essential during the early months.",
        6: "Mars in Bhav 6 during this period: excellent for defeating enemies, winning lawsuits and clearing debts. Workplace rivals retreat once you confront them clearly. Surgeries, if needed, succeed. Watch for inflammation, fevers, blood-related issues and accidents with sharp tools. Service-oriented roles, military, police and emergency work thrive. Loans can be repaid faster than expected; resist the urge to take on new ones for status reasons.",
        7: "Mars in Bhav 7 during this period: partnerships and marriage feel charged. Arguments with spouse or business partner are likely, and a power struggle may surface. Direct dialogue settles it; silence makes it fester. Public dealings demand restraint. Single people may meet someone fiery and attractive but volatile. Health of the partner needs attention. Travel for partnership matters is likely and largely productive.",
        8: "Mars in Bhav 8 during this period: a sensitive placement requiring care. Risk of accidents, surgeries or sudden financial shocks rises; insurance and medical check-ups are wise. Research, investigation and occult work bring breakthroughs. Inheritance or partner's money may come with disputes attached. Avoid risky travel, extreme sports and confrontations with strangers. Deep transformation is offered if you face fears squarely instead of reacting.",
        9: "Mars in Bhav 9 during this period: a fighter's faith and bold journeys. You will defend your principles publicly, possibly travel to challenging destinations and take initiative in higher learning or publishing. A guru or mentor may push you firmly out of your comfort zone. Father's energy or health may be intense. Legal matters tied to property abroad can move forward. Avoid religious arguments — not every battle is yours.",
        10: "Mars in Bhav 10 during this period: career action and visible achievement. Promotions through bold execution, project leadership and competitive wins are very likely. Government, defense, engineering and entrepreneurial roles flourish. Workplace politics heats up; pick battles carefully. Long hours could strain home life. Reputation grows fast, but so do enemies of progress; document decisions and keep a paper trail to protect what you build.",
        11: "Mars in Bhav 11 during this period: powerful gains, especially through your own initiative. Income spikes through new ventures, sales or commissions, and influential allies join your cause. Elder sibling matters take a positive turn. Group leadership roles open up. Be cautious with who you bring into business; one impulsive partnership choice can leak the year's profits. Fitness goals and competitive sports also reward effort.",
        12: "Mars in Bhav 12 during this period: hidden enemies, expenses and foreign matters rise. Spending on litigation, medical care or a parent can spike. Sleep is disturbed; fiery dreams and restlessness need outlets like exercise and breathwork. A foreign trip or relocation for work is possible. Avoid impulsive decisions made in frustration. Solitary practice — gym, martial arts, meditation — channels the energy more cleanly than confrontation.",
    },
    "Mercury": {
        1: "Mercury in Bhav 1 during this period: intellect, wit and communication shine. You will think faster, write better and connect new dots in your work. Networking comes easily, and a youthful energy returns to your demeanor. Skin and nervous system can feel sensitive — moderate caffeine and screen time. A good year to study, publish, pitch ideas, or rebrand yourself professionally. Avoid overcommitting just because everything feels possible.",
        2: "Mercury in Bhav 2 during this period: a strong year for finances through skill, communication and trade. Income rises through writing, speaking, teaching, accounting or commerce. Family discussions become more rational and less heated. Watch for overpromising in speech; words are contracts now. Investments in stocks, mutual funds or short-term instruments perform well with research-backed picks. Light, varied food suits your constitution this year.",
        3: "Mercury in Bhav 3 during this period: an outstanding placement for writers, marketers, content creators and entrepreneurs. Short journeys multiply, ideas convert into projects quickly, and a sibling or peer becomes a key collaborator. Skill-building courses pay off rapidly. Hands, fingers and breathing deserve some care from screen overuse. Self-publishing, podcasts, newsletters or any communication-driven side venture launched now can gain real momentum.",
        4: "Mercury in Bhav 4 during this period: home life intellectualizes — conversations replace silences, and you may set up a study, library or remote-work corner. Vehicle, gadget or property purchases tied to communication are likely. Mother's health is generally fine but mental restlessness needs care. Real estate negotiations favor the well-prepared. A move or renovation focused on creating a calmer, more functional space brings lasting value.",
        5: "Mercury in Bhav 5 during this period: students, writers, traders and creators thrive. Exams, certifications and competitive selections go well with disciplined study. Children's education progresses; you may invest in tutoring or creative classes for them. Romance becomes witty and conversational. Speculation can pay if research-led, but avoid tips and rumors. Mantra practice or learning a sacred text adds an unexpected steadiness to the year.",
        6: "Mercury in Bhav 6 during this period: detail-oriented work, service roles and analytical problem-solving bring success. Debts can be cleared through careful planning, and lawsuits favor the side with better documentation — usually you. Watch nervous-system issues, skin allergies and digestion. Workplace disputes resolve through correspondence rather than confrontation. A pet may bring joy or require care. Routine, lists and process give you an edge this year.",
        7: "Mercury in Bhav 7 during this period: partnerships work best when communication is frequent and clear. Contracts, negotiations and joint ventures move forward smoothly. Spouse may pursue learning, writing or business ventures of their own. Singles may meet a partner who is articulate, witty or younger. Travel for partnerships is likely. Read the fine print on every agreement; small clauses missed now create big issues later.",
        8: "Mercury in Bhav 8 during this period: research, investigation, occult studies and analytical depth bring rewards. Inheritance or partner's money may involve paperwork — handle it meticulously. Hidden information surfaces and you become the one who pieces it together. Watch for nervous strain, anxiety and skin issues. Therapy, journaling and breathwork are deeply helpful. Avoid signing financial documents in a hurry, especially loans or insurance contracts.",
        9: "Mercury in Bhav 9 during this period: higher education, publishing and travel for learning shine. You may enroll in a course, write a thesis, or start a teaching role. Travel to foreign destinations for study or business is favored. Mentors are often younger or more nimble than expected. Legal matters move forward through documentation. Faith deepens through reading and discussion rather than ritual alone this year.",
        10: "Mercury in Bhav 10 during this period: career growth through skill, communication and intellect. Roles in writing, marketing, IT, finance, education, consulting and trade flourish. Public speaking, presentations and proposals open new doors. Reputation grows for being the clear thinker in the room. Workload is high but manageable with good systems. A career pivot toward a more knowledge-driven role is realistically on the table.",
        11: "Mercury in Bhav 11 during this period: gains through networking, technology, trade and intellectual peers. Income rises through multiple streams, often involving communication or skill-sharing. Younger friends and online communities become especially valuable. A long-held goal centered on knowledge, publishing or a side business gets fulfilled. Avoid over-talking your plans before they materialize — keep some cards close while building credibility steadily.",
        12: "Mercury in Bhav 12 during this period: behind-the-scenes work, foreign clients and inner study come forward. Writing in solitude, research, translation or work for overseas clients can flourish. Expenses on books, courses or technology rise. Watch nervous exhaustion, sleep and anxiety; reduce input and create thinking space. A foreign opportunity may arrive quietly through email or referral; respond promptly even if it seems small at first.",
    },
    "Jupiter": {
        1: "Jupiter in Bhav 1 during this period: one of the most fortunate placements. Wisdom, optimism and a sense of purpose return. Health improves, weight may climb gently, and people instinctively trust your judgement. A spiritual teacher, mentor or significant book enters your life. A good year to teach, marry, conceive, or start a long-term project; the universe seems to clear obstacles you used to find paralyzing.",
        2: "Jupiter in Bhav 2 during this period: family wealth, savings and speech all expand. Income grows through ethical means, often with a teaching, advisory or financial flavor. Family events — marriage, naming ceremony, religious gathering — are likely. Speech becomes more authoritative and people listen. Watch weight and sugar, as Jupiter can be generous with both. A long-pending family matter resolves through a wise elder's intervention.",
        3: "Jupiter in Bhav 3 during this period: courage tempered with wisdom. You will take initiatives that are bold yet considered, and a sibling may become a genuine ally. Short pilgrimages and educational trips are favored. Writing, teaching and publishing efforts go well. Self-promotion with substance behind it works better than flash. A mentorship role offered to you now can shape your reputation for years to come.",
        4: "Jupiter in Bhav 4 during this period: deeply auspicious for home, mother and inner peace. Property purchase, vehicle upgrade or home renovation is highly favored. Mother's health and happiness improve, and family bonds strengthen. Spiritual practice at home becomes natural. A long-cherished dream of owning a particular kind of space can materialize. Real estate transactions tend to favor you, especially if linked to family heritage.",
        5: "Jupiter in Bhav 5 during this period: children, learning and creativity flourish. Conception or birth of a child is highly favored, especially for those trying. Existing children achieve milestones that bring pride. Higher studies, teaching and creative pursuits succeed. Romance becomes meaningful rather than merely fun. Speculative gains are possible with restraint. Mantra, study of scripture and devotional practice yield unusually deep results this year.",
        6: "Jupiter in Bhav 6 during this period: a calm year for handling enemies, debts and disease. Conflicts dissolve through dialogue rather than escalation, lawsuits favor your side, and chronic conditions improve with the right practitioner. Workplace rivals lose interest. Some weight gain or liver-related care may be needed. Service to elders, animals or those in need brings unexpected blessings — and quietly transforms how you see your own difficulties.",
        7: "Jupiter in Bhav 7 during this period: an exceptional year for partnerships. Marriage is highly favored for singles, and existing relationships deepen with mutual respect. Business partnerships expand, and consulting or advisory work attracts quality clients. Public dealings go smoothly. Spouse may achieve something meaningful. Travel with partner is rewarding. Counselling, mediation and contracts all benefit from your presence; you become the wise voice in the room.",
        8: "Jupiter in Bhav 8 during this period: inheritance, insurance and joint finances bring positive surprises. Research, occult studies and deep philosophical work reach new levels. A long-held fear or trauma can be processed and released this year. Partner's income may rise. Avoid recklessness; even Jupiter can't fully soften this house's edges. Longevity-related practices like yoga, pranayama and dietary discipline yield disproportionate benefits now.",
        9: "Jupiter in Bhav 9 during this period: arguably the most powerful placement. Dharma, fortune, mentors and long journeys flourish. Pilgrimage, foreign travel for higher purpose, advanced studies and publishing all succeed. A guru's grace becomes tangible. Father's well-being or relationship with him improves. Legal matters tilt in your favor. Teaching, writing books and ethical leadership bring not just success but a deep sense of meaning.",
        10: "Jupiter in Bhav 10 during this period: career growth with reputation and respect. Promotions, awards and opportunities to lead with integrity arise. Roles in education, law, finance, consulting, religion or government flourish. Authorities recognize your judgment. Workload is manageable and meaningful rather than draining. A leadership role you accept now can become the defining chapter of your professional life — choose deliberately.",
        11: "Jupiter in Bhav 11 during this period: outstanding for gains, fulfilled wishes and powerful friendships. Income rises substantially, especially through advisory, teaching or finance-related work. Elder siblings prosper. A long-held wish materializes, often unexpectedly. Influential, ethical people enter your network. Group leadership and association memberships bring honor. Be discerning — even abundance asks you to choose where to direct it rather than spread thin.",
        12: "Jupiter in Bhav 12 during this period: spiritual depth, foreign opportunities and meaningful expenses. You may travel abroad for study, work or pilgrimage, or invest significantly in learning, charity or a parent's care. Sleep and dreams become rich and restorative. Donations made now return as unseen protection later. Solitary practice deepens; a retreat or extended quiet period can shift your inner landscape more than any external achievement.",
    },
    "Venus": {
        1: "Venus in Bhav 1 during this period: charm, beauty and magnetism rise. Appearance improves, social invitations multiply, and romantic prospects flourish. Artistic, fashion or design-related work shines. Comfort can tip into indulgence — watch weight, late nights and overspending on appearance. A new wardrobe, grooming routine or even a small cosmetic refresh feels natural now. People genuinely enjoy your company; use it for connection, not just attention.",
        2: "Venus in Bhav 2 during this period: wealth, family harmony and pleasures of the senses grow. Income rises through luxury goods, art, beauty, food, or finance-related fields. Family gatherings are warm, and a marriage or engagement in the family is likely. Speech becomes sweet and persuasive. Spending on jewelry, dining and home decor will tempt you — set a clear budget so the year's income translates into lasting savings.",
        3: "Venus in Bhav 3 during this period: pleasant short trips, creative writing and relationships with siblings improve. Marketing, design, content and artistic communication flourish. A sister or female peer becomes a meaningful ally. Romance has a playful, conversational quality. Self-promotion comes naturally. Avoid laziness disguised as easy charm; the year rewards consistent, light effort more than occasional bursts of brilliance — keep the small commitments you make.",
        4: "Venus in Bhav 4 during this period: home becomes more beautiful and harmonious. Vehicle purchase, interior upgrade or property acquisition is highly favored. Mother's well-being improves, and family relationships sweeten. Hosting, gardening and decorating bring real joy. A long-cherished dream of a comfortable, aesthetic home space can materialize. Real estate dealings, especially properties associated with luxury, leisure or culture, are particularly auspicious.",
        5: "Venus in Bhav 5 during this period: romance, children and creativity bloom. New love, deepening of existing relationships, or conception is highly likely. Children bring joy through artistic or romantic milestones. Higher learning in arts, design or culture flourishes. Speculative gains tied to entertainment or luxury are possible with restraint. Devotional practice through music, dance or chanting feels especially natural and effective this year.",
        6: "Venus in Bhav 6 during this period: a gentler year for handling enemies, debts and health. Conflicts soften through diplomacy. Loans can be cleared steadily, and workplace rivals turn into reluctant allies. Watch reproductive, urinary or kidney health; check-ups are wise. A pet may bring great joy or need care. Service through art, beauty or hospitality work flourishes. Indulgence in food and comfort needs gentle daily moderation.",
        7: "Venus in Bhav 7 during this period: an outstanding year for marriage and partnership. Singles often meet a significant partner; existing relationships rekindle warmth and intimacy. Business partnerships in luxury, art, fashion, beauty, hospitality or finance flourish. Public dealings go smoothly. Spouse may achieve something noteworthy. Travel together is rewarding. Avoid letting comfort breed complacency; small gestures and active appreciation keep the bond alive.",
        8: "Venus in Bhav 8 during this period: intense, transformative experiences in love, money and intimacy. Inheritance or partner's income may rise, often unexpectedly. Sexuality and emotional depth become more important than surface charm. Research into healing, occult or psychological work attracts you. Watch reproductive health and avoid risky financial entanglements. A relationship taken to deeper, more honest ground this year can become genuinely soul-level rather than just pleasant.",
        9: "Venus in Bhav 9 during this period: love, luck and long journeys to beautiful places. Foreign travel, often with partner or for cultural reasons, is highly favored. Higher studies in arts, hospitality or culture flourish. Mentors are often refined, artistic women. Father's well-being improves. Legal matters resolve diplomatically. Faith deepens through beauty — temple architecture, music, sacred art — rather than dry doctrine alone.",
        10: "Venus in Bhav 10 during this period: career growth in luxury, art, fashion, beauty, hospitality, entertainment, finance or design. Reputation grows for being elegant and effective rather than aggressive. Promotions and awards are likely. Female mentors or clients support your rise. Workplace becomes more aesthetic and pleasant. Public-facing roles flourish. Reputation is a real asset this year — protect it by under-promising and consistently over-delivering.",
        11: "Venus in Bhav 11 during this period: outstanding gains and fulfillment of cherished wishes. Income rises substantially through luxury, art, finance, fashion or social ventures. Influential, often female, friends actively support your goals. A long-held romantic or creative wish materializes. Group activities and high-end social circles open up. Be selective with who you let in; not every sparkling invitation serves your deeper goals for the year.",
        12: "Venus in Bhav 12 during this period: pleasures, foreign comforts and bedroom intimacy come forward. Foreign travel for leisure, romance or art is likely. Spending on luxury, comfort, beauty or a partner can spike. Privacy in relationships becomes important; secret romances are possible but risky. Sleep and dreams become richer. Charity through art or to women in need brings unseen blessings; meditation and gentle spiritual practice deepen.",
    },
    "Saturn": {
        1: "Saturn in Bhav 1 during this period: a sober, disciplined and weighty year. Responsibilities increase, you feel older than your years, and frivolous company falls away. Health needs steady routine — bones, joints, skin and chronic issues respond best to consistency. Professional reputation grows through reliability rather than charisma. A good year to commit to hard practice, rebuild a habit, or take on a serious responsibility you have been postponing.",
        2: "Saturn in Bhav 2 during this period: finances and family demand discipline. Income may grow slowly through hard work, while expenses test your planning. Speech becomes more measured — sometimes too restrained. Family conversations may carry old grievances; address them with patience. Watch teeth, eyes and digestion. A serious commitment to saving, budgeting or eliminating wasteful spending this year creates a foundation for the next several.",
        3: "Saturn in Bhav 3 during this period: an unexpectedly strong placement for Saturn. Sustained effort in writing, communication or skill-building pays off. Short journeys are tiring but productive. Relationships with siblings deepen through responsibility rather than fun. Courage shows up as endurance rather than impulse. Self-promotion through quiet credibility works far better than flash. Hands, shoulders and posture deserve regular care this year.",
        4: "Saturn in Bhav 4 during this period: home, mother and emotional comfort feel heavy. Family responsibilities increase and you may take on caregiving for a parent. Property matters drag on but eventually resolve. Mother's health needs attention. Watch for melancholy at home; a steady, simple routine helps. A move or renovation may be necessary rather than chosen. Long-term, the discipline this year demands creates real domestic stability.",
        5: "Saturn in Bhav 5 during this period: children, romance and creativity require patience. Children may face challenges that need your sustained support. Conception can be delayed; medical guidance helps. Higher studies progress slowly but solidly. Romance feels serious or strained. Speculation should be avoided. Disciplined creative practice — daily writing, daily art, daily study — produces work this year that you will be proud of for decades.",
        6: "Saturn in Bhav 6 during this period: an excellent placement. You will steadily defeat enemies, clear long-standing debts and recover from chronic ailments. Workload is heavy but rewarding, and discipline at the workplace earns respect. Lawsuits favor the patient side. Service-oriented roles flourish. Joints, knees and chronic conditions need ongoing care. Loans can be cleared faster than expected if you stay disciplined and avoid taking on new ones.",
        7: "Saturn in Bhav 7 during this period: partnerships demand maturity. Marriage is possible but to someone older, more serious or from a different background. Existing relationships are tested by responsibility rather than passion. Business partnerships work if grounded in clear contracts. Public dealings require patience. Spouse may carry a heavy load this year; share it. Long-distance or delayed connections can deepen meaningfully if you show up consistently.",
        8: "Saturn in Bhav 8 during this period: a slow, deep, transformative year. Inheritance, insurance or joint finances move slowly through bureaucracy but eventually resolve. Chronic conditions need patience. Research, occult studies and longevity-related practices yield deep results. Avoid risky travel and extreme sports. A long-buried fear or pattern can finally be processed with the help of a steady practice or a skilled practitioner.",
        9: "Saturn in Bhav 9 during this period: faith, fortune and father are tested through discipline. Long journeys may be tiring but meaningful — pilgrimage, work travel or relocation are likely. Higher studies progress steadily. Father may face health concerns. Legal matters drag on but tilt in your favor with patience. Teaching, ethical leadership and disciplined spiritual practice bring deeper rewards than easier years would have offered.",
        10: "Saturn in Bhav 10 during this period: a powerful career placement. Promotions, expanded responsibility and recognition for sustained effort are very likely. Roles in government, law, engineering, mining, real estate and traditional industries flourish. Workload is heavy and hours long; family time needs guarding. Reputation grows through reliability, not flash. A serious leadership role accepted now can define your professional identity for the next decade.",
        11: "Saturn in Bhav 11 during this period: steady, substantial gains through hard work and patient networking. Income rises through long-term commitments rather than quick wins. Elder siblings may need support or bring news of significant developments. Older, established friends become especially valuable. A long-held wish requiring patience finally fulfills. Group leadership in serious associations or causes is likely; be selective about commitments to avoid burnout.",
        12: "Saturn in Bhav 12 during this period: expenses, foreign matters and inner discipline rise. Spending on litigation, medical care or a parent can be heavy. Foreign relocation or extended travel for work is possible. Sleep needs attention; reduce stimulation in evenings. Solitary practice, meditation, retreat and serious spiritual study yield deep results. A quiet year of inner work this year sets up the visible breakthroughs of the years ahead.",
    },
    "Rahu": {
        1: "Rahu in Bhav 1 during this period: identity, ambition and image undergo a strange but powerful shift. You may chase unconventional goals, attract attention from unexpected quarters and feel pulled toward foreign or non-traditional paths. Health can feel inexplicable; favor grounding routines. Confidence is high but illusions are also strong. A good year to break out of an old self-image, provided you don't lose sight of what is genuinely yours.",
        2: "Rahu in Bhav 2 during this period: finances, family and speech swing dramatically. Sudden gains through unconventional means, foreign sources or technology are possible, alongside equally sudden expenses. Family dynamics shift, sometimes through a foreign or unusual element. Watch speech — half-truths catch up quickly. Investments in tech, crypto or speculative instruments can pay off but stay disciplined; what comes fast can also leave fast.",
        3: "Rahu in Bhav 3 during this period: usually a strong placement for Rahu. Bold initiatives, foreign communication, technology, social media and unconventional ventures flourish. Courage is high and you will take risks others wouldn't. A sibling may be involved in something unusual or far away. Self-promotion through digital and viral channels works well. Avoid burning bridges in the rush; some collaborators are worth keeping for later.",
        4: "Rahu in Bhav 4 during this period: home life and inner peace get unsettled. Possible relocation abroad, unusual property dealings or family secrets surfacing. Mother's health may be a concern. Vehicle changes, often impulsive, are likely. Watch dissatisfaction at home that is really restlessness inside. A foreign or unconventional approach to housing — co-living, remote work setup, rental abroad — can work surprisingly well this year.",
        5: "Rahu in Bhav 5 during this period: speculation, romance and children become unpredictable. Sudden gains through markets, crypto or risky ventures are possible but stay measured. Romance may involve someone foreign, unconventional or much younger or older than expected. Conception can be delayed or come unexpectedly. Children may take unusual paths. Devotional practice with mantra, especially for Rahu, helps stabilize the year's intensity.",
        6: "Rahu in Bhav 6 during this period: another strong placement. You will defeat enemies through unconventional means and clear debts in surprising ways. Workplace politics tilt in your favor if you stay alert. Watch for skin issues, mysterious ailments and anxiety. Service-oriented roles in foreign companies, tech or unconventional fields flourish. Lawsuits can be won through smart maneuvering rather than direct confrontation. Avoid manipulative tactics — they backfire.",
        7: "Rahu in Bhav 7 during this period: partnerships become unconventional and unpredictable. Marriage may be inter-cultural, long-distance or to someone unusual. Existing relationships face sudden shifts. Business partnerships with foreigners or in tech can succeed but require clear contracts. Public dealings demand caution against deception. Spouse's behavior may surprise you. Read every agreement twice; this is not the year for handshake deals or casual trust.",
        8: "Rahu in Bhav 8 during this period: a sensitive placement. Sudden financial events, inheritance disputes or unexpected losses are possible. Research, occult studies and investigation reach unusual depths. Watch for accidents, surgeries and risky travel. Joint finances need careful documentation. A long-buried truth — yours or others' — may surface. Insurance and medical check-ups are wise. Spiritual practice, especially mantra, provides genuine protection through the year.",
        9: "Rahu in Bhav 9 during this period: foreign travel, unconventional teachers and unusual philosophies attract you. Higher studies abroad, distance learning or non-traditional credentials work well. Father may face unexpected developments. Legal matters carry uncertainty; rely on documentation, not goodwill. Avoid getting drawn into cult-like groups or charismatic but shallow gurus. A genuine teacher, often from a foreign tradition, can offer something authentic this year.",
        10: "Rahu in Bhav 10 during this period: a powerful but volatile career placement. Sudden rise in status, unconventional career moves and visibility through foreign or technology-driven channels are likely. Promotions can come surprisingly fast. Watch for politics, scandals and overreach. Reputation is fragile — protect it actively. Roles in technology, foreign companies, media, aviation or unconventional fields flourish. Don't believe your own hype before the results land.",
        11: "Rahu in Bhav 11 during this period: typically excellent. Sudden gains, unexpected income streams and influential foreign or unconventional friends are very likely. Elder siblings may achieve something noteworthy. A long-held ambitious wish materializes through unusual channels. Group activities in tech, foreign or alternative spaces open up. Be discerning with new connections — not every charismatic newcomer to your circle has aligned interests with yours.",
        12: "Rahu in Bhav 12 during this period: foreign matters, hidden expenses and unusual inner experiences rise. Foreign travel, relocation or work for overseas clients is highly likely. Spending on travel, unusual interests or hidden matters can spike. Sleep becomes strange; vivid dreams need attention. Watch for hidden enemies and scams. Solitary spiritual practice, especially mantra and meditation, deepens significantly. Charity made discreetly returns multifold over time.",
    },
    "Ketu": {
        1: "Ketu in Bhav 1 during this period: identity feels detached, even uncertain. You may withdraw from social roles, question who you are, and feel pulled toward solitude or spirituality. Health can feel mysterious; favor gentle, grounding routines. Old ambitions lose their grip. A good year for inner work, retreat and dropping what no longer fits, even if external life looks momentarily quieter than usual to outsiders.",
        2: "Ketu in Bhav 2 during this period: finances and family feel less central, sometimes uncertain. Income may dip in some streams while opening unexpectedly in others. Family ties feel either deeper or more distant — rarely neutral. Speech becomes either profound or absent. Watch teeth, eyes and digestion. A simpler relationship with money and possessions this year, even if forced, often turns out to be a real blessing.",
        3: "Ketu in Bhav 3 during this period: courage takes a quieter, more spiritual form. You may take initiatives that look small but shift something deep. A sibling becomes more spiritual or distant. Short journeys may include pilgrimage. Communication becomes selective — fewer words, more meaning. Hands and shoulders need care. A skill or practice picked up almost accidentally now can become surprisingly central to your life later.",
        4: "Ketu in Bhav 4 during this period: home and emotional comfort feel less anchoring. You may detach from a property, vehicle or living situation. Mother's well-being may need attention. A spiritual atmosphere develops at home — meditation corner, simpler decor, fewer possessions. Watch sense of inner emptiness; it is asking for spiritual depth, not more stuff. Long-pending domestic clutter is best released this year, literally and emotionally.",
        5: "Ketu in Bhav 5 during this period: children, romance and creativity take a spiritual turn. Conception can be delayed; medical and prayerful approaches both help. Existing children may become more independent or distant. Romance feels less interesting than inner work. Speculation should be avoided — Ketu doesn't pay out reliably. Mantra, devotional practice and study of sacred texts feel unusually rewarding and natural this year.",
        6: "Ketu in Bhav 6 during this period: usually a strong placement. Enemies lose interest, debts dissolve unexpectedly and chronic conditions can heal in mysterious ways. Workplace conflicts fade rather than escalate. Watch for unusual ailments that mainstream medicine struggles with; alternative healing often works better here. Service to those in need, especially anonymously, brings real grace into your life. Lawsuits tend to settle out of court.",
        7: "Ketu in Bhav 7 during this period: partnerships feel strangely detached. Existing marriage may face emotional distance — patience and conscious presence help. Singles may meet someone briefly significant but transient. Business partnerships dissolve or transform. Public dealings feel less interesting. Spouse may turn spiritual or distant. A solo journey, retreat or quiet period in a partnership often deepens it more than any forced togetherness would.",
        8: "Ketu in Bhav 8 during this period: deep transformation, occult insight and detachment from material concerns. Inheritance or joint finances may resolve in unexpected ways. Research, healing and spiritual practice reach unusual depths. Watch for accidents and risky travel. A long-buried fear or trauma can finally be released, often through an unexpected catalyst. Longevity practices like yoga, pranayama and dietary discipline yield real results this year.",
        9: "Ketu in Bhav 9 during this period: faith deepens through experience rather than doctrine. Pilgrimage, meditation retreats and unconventional spiritual paths attract you. Higher studies in philosophy, theology or healing arts flourish. Father may turn spiritual or face health concerns. Legal matters resolve in unexpected ways. A genuine inner teacher — sometimes a book, sometimes a person you barely know — appears at exactly the right moment.",
        10: "Ketu in Bhav 10 during this period: career feels less compelling, even if outwardly successful. You may walk away from a role that no longer fits, or feel pulled toward purpose-driven, spiritual or healing work. Recognition comes in unusual ways. Watch for sudden career shifts that look risky but feel inwardly right. Reputation grows for depth and integrity rather than ambition; this is often quietly more valuable.",
        11: "Ketu in Bhav 11 during this period: gains feel less central, social circle thins and quality matters more than quantity. Income may shift toward purpose-driven streams. Elder siblings may become more spiritual or distant. A long-held material wish either fulfills in a transformed way or quietly loses its hold on you. Genuine, soul-level friendships deepen while superficial ones drift away with surprisingly little drama.",
        12: "Ketu in Bhav 12 during this period: arguably Ketu's best placement. Spiritual depth, foreign retreats, meditation and inner liberation reach new levels. Foreign travel often takes a spiritual or service-oriented form. Expenses on charity, retreat or healing rise but feel meaningful. Sleep becomes deeply restorative; dreams carry real insight. A quiet year of inner work this year often produces the spiritual breakthroughs of a lifetime.",
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

# Ghata Chakra (Ghatak) — classical Vedic table of inauspicious points to avoid
# for important undertakings, indexed by Lagna sign. Each entry exposes 10
# fields matching the panel that Astrosage and other Jyotish software display:
#   bad_day, bad_karana, bad_lagna, bad_masa, bad_nakshatra, bad_prahara,
#   bad_rashi, bad_tithi, bad_yoga, bad_planets
# Capricorn values are anchored to the Nandish Dave Astrosage reference PDF.
# Lagna and Rashi are stored in Sanskrit (Vrishchika, Vrish, etc.) so the
# render layer can show them verbatim without an English→Sanskrit map.
GHATAK = {
    "Aries":       {"bad_day": "Saturday",  "bad_karana": "Vishti",  "bad_lagna": "Kumbha",       "bad_masa": "Sravana",     "bad_nakshatra": "Swati",          "bad_prahara": "1", "bad_rashi": "Kumbha",  "bad_tithi": "2, 7, 12", "bad_yoga": "Siddha",     "bad_planets": "Saturn"},
    "Taurus":      {"bad_day": "Sunday",    "bad_karana": "Kaulava", "bad_lagna": "Meena",        "bad_masa": "Bhadrapada",  "bad_nakshatra": "Vishakha",       "bad_prahara": "2", "bad_rashi": "Meena",   "bad_tithi": "3, 8, 13", "bad_yoga": "Vyatipata",  "bad_planets": "Sun"},
    "Gemini":      {"bad_day": "Monday",    "bad_karana": "Bava",    "bad_lagna": "Mesha",        "bad_masa": "Ashwina",     "bad_nakshatra": "Anuradha",       "bad_prahara": "3", "bad_rashi": "Mesha",   "bad_tithi": "4, 9, 14", "bad_yoga": "Brahma",     "bad_planets": "Moon"},
    "Cancer":      {"bad_day": "Tuesday",   "bad_karana": "Balava",  "bad_lagna": "Vrish",        "bad_masa": "Karttika",    "bad_nakshatra": "Jyeshtha",       "bad_prahara": "4", "bad_rashi": "Vrish",   "bad_tithi": "5, 10, 15","bad_yoga": "Atiganda",   "bad_planets": "Mars"},
    "Leo":         {"bad_day": "Wednesday", "bad_karana": "Taitila", "bad_lagna": "Mithuna",      "bad_masa": "Margashira",  "bad_nakshatra": "Mula",           "bad_prahara": "1", "bad_rashi": "Mithuna", "bad_tithi": "1, 6, 11", "bad_yoga": "Sukarman",   "bad_planets": "Mercury"},
    "Virgo":       {"bad_day": "Thursday",  "bad_karana": "Garaja",  "bad_lagna": "Karka",        "bad_masa": "Pausha",      "bad_nakshatra": "Purva Ashadha",  "bad_prahara": "2", "bad_rashi": "Karka",   "bad_tithi": "2, 7, 12", "bad_yoga": "Dhriti",     "bad_planets": "Jupiter"},
    "Libra":       {"bad_day": "Friday",    "bad_karana": "Vanija",  "bad_lagna": "Simha",        "bad_masa": "Magha",       "bad_nakshatra": "Uttara Ashadha", "bad_prahara": "3", "bad_rashi": "Simha",   "bad_tithi": "3, 8, 13", "bad_yoga": "Shoola",     "bad_planets": "Venus"},
    "Scorpio":     {"bad_day": "Saturday",  "bad_karana": "Vishti",  "bad_lagna": "Kanya",        "bad_masa": "Phalguna",    "bad_nakshatra": "Shravana",       "bad_prahara": "4", "bad_rashi": "Kanya",   "bad_tithi": "4, 9, 14", "bad_yoga": "Ganda",      "bad_planets": "Saturn"},
    "Sagittarius": {"bad_day": "Sunday",    "bad_karana": "Bava",    "bad_lagna": "Tula",         "bad_masa": "Chaitra",     "bad_nakshatra": "Dhanishtha",     "bad_prahara": "1", "bad_rashi": "Tula",    "bad_tithi": "5, 10, 15","bad_yoga": "Vriddhi",    "bad_planets": "Sun"},
    "Capricorn":   {"bad_day": "Friday",    "bad_karana": "Garaja",  "bad_lagna": "Vrishchika",   "bad_masa": "Ashwin",      "bad_nakshatra": "Revati",         "bad_prahara": "1", "bad_rashi": "Vrish",   "bad_tithi": "1, 6, 11", "bad_yoga": "Brahma",     "bad_planets": "Mercury"},
    "Aquarius":    {"bad_day": "Monday",    "bad_karana": "Balava",  "bad_lagna": "Dhanu",        "bad_masa": "Karttika",    "bad_nakshatra": "Ashwini",        "bad_prahara": "2", "bad_rashi": "Dhanu",   "bad_tithi": "2, 7, 12", "bad_yoga": "Vishkambha", "bad_planets": "Moon"},
    "Pisces":      {"bad_day": "Tuesday",   "bad_karana": "Taitila", "bad_lagna": "Makara",       "bad_masa": "Margashira",  "bad_nakshatra": "Bharani",        "bad_prahara": "3", "bad_rashi": "Makara",  "bad_tithi": "3, 8, 13", "bad_yoga": "Priti",      "bad_planets": "Mars"},
}


# ── FAVOURABLE POINTS (by Lagna sign) ────────────────────────────────────────

# Favourable Points — classical "lucky" reference table indexed by Lagna,
# matching the panel that Astrosage and other Jyotish software display.
# Each entry exposes 10 fields:
#   lucky_numbers, good_numbers, evil_numbers, good_years, lucky_days,
#   good_planets, friendly_signs, good_lagna, lucky_metal, lucky_stone
# Capricorn values are anchored to the Astrosage Nandish Dave reference PDF.
# Other lagnas follow these derivable patterns (verify against Astrosage if
# you have a reference chart for them):
#   good_years    : arithmetic sequence (lagna_num + 3) + 9k for k=0..4
#   friendly_signs: signs at houses 4, 8, 12 from the Lagna
#   good_lagna    : signs at houses 12, 3, 5, 1 from the Lagna (in that order)
# Varna/Yoni/Gana/Nadi were previously stored here too — they have moved to
# the Avkahada Chakra section (calc_avkahada in kundli_calculator.py) where
# they are now correctly computed from the Moon's nakshatra and rashi.
FAVOURABLE = {
    "Aries":       {"lucky_numbers": "9", "good_numbers": "1, 3, 5, 9", "evil_numbers": "2, 6, 8", "good_years": "4, 13, 22, 31, 40, 49", "lucky_days": "Tuesday, Saturday, Friday", "good_planets": "Mars, Jupiter, Sun",       "friendly_signs": "Can, Sco, Pis", "good_lagna": "Pis, Gem, Leo, Ari", "lucky_metal": "Copper", "lucky_stone": "Red Coral"},
    "Taurus":      {"lucky_numbers": "6", "good_numbers": "2, 4, 6, 8", "evil_numbers": "1, 5, 7", "good_years": "5, 14, 23, 32, 41, 50", "lucky_days": "Friday, Wednesday, Saturday","good_planets": "Venus, Mercury, Saturn",  "friendly_signs": "Leo, Sag, Ari", "good_lagna": "Ari, Can, Vir, Tau", "lucky_metal": "Silver", "lucky_stone": "Diamond"},
    "Gemini":      {"lucky_numbers": "5", "good_numbers": "3, 5, 7, 9", "evil_numbers": "2, 4, 6", "good_years": "6, 15, 24, 33, 42, 51", "lucky_days": "Wednesday, Friday, Thursday","good_planets": "Mercury, Venus, Saturn",  "friendly_signs": "Vir, Cap, Tau", "good_lagna": "Tau, Leo, Lib, Gem", "lucky_metal": "Gold",   "lucky_stone": "Emerald"},
    "Cancer":      {"lucky_numbers": "2", "good_numbers": "1, 2, 4, 7", "evil_numbers": "3, 5, 8", "good_years": "7, 16, 25, 34, 43, 52", "lucky_days": "Monday, Thursday, Sunday",   "good_planets": "Moon, Mars, Jupiter",     "friendly_signs": "Lib, Aqu, Gem", "good_lagna": "Gem, Vir, Sco, Can", "lucky_metal": "Silver", "lucky_stone": "Pearl"},
    "Leo":         {"lucky_numbers": "1", "good_numbers": "1, 3, 5, 9", "evil_numbers": "2, 6, 8", "good_years": "8, 17, 26, 35, 44, 53", "lucky_days": "Sunday, Tuesday, Wednesday", "good_planets": "Sun, Mars, Jupiter",      "friendly_signs": "Sco, Pis, Can", "good_lagna": "Can, Lib, Sag, Leo", "lucky_metal": "Gold",   "lucky_stone": "Ruby"},
    "Virgo":       {"lucky_numbers": "5", "good_numbers": "2, 4, 5, 8", "evil_numbers": "1, 3, 9", "good_years": "9, 18, 27, 36, 45, 54", "lucky_days": "Wednesday, Friday, Monday",  "good_planets": "Mercury, Venus, Saturn",  "friendly_signs": "Sag, Ari, Leo", "good_lagna": "Leo, Sco, Cap, Vir", "lucky_metal": "Bronze", "lucky_stone": "Emerald"},
    "Libra":       {"lucky_numbers": "6", "good_numbers": "2, 6, 7, 8", "evil_numbers": "1, 5, 9", "good_years": "10, 19, 28, 37, 46, 55","lucky_days": "Friday, Wednesday, Saturday","good_planets": "Venus, Mercury, Saturn",  "friendly_signs": "Cap, Tau, Vir", "good_lagna": "Vir, Sag, Aqu, Lib", "lucky_metal": "Silver", "lucky_stone": "Diamond"},
    "Scorpio":     {"lucky_numbers": "9", "good_numbers": "1, 3, 7, 9", "evil_numbers": "2, 4, 6", "good_years": "11, 20, 29, 38, 47, 56","lucky_days": "Tuesday, Thursday, Sunday",  "good_planets": "Mars, Jupiter, Moon",     "friendly_signs": "Aqu, Gem, Lib", "good_lagna": "Lib, Cap, Pis, Sco", "lucky_metal": "Copper", "lucky_stone": "Red Coral"},
    "Sagittarius": {"lucky_numbers": "3", "good_numbers": "1, 3, 5, 8", "evil_numbers": "2, 6, 7", "good_years": "12, 21, 30, 39, 48, 57","lucky_days": "Thursday, Tuesday, Sunday",  "good_planets": "Jupiter, Sun, Mars",      "friendly_signs": "Pis, Can, Sco", "good_lagna": "Sco, Aqu, Ari, Sag", "lucky_metal": "Gold",   "lucky_stone": "Yellow Sapphire"},
    "Capricorn":   {"lucky_numbers": "4", "good_numbers": "2, 4, 5, 8", "evil_numbers": "1, 7, 9", "good_years": "13, 22, 31, 40, 49",    "lucky_days": "Thursday, Tuesday",          "good_planets": "Jupiter, Mars, Moon",     "friendly_signs": "Ari, Leo, Sag", "good_lagna": "Sag, Pis, Tau, Cap", "lucky_metal": "Gold",   "lucky_stone": "Red Coral"},
    "Aquarius":    {"lucky_numbers": "8", "good_numbers": "2, 4, 6, 8", "evil_numbers": "1, 3, 9", "good_years": "14, 23, 32, 41, 50",    "lucky_days": "Saturday, Friday, Wednesday","good_planets": "Saturn, Venus, Mercury",  "friendly_signs": "Tau, Vir, Cap", "good_lagna": "Cap, Ari, Gem, Aqu", "lucky_metal": "Iron",   "lucky_stone": "Blue Sapphire"},
    "Pisces":      {"lucky_numbers": "3", "good_numbers": "1, 3, 7, 9", "evil_numbers": "2, 5, 8", "good_years": "15, 24, 33, 42, 51",    "lucky_days": "Thursday, Tuesday, Sunday",  "good_planets": "Jupiter, Moon, Mars",     "friendly_signs": "Gem, Lib, Aqu", "good_lagna": "Aqu, Tau, Can, Pis", "lucky_metal": "Gold",   "lucky_stone": "Yellow Sapphire"},
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
