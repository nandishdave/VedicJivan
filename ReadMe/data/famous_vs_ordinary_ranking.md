# Famous vs Ordinary - Full Ranking (Dhana + Prosperity split)

All 128 charts (32 famous star + 96 ordinary), scored by a cross-validated 8-feature
model. The wealth axis is now TWO separate graded features from
api/app/services/kundli_calculator/dhana_yoga.py:
  - Dhana yoga       = lords of 1/2/11 (Lagnesh/Dhanesh/Labhesh) - true wealth
  - Prosperity yoga  = links touching the 5th/9th lord - fortune, kept separate

Honest note: neither yoga separates fame (famous 27.5 vs ordinary 26.5, famous
median rank 74/128) - they are wealth/fortune readouts, not fame predictors.
Regenerate with scripts/score_ranking.py.
```text
RANK  SCORE  WHO   NAME
  1    78.0        Bhargav M Raval
  2    64.7   â˜…    Oprah
  3    60.0   â˜…    Tesla
  4    59.5        Harsh Raval
  5    57.0        Nayan Shah
  6    56.6   â˜…    Churchill
  7    56.5   â˜…    GW Bush
  8    52.1        Nandish Dave
  9    52.0        Sneha Shah
 10    51.4        Arohi N Parikh
 11    50.5   â˜…    Queen Elizabeth II
 12    49.6        Dhaval J Shah
 13    48.5        Snehal J Chauhan
 14    48.4        Ruchi Raval
 15    47.2        Rupal Raghuvanshi
 16    46.5        Shobha Dave
 17    46.4        Esha Shah
 18    46.0        Pooja Priya
 19    44.4        Bhupesh Kumar
 20    44.3        Varta Shah
 21    44.1        Hardik Suchak
 22    43.0   â˜…    Reagan
 23    41.9        Lav Butala
 24    40.2        Rahul R Joshi
 25    39.8        Yatin Punjabi
 26    39.2        Harsh Trivedi
 27    38.8   â˜…    Taylor Swift
 28    38.7        Priyal Parikh
 29    38.7   â˜…    Trump
 30    38.5        Pragati Nayak
 31    38.4        Binal Shah
 32    37.8        Pooja Dhaval Shah
 33    37.0        Partha Saha
 34    36.8        Sahil Jani
 35    36.7        Yaduvendra Chaurasia
 36    35.5        Jinal Shah
 37    35.4   â˜…    Hendrix
 38    35.1        Manish Singh
 39    34.2   â˜…    Elvis
 40    33.4   â˜…    John Lennon
 41    33.2        Harsh Shah
 42    33.2   â˜…    Madonna
 43    32.2        Vatsal Raicha
 44    31.4        Bhusan Savani
 45    31.0        Helena Dave
 46    30.7        Bishal Bose
 47    30.6        Aniket Shah
 48    30.6        Krutik Shah
 49    30.0        Jigisha Dhruv Jani
 50    29.7        Vixita Nayak
 51    28.9        Yatin Mirani
 52    28.8        Prasad
 53    27.9        Jigar Mehta
 54    26.0        Suraj Mehta
 55    25.4        Heena T Dave
 56    25.4        Mayank Kumar
 57    24.9        Karan Patel
 58    24.8   â˜…    Obama
 59    24.7        Shikha Kumari
 60    24.3        Bhargav
 61    23.8        Moxta
 62    22.8   â˜…    Muhammad Ali
 63    22.6        Sonali Pagar
 64    22.5        Nency A Shah
 65    22.3        Rama G Dave
 66    22.1        Melvin Methew
 67    21.8        Bhavika Bhayani
 68    21.6        Monika Pattanayak
 69    21.5        Paras Gajjar
 70    21.0        Harshal Joshi
 71    20.7   â˜…    Marilyn Monroe
 72    20.6        Grandin Major Vincent
 73    20.0   â˜…    Freud
 74    19.8   â˜…    Jim Morrison
 75    19.5        Nishit Parikh
 76    19.5   â˜…    Diana
 77    19.4        Darshan
 78    19.4        Varun Chaturvedi
 79    18.5        Ravi Shah
 80    18.3   â˜…    Prince Harry
 81    18.2   â˜…    Bill Clinton
 82    17.9   â˜…    Charles III
 83    17.5   â˜…    Carl Jung
 84    16.8        Devang Shah
 85    16.7   â˜…    Darwin
 86    16.3        Janki Dave
 87    16.2        Tushar G Dave
 88    16.1   â˜…    Einstein
 89    16.1        Praveen
 90    15.9   â˜…    Prince William
 91    15.9        Viraj Shah
 92    15.7        Manthan
 93    15.7        Neha Khetrapal
 94    15.2        Kaumil Bhavsar
 95    15.2   â˜…    JFK
 96    14.8        Aastha Sachin Raval
 97    14.8        Priyesh Dave
 98    14.6        Jainith Nayak
 99    14.5        Venkat
100    14.3        Shreya
101    14.3        Rohan
102    14.0        Sanjay M Raval
103    13.8   â˜…    Michael Jackson
104    13.8        Rumna Saha
105    13.6        Anmol Mehta
106    13.6   â˜…    Kurt Cobain
107    13.2   â˜…    Angelina Jolie
108    13.1        Riddhish Shah
109    13.0        Viral Gajjar
110    12.7        Dhruv Jani
111    11.4        Shivani Kandarp Dave
112    11.2   â˜…    Hitler
113    11.1   â˜…    Hillary Clinton
114    10.7        Kandarp Dave
115    10.2        Pooja Dave
116     9.7        Akash Zaveri
117     9.6        Shikha Dave
118     9.1        Papu ben
119     8.6        Dipti Dave
120     8.4   â˜…    McCartney
121     8.4        Kushal Shah
122     8.2        Dhara Ravi Shah
123     7.5        Vishal Khetrapal
124     6.9        Dharini Anmol Mehta
125     6.7        Riya Viraj Shah
126     6.7        Misika Butala
127     5.7        Harshad Patel
128     5.1        Pratiksha

â˜… = famous (32), blank = ordinary (96)
Famous mean score=27.5  |  Ordinary mean=26.5
Top 20: 5 famous / 15 ordinary  |  famous median rank=74 of 128
```
