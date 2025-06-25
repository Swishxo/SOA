import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

'''
If the compound score is greater than or equal to 0.05, the sentiment is positive.
If the compound score is less than or equal to -0.05, the sentiment is negative.
If the compound score is between -0.05 and 0.05, the sentiment is neutral.
'''
# ranges from -4 to 4 so a more detailed set can be made 

res = []


countPos = 0
countNeg = 0
countNeu = 0

#Grade incoming text and give each a compound score
    #Grades: Positive, Negative, & Neutral 
def scoreText(incoming):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(incoming)

    global countPos, countNeg, countNeu

    if(score['compound'] >= 0.05):
        countPos += 1 
    elif(score['compound'] <= -0.05):
        countNeg += 1
    else:
        countNeu += 1


#functions to get corresponding composite score
def getPos():
    return countPos

def getNeg():
    return countNeg

def getNeu():
    return countNeu

def reset():
    global countPos, countNeg, countNeu
    countPos = 0
    countNeg = 0
    countNeu = 0

    
