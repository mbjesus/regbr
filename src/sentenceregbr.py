from nltk.tokenize.punkt import  PunktTrainer
from nltk.tokenize import RegexpTokenizer
import nltk
nltk.download('punkt')
from random import seed, randint

from src.preprocessing import PreProcessing

class SentenceRegBr:
    
    """This class is used to tranfrom a text into sentences for RegBr database representation."""
    
    
    def __init__(self):
        seed(93)
        self.objPreProcessing = PreProcessing()
        self.sentence_tokenizer = self.trainSenteceRegBr()
        self.stopword_list_nltk = -1
        

    def trainSenteceRegBr(self):
        """Getting PunktSentenceTokenizer trained in Portuguese and training it for particular abbreviations in the RegBr corpus."""
        
        txtCorpus = ''', e no parágrafo único do art. 1º da Resolução da Diretoria Colegiada - RDC nº 151, de 20 de abril de 2017, resolve: Art. 1º As vacinas influenza a serem comercializadas ou utilizadas no Brasil na temporada de influenza de 2019 deverão estar em conformidade com o disposto nesta Resolução. Art. 2º As vacinas influenza trivalentes a serem utilizadas no Brasil a partir de fevereiro de 2019 deverão conter, obrigatoriamente, três tipos de cepas de vírus em combinação, e deverão estar dentro das especificações abaixo descritas: - um vírus similar ao vírus influenza A/Michigan/45/2015  pdm09; - um vírus similar ao vírus influenza A/Switzerland/8060/2017 ; e - um vírus similar ao vírus influenza B/Colorado/06/2017 . Parágrafo único. Recomenda-se que o componente A  de vacinas não baseadas em ovos para uso na temporada de influenza de 2019 seja um vírus tipo A/Singapore/INFIMH-16- 0019/  juntamente com os outros componentes da vacina, conforme indicado acima. Art. 3º As vacinas influenza quadrivalentes contendo dois tipos de cepas do vírus influenza B deverão conter um vírus similar ao vírus influenza B/Phuket/3073/2013 , adicionalmente aos três tipos de cepas especificadas no Art. 2º. Art. 4º Esta Resolução entra em vigor na data de sua publicação.  ALESSANDRA PAIXÃO DIAS '''
        abbreviations = "ART."
        corpus  = self.objPreProcessing.clearText(txtCorpus)
        
        trainer = PunktTrainer()
        trainer.train(corpus, finalize=False, verbose=True)
        trainer.train(abbreviations, finalize=False, verbose=True)
        sentence_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
        sentence_tokenizer._params = trainer.get_params()
        return sentence_tokenizer
        
    def getNrTokens(self, txt):
        """ Returns the number of tokens in the a given sentence."""
        
        if(self.stopword_list_nltk == -1):
            self.getStopWordList()

        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(txt)
        filtered_sentence = [w for w in tokens if not w.lower() in self.stopword_list_nltk]
        return {"tokens_total": len(tokens), "tokens_no_stopwords":len(filtered_sentence)}


    def getStopWordList(self) -> None:
        """ Create Stop Words List in Portuguese. """
        nltk.download('stopwords')
        nltk.download('punkt')
        self.stopword_list_nltk = nltk.corpus.stopwords.words('portuguese')
        
    def getSentences(self,text):
        text = self.objPreProcessing.clearText(text)
        sentenceList = self.sentence_tokenizer.tokenize(text)
        return sentenceList
        
    def getSentencesRegBrFormat(self,text,id_doc_base,category):
        """ Returns a list with sentences in json format """
        
        sentenceTokens = self.getSentences(text)
        sentenceList = []
        position = 0
        for sentence in sentenceTokens:
            position = position + 1
            if(len(sentence)  > 100):
                sentence = self.objPreProcessing.clearText(sentence)
                nr_tokens = self.getNrTokens(sentence)
                id_al = randint(1,9999)
                idSentenca = f'{id_doc_base}_SENT_{id_al}'
                sentenceList.append({    "id_sentenca": idSentenca
                                        ,"ordem":position
                                        ,"id_doc_base": id_doc_base
                                        ,"tokens_total":nr_tokens["tokens_total"]
                                        ,"tokens_no_stopwords":nr_tokens["tokens_no_stopwords"]
                                        ,"cat_sentenca":category
                                        ,"text_sentenca":sentence
                                })
        return sentenceList