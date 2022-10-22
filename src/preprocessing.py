import re
from bs4 import BeautifulSoup


class PreProcessing:

    def __init__(self):
        self.stopword_list_nltk = -1

    def clearText(self, text)  -> str:
        """ Removing unnecessary words or symbols from a sentence """
        
        text = str(text).strip().upper()
        text = text.encode('utf-8').decode('utf-8')
        
        # removing paragraph numbers
        text = re.sub('[0-9]+.\t','',str(text))
        
        # removing new line characters
        text = re.sub('\n ','',str(text))
        text = re.sub('\n',' ',str(text))
        
        # removing apostrophes
        text = re.sub("'s",' ',str(text))

        # removing quotation marks
        text = re.sub('\"',' ',str(text))
        
        # removing any reference to outside text
        text = re.sub("[\(\[].*?[\)\]]", "", str(text))
        text = re.sub(r'\((.*?)\)',' ',text)
        
        # Replacing accents of words in Brazilian Portuguese
        text = re.sub(r"(@\[A-Za-z0-9]+)|([^0-9A-Za-z . ! ? : \( \) , ; À Á Â Ã Ç È É Ê Ì Í Î Ò Ó Ô Õ Ù Ú Û ])|(\w+:\/\/\S+)|^rt|http.+?|[.]{2,}", " ", text)
        text = re.sub(r'\n',' ',text)
        
        ##drop starting or ending numbers
        text = re.sub('^[0-9]*|[0-9]*$','',text)
        text = text.strip()
        
        # replace multiple spaces with a single space
        text = re.sub(' +', ' ', text)
        return text.lower()

    def clearNumerosRomanos(self, text):
        text = re.sub(r'[MDCLXVI]*[.|;|\s|] ', '',str(text).upper())
        return text.lower()

    def getTextFromHTML(self, path) -> str:
        
        f = open(path, "r", encoding = "ISO-8859-1")
        soup = BeautifulSoup(f, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        text = soup.get_text()
        
        lines = (line.strip() for line in text.splitlines())

        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        
        # drop blank lines
        textIn = ' '.join(chunk for chunk in chunks if chunk)
        return textIn
