from flask import Flask
from flask import request,jsonify
from keyphraseutils import *
import json 
from textblob import TextBlob


app = Flask(__name__) 

@app.route("/devcon/submit",methods=["POST"]) 
def kephrase_sentim_analysis():
    sentence_re = r'''(?x)          
      (?:[A-Z]\.)+        
    | \w+(?:-\w+)*        
    | \$?\d+(?:\.\d+)?%?  
    | \.\.\.              
    | [][.,;"'?():_`-]    
    '''
    grammar = r""" NP: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+}"""
    
    req=request.get_json() 
    text = req["documents"][0]["text"]
    phrase_ls = []
    toks = nltk.regexp_tokenize(text, sentence_re)
    postoks = nltk.tag.pos_tag(toks)
    chunker = nltk.RegexpParser(grammar)
    tree = chunker.parse(postoks)
    terms = get_terms(tree)
    textblob_result = TextBlob(text)

    for term in terms:
        phrase_ls.append(" ".join(term)) 
    response= {"documents":[]}
    content_info= {}
    content_info['ids']= req["documents"][0]["id"]
    content_info['keyPhrases']= phrase_ls 
    content_info['sentiment'] = textblob_result.sentiment.polarity 

    response["documents"].append(content_info)
    return response

app.run(host='0.0.0.0', port= 5000)    