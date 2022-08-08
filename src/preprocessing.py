import re
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
import nltk

class PreProcessing:

    def __init__(self):
        self.stopword_list_nltk = -1

    def clearText(self, text):
        text = str(text).strip().upper()
        text = text.encode('utf-8').decode('utf-8')
        # removing paragraph numbers
        text = re.sub('[0-9]+.\t','',str(text))
        # removing new line characters
        text = re.sub('\n ','',str(text))
        text = re.sub('\n',' ',str(text))
        # removing apostrophes
        text = re.sub("'s",' ',str(text))
        # removing hyphens
        text = re.sub("-",' ',str(text))
        text = re.sub("— ",'',str(text))
        # removing quotation marks
        text = re.sub('\"',' ',str(text))
        # removing any reference to outside text
        text = re.sub("[\(\[].*?[\)\]]", "", str(text))
        
        text = re.sub(r'\((.*?)\)',' ',text)
        text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z . ! ? : \( \) , ; À Á Â Ã Ç È É Ê Ì Í Î Ò Ó Ô Õ Ù Ú Û ])|(\w+:\/\/\S+)|^rt|http.+?|[.]{2,}", " ", text)
        text = re.sub(r'\n',' ',text)
        
        # replace multiple spaces with a single space
        text = re.sub(' +', ' ', text)
        return text


    def getTextFromHTML(self, path) -> str:
        
        f = open(path, "r", encoding = "ISO-8859-1")
        soup = BeautifulSoup(f, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        textIn = ' '.join(chunk for chunk in chunks if chunk)
        return textIn

    def getNrTokens(self, txt):

        if(self.stopword_list_nltk == -1):
            self.getStopWordList()

        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(txt)
        filtered_sentence = [w for w in tokens if not w.lower() in self.stopword_list_nltk]
        return {"tokens_total": len(tokens), "tokens_no_stopwords":len(filtered_sentence)}


    def getStopWordList(self) -> None:
        # Create Stop Words List
        nltk.download('stopwords')
        nltk.download('punkt')
        self.stopword_list_nltk = nltk.corpus.stopwords.words('portuguese')