import re

raw_text = '''
Touch by Lucky Tapes
Little something crazy
Everything is all right
Little something lonely
Everything is all right
I know you were a player
You know I used to be
We have known the meaning of love
lf we waste the night to Sunday
lf I run into you someday
We should call this happen "The precious love"
Touch a piece of your heart
We'll have to make another love
Dancing all night
Touch a piece of your heart
I wanna take your soul tonight
Please please tell me
Little something lazy
Everything is all right
Little something weary
Everything is all right
l know you were a player
You know l used to be
We have known the meaning of love
lf we waste the night to Sunday
If I run into you someday
We should call this happen "The precious love"
l miss you now you're gone
When you get back everything will be alright
Touch a piece of your heart
We'll have to make another love
Dancing all night
Touch a piece of your heart
l wanna take your soul tonight
Please please tell me
Touch a piece of your heart
We'll have to make another love, dancing all night
Touch a piece of your heart
I wanna take your soul tonight
Baby please please tell me
'''
text = re.sub('[\.,"]', '', raw_text)
words = list(set(filter(lambda s: len(s) > 0, re.split(r'\s', text))))
