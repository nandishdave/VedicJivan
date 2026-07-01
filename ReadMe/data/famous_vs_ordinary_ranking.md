# Famous vs Ordinary - Full Ranking (Dhana + Prosperity + graded Raja yoga)

All 128 charts (32 famous star + 96 ordinary), cross-validated 8-feature model.
Yoga features from api/app/services/kundli_calculator/:
  - Dhana yoga       = lords of 1/2/11 (wealth)                    [dhana_yoga.py]
  - Prosperity yoga  = links touching 5/9 (fortune), separate      [dhana_yoga.py]
  - Raja yoga        = kendra(1/4/7/10)+trikona(1/5/9) lords,       [raja_yoga.py]
                       graded by connection x lord-grade x dignity
                       x house x COMBUSTION (replaces crude trikona)

Honest note: none of the yogas separate fame (famous 26.6 vs ordinary 26.5, famous
median rank 63/128) - they are wealth/fortune/power readouts, not fame predictors.
Regenerate with scripts/score_ranking.py.
```text
RANK  SCORE  WHO   NAME
  1    69.4   â˜…    Tesla
  2    68.1   â˜…    Churchill
  3    60.2        Dhaval J Shah
  4    56.0   â˜…    GW Bush
  5    53.3        Binal Shah
  6    53.2        Sahil Jani
  7    52.3        Rahul R Joshi
  8    51.9        Bhargav M Raval
  9    51.3        Hardik Suchak
 10    51.0        Esha Shah
 11    50.5        Helena Dave
 12    50.3        Harsh Trivedi
 13    50.2        Shobha Dave
 14    49.5        Heena T Dave
 15    46.5        Lav Butala
 16    46.2   â˜…    Oprah
 17    44.6        Priyal Parikh
 18    43.9        Bhupesh Kumar
 19    42.1        Snehal J Chauhan
 20    41.8        Grandin Major Vincent
 21    41.5        Pooja Priya
 22    39.9        Karan Patel
 23    39.5        Nayan Shah
 24    38.0        Nency A Shah
 25    37.4        Yaduvendra Chaurasia
 26    36.5        Harsh Raval
 27    36.4        Ruchi Raval
 28    36.3        Partha Saha
 29    36.1   â˜…    Hendrix
 30    36.1        Neha Khetrapal
 31    35.8        Harshal Joshi
 32    35.7   â˜…    Freud
 33    34.1   â˜…    Elvis
 34    34.0        Arohi N Parikh
 35    33.9        Bhusan Savani
 36    33.6        Harsh Shah
 37    33.5   â˜…    Muhammad Ali
 38    33.0   â˜…    John Lennon
 39    32.4   â˜…    Taylor Swift
 40    32.3   â˜…    Reagan
 41    30.5   â˜…    Madonna
 42    30.3        Priyesh Dave
 43    29.9        Bhargav
 44    29.9        Vixita Nayak
 45    29.8        Pragati Nayak
 46    29.7        Aastha Sachin Raval
 47    29.6        Janki Dave
 48    29.0        Jinal Shah
 49    28.5        Nandish Dave
 50    28.2   â˜…    Jim Morrison
 51    28.1        Manish Singh
 52    28.1        Aniket Shah
 53    27.8        Shikha Kumari
 54    27.7        Viraj Shah
 55    27.6   â˜…    Carl Jung
 56    27.5   â˜…    Trump
 57    27.2        Melvin Methew
 58    27.0   â˜…    Queen Elizabeth II
 59    26.9        Bishal Bose
 60    26.8        Viral Gajjar
 61    26.4        Nishit Parikh
 62    25.5        Rama G Dave
 63    24.9        Prasad
 64    24.9        Krutik Shah
 65    24.5        Darshan
 66    24.4        Sneha Shah
 67    24.1        Kaumil Bhavsar
 68    23.8   â˜…    Prince Harry
 69    23.2        Yatin Mirani
 70    23.1        Vatsal Raicha
 71    21.9        Riddhish Shah
 72    21.8        Varta Shah
 73    21.7        Jigar Mehta
 74    21.2        Rupal Raghuvanshi
 75    21.2   â˜…    Angelina Jolie
 76    20.6        Tushar G Dave
 77    20.2        Sanjay M Raval
 78    20.1        Vishal Khetrapal
 79    19.4        Pooja Dhaval Shah
 80    19.4        Shreya
 81    19.0        Jigisha Dhruv Jani
 82    18.7   â˜…    Darwin
 83    18.7   â˜…    Diana
 84    18.5        Varun Chaturvedi
 85    17.9        Venkat
 86    17.7   â˜…    Marilyn Monroe
 87    17.7        Jainith Nayak
 88    17.7   â˜…    Bill Clinton
 89    17.4   â˜…    Charles III
 90    15.8   â˜…    Kurt Cobain
 91    15.7   â˜…    Michael Jackson
 92    15.5        Dhruv Jani
 93    15.4        Mayank Kumar
 94    15.4        Paras Gajjar
 95    15.3        Suraj Mehta
 96    15.2        Monika Pattanayak
 97    14.9        Bhavika Bhayani
 98    14.9        Moxta
 99    14.6        Harshad Patel
100    14.4        Yatin Punjabi
101    14.1        Anmol Mehta
102    13.8        Shivani Kandarp Dave
103    13.8        Devang Shah
104    13.7        Ravi Shah
105    13.6        Kushal Shah
106    13.6        Kandarp Dave
107    13.0        Pooja Dave
108    12.9        Dhara Ravi Shah
109    12.4        Sonali Pagar
110    12.4   â˜…    Obama
111    12.2   â˜…    Hillary Clinton
112    12.0        Dharini Anmol Mehta
113    11.9   â˜…    JFK
114    11.9        Praveen
115    10.9        Manthan
116    10.2        Rumna Saha
117    10.0        Shikha Dave
118     9.9   â˜…    Prince William
119     9.6        Papu ben
120     9.2        Misika Butala
121     9.0        Rohan
122     8.7   â˜…    Hitler
123     8.0   â˜…    McCartney
124     7.3        Pratiksha
125     6.3        Akash Zaveri
126     5.4        Dipti Dave
127     4.9   â˜…    Einstein
128     4.1        Riya Viraj Shah

â˜… = famous (32), blank = ordinary (96)
Famous mean score=26.6  |  Ordinary mean=26.5
Top 20: 4 famous / 16 ordinary  |  famous median rank=63 of 128
```
