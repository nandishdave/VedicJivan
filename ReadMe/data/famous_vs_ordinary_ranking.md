# Famous vs Ordinary - Full Ranking (composite strong-factor COUNT)

All 128 charts (32 famous star + 96 ordinary), scored by how many of the 8
strong-chart factors each chart STACKS (orient each factor famous-positive,
standardise, count the elevated ones). STRONG = count of 8 factors above par;
COMPOSITE = continuous z-sum (tie-break within a count).

Factors: dasha-timing, Dhana(1/2/11), Prosperity(5/9), Raja(kendra/trikona+
combustion), functional-benefics, 1st-house SAV, 10th-house SAV, D60.

This co-occurrence count is the BEST formulation of the (still weak) signal:
famous stack more (mean 4.00 vs 3.44 of 8), famous median rank 41/128, top-20 =
8 famous, CV-AUC 0.547 (vs the weighted linear model's 0.485; 0.5 = chance). It
is co-occurrence, not synergy (pairwise interactions overfit to 0.428). Still a
weak tilt (~0.55), not a fame predictor. Regenerate with scripts/score_ranking.py.
```text
RANK  STRONG  COMPOSITE  WHO   NAME
  1    7/8     +4.83         Lav Butala
  2    6/8     +7.70    â˜…    Tesla
  3    6/8     +6.04    â˜…    Oprah
  4    6/8     +4.59    â˜…    Reagan
  5    6/8     +4.22         Hardik Suchak
  6    6/8     +4.02    â˜…    Madonna
  7    6/8     +3.94         Harsh Trivedi
  8    6/8     +1.49         Yaduvendra Chaurasia
  9    5/8     +4.87    â˜…    GW Bush
 10    5/8     +4.57    â˜…    Hitler
 11    5/8     +4.47         Shobha Dave
 12    5/8     +4.38         Rahul R Joshi
 13    5/8     +4.36    â˜…    Freud
 14    5/8     +3.44    â˜…    Churchill
 15    5/8     +2.87         Sahil Jani
 16    5/8     +2.82         Binal Shah
 17    5/8     +2.67         Darshan
 18    5/8     +2.65         Bhargav M Raval
 19    5/8     +2.64         Bishal Bose
 20    5/8     +2.64         Priyal Parikh
 21    5/8     +2.47         Rama G Dave
 22    5/8     +2.45         Jigisha Dhruv Jani
 23    5/8     +2.31    â˜…    Trump
 24    5/8     +2.17    â˜…    Elvis
 25    5/8     +1.36         Jinal Shah
 26    5/8     +1.31         Viraj Shah
 27    5/8     +1.21         Priyesh Dave
 28    5/8     +0.34         Helena Dave
 29    5/8     +0.10         Prasad
 30    5/8     -0.03         Jigar Mehta
 31    5/8     -0.46    â˜…    Obama
 32    4/8     +2.35    â˜…    Muhammad Ali
 33    4/8     +2.33    â˜…    Hendrix
 34    4/8     +1.99         Heena T Dave
 35    4/8     +1.96         Vixita Nayak
 36    4/8     +1.88    â˜…    John Lennon
 37    4/8     +1.86         Partha Saha
 38    4/8     +1.77    â˜…    Carl Jung
 39    4/8     +1.51    â˜…    Diana
 40    4/8     +1.48         Aniket Shah
 41    4/8     +1.42         Nency A Shah
 42    4/8     +1.21         Bhupesh Kumar
 43    4/8     +1.20    â˜…    Jim Morrison
 44    4/8     +1.17         Ruchi Raval
 45    4/8     +1.07         Shikha Kumari
 46    4/8     +0.87         Karan Patel
 47    4/8     +0.78         Arohi N Parikh
 48    4/8     +0.46    â˜…    Kurt Cobain
 49    4/8     +0.42    â˜…    Queen Elizabeth II
 50    4/8     +0.38    â˜…    Taylor Swift
 51    4/8     +0.38         Nayan Shah
 52    4/8     +0.34         Snehal J Chauhan
 53    4/8     +0.29         Pragati Nayak
 54    4/8     +0.16    â˜…    Michael Jackson
 55    4/8     +0.12         Shivani Kandarp Dave
 56    4/8     +0.11    â˜…    Marilyn Monroe
 57    4/8     +0.07         Melvin Methew
 58    4/8     -0.05         Vishal Khetrapal
 59    4/8     -0.14         Nishit Parikh
 60    4/8     -0.31         Aastha Sachin Raval
 61    4/8     -0.46         Krutik Shah
 62    4/8     -0.65         Grandin Major Vincent
 63    4/8     -0.76         Esha Shah
 64    4/8     -0.91    â˜…    Charles III
 65    4/8     -0.99         Sanjay M Raval
 66    4/8     -1.33         Kaumil Bhavsar
 67    4/8     -2.48         Shikha Dave
 68    3/8     +2.77         Dhaval J Shah
 69    3/8     +2.45         Harsh Raval
 70    3/8     +2.07         Pooja Priya
 71    3/8     +1.26         Harshal Joshi
 72    3/8     +0.98    â˜…    Darwin
 73    3/8     +0.93         Manish Singh
 74    3/8     +0.41    â˜…    Bill Clinton
 75    3/8     +0.33         Harsh Shah
 76    3/8     +0.30    â˜…    Prince Harry
 77    3/8     -0.26         Janki Dave
 78    3/8     -0.30         Nandish Dave
 79    3/8     -0.52         Neha Khetrapal
 80    3/8     -0.61         Jainith Nayak
 81    3/8     -0.66         Bhusan Savani
 82    3/8     -0.88         Venkat
 83    3/8     -0.90         Tushar G Dave
 84    3/8     -1.34         Vatsal Raicha
 85    3/8     -1.35         Anmol Mehta
 86    3/8     -1.39         Bhavika Bhayani
 87    3/8     -1.44         Sonali Pagar
 88    3/8     -1.45         Shreya
 89    3/8     -1.61         Riddhish Shah
 90    3/8     -1.78         Rupal Raghuvanshi
 91    3/8     -2.02         Suraj Mehta
 92    3/8     -2.16         Viral Gajjar
 93    3/8     -2.50         Varun Chaturvedi
 94    3/8     -2.58         Ravi Shah
 95    3/8     -2.69         Pooja Dhaval Shah
 96    3/8     -2.76         Kandarp Dave
 97    3/8     -2.86         Moxta
 98    3/8     -3.50         Yatin Mirani
 99    2/8     -0.45         Dhruv Jani
100    2/8     -0.90         Sneha Shah
101    2/8     -1.11    â˜…    Angelina Jolie
102    2/8     -1.26         Paras Gajjar
103    2/8     -1.67         Mayank Kumar
104    2/8     -1.74         Devang Shah
105    2/8     -1.82         Monika Pattanayak
106    2/8     -2.11         Varta Shah
107    2/8     -2.25    â˜…    JFK
108    2/8     -2.31         Pooja Dave
109    2/8     -2.44         Bhargav
110    2/8     -2.49         Harshad Patel
111    2/8     -2.57    â˜…    Hillary Clinton
112    2/8     -2.97         Pratiksha
113    2/8     -3.08         Misika Butala
114    2/8     -3.23    â˜…    McCartney
115    2/8     -3.29         Manthan
116    2/8     -3.33         Praveen
117    2/8     -3.45         Rumna Saha
118    2/8     -3.62         Kushal Shah
119    2/8     -3.63         Papu ben
120    2/8     -3.80    â˜…    Prince William
121    2/8     -4.21         Akash Zaveri
122    2/8     -4.54         Dharini Anmol Mehta
123    2/8     -4.67    â˜…    Einstein
124    2/8     -5.15         Riya Viraj Shah
125    2/8     -5.83         Dipti Dave
126    1/8     -1.82         Yatin Punjabi
127    1/8     -3.85         Rohan
128    1/8     -4.29         Dhara Ravi Shah

â˜… = famous (32), blank = ordinary (96)
Famous mean strong-count=4.00  |  Ordinary mean=3.44
Top 20: 8 famous / 12 ordinary  |  famous median rank=41 of 128
CV-AUC of the composite strong-count = 0.547  (linear 8-feature was 0.485; 0.5=chance)
```
