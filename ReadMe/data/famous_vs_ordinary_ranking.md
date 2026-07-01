# Famous vs Ordinary - Full Ranking (graded Dhana-yoga)

All 128 charts (32 famous star + 96 ordinary), scored by a cross-validated model and
ranked by "famous-likeness". The wealth feature is now the graded Dhana-yoga
(api/app/services/kundli_calculator/dhana_yoga.py) - connection x lords x dignity x
house - replacing the old crude 2-11 flag.

Honest note: with the graded Dhana-yoga the group means are essentially equal
(famous 27.1 vs ordinary 27.1) and the famous median rank is 74/128 - i.e. the
graded yoga is astrologically faithful but does NOT separate fame (Dhana yogas are
~equally common in both groups). Regenerate with scripts/score_ranking.py.
```text
RANK  SCORE  WHO   NAME
  1    75.6        Bhargav M Raval
  2    63.8   â˜…    Tesla
  3    59.2   â˜…    Queen Elizabeth II
  4    58.1        Nayan Shah
  5    58.0   â˜…    Churchill
  6    57.6   â˜…    GW Bush
  7    54.7        Bhupesh Kumar
  8    53.6        Arohi N Parikh
  9    52.9        Sneha Shah
 10    52.8        Nandish Dave
 11    52.1        Dhaval J Shah
 12    51.3        Harsh Raval
 13    51.0   â˜…    Oprah
 14    49.3        Varta Shah
 15    49.1        Rupal Raghuvanshi
 16    48.8        Snehal J Chauhan
 17    46.5        Pooja Priya
 18    45.3   â˜…    Taylor Swift
 19    44.8        Binal Shah
 20    44.7        Ruchi Raval
 21    43.2   â˜…    Hendrix
 22    43.1        Helena Dave
 23    42.6        Esha Shah
 24    42.4        Hardik Suchak
 25    41.2        Pooja Dhaval Shah
 26    41.2        Sahil Jani
 27    40.5        Yatin Mirani
 28    40.3        Shobha Dave
 29    40.2        Yatin Punjabi
 30    39.6        Priyal Parikh
 31    38.8        Pragati Nayak
 32    38.6        Partha Saha
 33    38.2        Vatsal Raicha
 34    37.6        Bhusan Savani
 35    37.3   â˜…    Reagan
 36    35.9        Harsh Trivedi
 37    34.7        Yaduvendra Chaurasia
 38    33.8        Krutik Shah
 39    33.6        Harsh Shah
 40    33.1        Manish Singh
 41    32.8        Lav Butala
 42    31.9   â˜…    Elvis
 43    31.1   â˜…    John Lennon
 44    30.8        Vixita Nayak
 45    30.7        Bhargav
 46    29.8        Moxta
 47    29.5        Heena T Dave
 48    29.4        Prasad
 49    29.0        Karan Patel
 50    28.6   â˜…    Trump
 51    28.2        Bishal Bose
 52    28.1        Jinal Shah
 53    27.2        Jigar Mehta
 54    26.5        Suraj Mehta
 55    25.5        Aniket Shah
 56    25.4        Janki Dave
 57    24.9   â˜…    Madonna
 58    23.0   â˜…    Angelina Jolie
 59    22.5        Jigisha Dhruv Jani
 60    22.3        Nency A Shah
 61    22.3        Melvin Methew
 62    22.3        Jainith Nayak
 63    22.1        Varun Chaturvedi
 64    21.9        Harshal Joshi
 65    21.7        Mayank Kumar
 66    21.6        Grandin Major Vincent
 67    21.3   â˜…    Marilyn Monroe
 68    21.2        Shikha Kumari
 69    21.1        Viraj Shah
 70    20.9        Rahul R Joshi
 71    20.9   â˜…    Obama
 72    20.5        Paras Gajjar
 73    20.2        Neha Khetrapal
 74    19.9   â˜…    Diana
 75    19.7   â˜…    JFK
 76    19.5   â˜…    Darwin
 77    19.3   â˜…    Einstein
 78    19.3        Devang Shah
 79    18.6   â˜…    Prince William
 80    18.4        Nishit Parikh
 81    18.4   â˜…    Jim Morrison
 82    17.8        Darshan
 83    17.6        Papu ben
 84    17.5        Ravi Shah
 85    17.3        Praveen
 86    16.9   â˜…    Michael Jackson
 87    16.9        Rumna Saha
 88    16.9        Dipti Dave
 89    16.7   â˜…    Hillary Clinton
 90    16.5        Viral Gajjar
 91    16.5        Kaumil Bhavsar
 92    16.4   â˜…    Bill Clinton
 93    16.4        Bhavika Bhayani
 94    16.4   â˜…    Muhammad Ali
 95    16.1   â˜…    Prince Harry
 96    16.1        Monika Pattanayak
 97    16.0        Anmol Mehta
 98    15.8        Rohan
 99    15.6        Sanjay M Raval
100    15.5        Aastha Sachin Raval
101    15.2        Manthan
102    15.1   â˜…    Freud
103    14.9        Rama G Dave
104    14.7        Sonali Pagar
105    14.7        Tushar G Dave
106    13.5   â˜…    Charles III
107    13.5        Dhruv Jani
108    13.3        Dharini Anmol Mehta
109    13.3        Shreya
110    13.0        Riddhish Shah
111    12.6        Pooja Dave
112    12.6   â˜…    McCartney
113    12.2        Shivani Kandarp Dave
114    12.1        Priyesh Dave
115    11.4        Kandarp Dave
116    11.1   â˜…    Carl Jung
117    10.8        Kushal Shah
118    10.6        Venkat
119    10.6        Misika Butala
120    10.5   â˜…    Kurt Cobain
121    10.0        Pratiksha
122    10.0        Dhara Ravi Shah
123     8.8   â˜…    Hitler
124     7.6        Akash Zaveri
125     7.3        Shikha Dave
126     6.9        Vishal Khetrapal
127     6.6        Harshad Patel
128     6.2        Riya Viraj Shah

â˜… = famous (32), blank = ordinary (96)
Famous mean score=27.1  |  Ordinary mean=27.1
Top 20: 6 famous / 14 ordinary  |  famous median rank=74 of 128
```
