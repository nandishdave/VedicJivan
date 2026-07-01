# Famous vs Ordinary - Full Ranking (composite strong-factor COUNT)

All 128 charts (32 famous star + 96 ordinary), scored by how many of the 8
strong-chart factors each chart STACKS (orient famous-positive, standardise, count
the elevated ones). STRONG = count above par; COMPOSITE = continuous z-sum.

Factors: dasha-timing (FUNCTIONAL-benefic bonus, lagna-specific), Dhana(1/2/11),
Prosperity(5/9), Raja(kendra/trikona+combustion), functional-benefics, 1st-house
SAV, 10th-house SAV, D60.

Best formulation of the (still weak) signal: famous stack more (4.09 vs 3.42 of 8),
famous median rank 43/128, top-20 = 8 famous, CV-AUC 0.565 (vs the weighted linear
model's 0.498; 0.5 = chance). Co-occurrence, not synergy. Still a weak ~0.56 tilt,
not a fame predictor. Regenerate with scripts/score_ranking.py.
```text
RANK  STRONG  COMPOSITE  WHO   NAME
  1    7/8     +4.96         Lav Butala
  2    7/8     +4.73    â˜…    Madonna
  3    6/8     +7.74    â˜…    Tesla
  4    6/8     +6.01    â˜…    Oprah
  5    6/8     +4.90    â˜…    Reagan
  6    6/8     +4.07         Harsh Trivedi
  7    6/8     +3.56    â˜…    Churchill
  8    6/8     +3.39         Hardik Suchak
  9    6/8     +1.36         Yaduvendra Chaurasia
 10    6/8     +1.33         Priyesh Dave
 11    5/8     +5.01    â˜…    GW Bush
 12    5/8     +4.60    â˜…    Hitler
 13    5/8     +4.51         Shobha Dave
 14    5/8     +4.44         Rahul R Joshi
 15    5/8     +4.29    â˜…    Freud
 16    5/8     +2.99         Bhargav M Raval
 17    5/8     +2.91         Sahil Jani
 18    5/8     +2.79         Binal Shah
 19    5/8     +2.74         Darshan
 20    5/8     +2.68         Priyal Parikh
 21    5/8     +2.67         Jigisha Dhruv Jani
 22    5/8     +2.60    â˜…    Trump
 23    5/8     +2.31         Bishal Bose
 24    5/8     +2.19    â˜…    Elvis
 25    5/8     +2.08         Rama G Dave
 26    5/8     +1.46         Jinal Shah
 27    5/8     +0.91         Viraj Shah
 28    5/8     +0.59         Helena Dave
 29    5/8     +0.07         Jigar Mehta
 30    5/8     -0.03         Prasad
 31    4/8     +2.35    â˜…    Muhammad Ali
 32    4/8     +2.18         Pooja Priya
 33    4/8     +2.18         Vixita Nayak
 34    4/8     +2.08         Heena T Dave
 35    4/8     +1.89         Nency A Shah
 36    4/8     +1.85    â˜…    John Lennon
 37    4/8     +1.79    â˜…    Carl Jung
 38    4/8     +1.69    â˜…    Hendrix
 39    4/8     +1.66         Partha Saha
 40    4/8     +1.64    â˜…    Diana
 41    4/8     +1.54         Aniket Shah
 42    4/8     +1.27    â˜…    Jim Morrison
 43    4/8     +1.26         Bhupesh Kumar
 44    4/8     +1.10    â˜…    Darwin
 45    4/8     +0.98         Shikha Kumari
 46    4/8     +0.96         Karan Patel
 47    4/8     +0.94         Arohi N Parikh
 48    4/8     +0.63    â˜…    Michael Jackson
 49    4/8     +0.53    â˜…    Prince Harry
 50    4/8     +0.52         Snehal J Chauhan
 51    4/8     +0.52    â˜…    Taylor Swift
 52    4/8     +0.31    â˜…    Kurt Cobain
 53    4/8     +0.31         Pragati Nayak
 54    4/8     +0.20         Shivani Kandarp Dave
 55    4/8     +0.19    â˜…    Marilyn Monroe
 56    4/8     +0.09         Melvin Methew
 57    4/8     -0.20         Vishal Khetrapal
 58    4/8     -0.21         Krutik Shah
 59    4/8     -0.31    â˜…    Queen Elizabeth II
 60    4/8     -0.44         Grandin Major Vincent
 61    4/8     -0.53         Aastha Sachin Raval
 62    4/8     -0.61         Esha Shah
 63    4/8     -0.67    â˜…    Charles III
 64    4/8     -0.77         Sanjay M Raval
 65    4/8     -0.83         Kaumil Bhavsar
 66    4/8     -0.88    â˜…    Obama
 67    4/8     -2.53         Shikha Dave
 68    3/8     +2.90         Dhaval J Shah
 69    3/8     +2.54         Harsh Raval
 70    3/8     +0.86         Harshal Joshi
 71    3/8     +0.58         Ruchi Raval
 72    3/8     +0.57    â˜…    Bill Clinton
 73    3/8     +0.53         Manish Singh
 74    3/8     -0.22         Harsh Shah
 75    3/8     -0.23         Nandish Dave
 76    3/8     -0.51         Nayan Shah
 77    3/8     -0.68         Bhusan Savani
 78    3/8     -0.74         Janki Dave
 79    3/8     -0.75         Tushar G Dave
 80    3/8     -0.85         Jainith Nayak
 81    3/8     -0.90         Nishit Parikh
 82    3/8     -1.05         Sonali Pagar
 83    3/8     -1.10         Anmol Mehta
 84    3/8     -1.13         Neha Khetrapal
 85    3/8     -1.16         Bhavika Bhayani
 86    3/8     -1.17         Venkat
 87    3/8     -1.38         Shreya
 88    3/8     -1.53         Vatsal Raicha
 89    3/8     -1.58         Riddhish Shah
 90    3/8     -1.88         Suraj Mehta
 91    3/8     -2.07         Viral Gajjar
 92    3/8     -2.28         Rupal Raghuvanshi
 93    3/8     -2.47         Varun Chaturvedi
 94    3/8     -2.55         Moxta
 95    3/8     -2.55         Ravi Shah
 96    3/8     -2.76         Kandarp Dave
 97    3/8     -3.44         Yatin Mirani
 98    2/8     +0.19         Dhruv Jani
 99    2/8     -1.10         Paras Gajjar
100    2/8     -1.13         Sneha Shah
101    2/8     -1.53         Mayank Kumar
102    2/8     -1.62         Devang Shah
103    2/8     -1.66    â˜…    Angelina Jolie
104    2/8     -1.80         Varta Shah
105    2/8     -2.11         Pooja Dave
106    2/8     -2.30         Harshad Patel
107    2/8     -2.33    â˜…    JFK
108    2/8     -2.40    â˜…    Hillary Clinton
109    2/8     -2.45         Manthan
110    2/8     -2.47         Monika Pattanayak
111    2/8     -2.76         Bhargav
112    2/8     -2.79         Pratiksha
113    2/8     -2.89         Misika Butala
114    2/8     -3.20    â˜…    McCartney
115    2/8     -3.32         Rumna Saha
116    2/8     -3.38         Pooja Dhaval Shah
117    2/8     -3.39         Kushal Shah
118    2/8     -3.49         Papu ben
119    2/8     -3.62         Praveen
120    2/8     -3.85    â˜…    Prince William
121    2/8     -4.18         Akash Zaveri
122    2/8     -4.37         Dharini Anmol Mehta
123    2/8     -4.66    â˜…    Einstein
124    2/8     -5.32         Riya Viraj Shah
125    2/8     -5.46         Dipti Dave
126    1/8     -2.28         Yatin Punjabi
127    1/8     -3.83         Rohan
128    1/8     -4.01         Dhara Ravi Shah

â˜… = famous (32), blank = ordinary (96)
Famous mean strong-count=4.09  |  Ordinary mean=3.42
Top 20: 8 famous / 12 ordinary  |  famous median rank=43 of 128
CV-AUC of the composite strong-count = 0.565  (linear 8-feature was 0.485; 0.5=chance)
```
