from nltk.tokenize.punkt import  PunktTrainer
from nltk import tokenize  
import nltk
from random import seed, randint
import string
import re

from src.preprocessing import PreProcessing

class SentenceRegBr:
    
    """This class is used to tranfrom a text into sentences for RegBr database representation."""
    
    
    def __init__(self):
        seed(93)
        self.objPreProcessing = PreProcessing()
        self.getStopWordList()
        self.sentence_tokenizer = self.trainSenteceRegBr()
        

    def trainSenteceRegBr(self):
        """Getting PunktSentenceTokenizer trained in Portuguese and training it for particular abbreviations in the RegBr corpus."""
        
        txtCorpus = ''', e no parágrafo único do art. 1º da Resolução da arts. 20 Diretoria Colegiada - RDC nº Nr. 151 n. 151, de N. 20 de abril de 2017, resolve: Art. 1º As sra. vacinas influenza a serem comercializadas ou utilizadas no sr. Brasil na temporada de influenza de 2019 deverão estar em conformidade com o disposto nesta Resolução. Art. 2º As vacinas influenza trivalentes a serem utilizadas no Brasil a partir de fevereiro de 2019 deverão conter, obrigatoriamente, três tipos de cepas de vírus em combinação, e deverão estar dentro das especificações abaixo descritas: - um vírus similar ao vírus influenza A/Michigan/45/2015  pdm09; - um vírus similar ao vírus influenza A/Switzerland/8060/2017 ; e - um vírus similar ao vírus influenza B/Colorado/06/2017 . Parágrafo único. Recomenda-se que o componente A  de vacinas não baseadas em ovos para uso na temporada de influenza de 2019 seja um vírus tipo A/Singapore/INFIMH-16- 0019/  juntamente com os outros componentes da vacina, conforme indicado acima. Art. 3º As vacinas influenza quadrivalentes contendo dois tipos de cepas do vírus influenza B deverão conter um vírus similar ao vírus influenza B/Phuket/3073/2013 , adicionalmente aos três tipos de cepas especificadas no Art. 2º. Art. 4º Esta Resolução entra em vigor na data de sua publicação.  ALESSANDRA PAIXÃO DIAS '''
        
        abbreviations = "art. arts. nr. n. sr. sra. ms. msr."
        corpus  = self.objPreProcessing.clearText(txtCorpus)
        
        trainer = PunktTrainer()
        trainer.train(corpus, finalize=False, verbose=True)
        trainer.train(abbreviations, finalize=False, verbose=True)
        sentence_tokenizer = nltk.data.load('tokenizers/punkt/portuguese.pickle')
        sentence_tokenizer._params = trainer.get_params()
        return sentence_tokenizer
        
    def getNrTokensFull(self, txt):
        """ Returns the number of tokens in the a given sentence."""
        tokens = tokenize.word_tokenize(txt, language='portuguese')
        return len(tokens)

    def getNrTokensNoStopWords(self, txt):
        """ Returns the number of tokens in the a given sentence."""
        
        tokens = self.getTokensNoStopWords(txt)
        return len(tokens)

    def getTokensNoStopWords(self,txt):
        if(self.stopword_list_nltk == -1):
            self.getStopWordList()
            
        tokens = tokenize.word_tokenize(txt.translate(str.maketrans('', '', string.punctuation)), language='portuguese')
        tokens = [w for w in tokens if not w.lower() in self.stopword_list_nltk]
        return tokens


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
        maxTokensBySentence = 512
        minTokensNoStopSplitIncisosBySentence = 50
        minTokensNoStopBySentence = 0
        
        sentenceList = []
        position = 0
        for sentence in sentenceTokens:
            position = position + 1
            if(self.getNrTokensNoStopWords(sentence)  > minTokensNoStopBySentence):
                
                if(self.getNrTokensNoStopWords(sentence)  < minTokensNoStopSplitIncisosBySentence):
                
                    id_al = randint(1,9999999)
                    idSentenca = f'{id_doc_base}_SENT_{id_al}'
                    dictSentence = self.getDictSentence(idSentenca, position, id_doc_base, sentence, category)
                    sentenceList.append(dictSentence)

                else:

                    ##DROP IN INCISOS IF EXISTS
                    txtList = re.split(r'; [MDCLXVI]+ ', sentence, flags=re.IGNORECASE)
                    txtList = [str(texto).strip() for texto in txtList if str(texto).strip() != ""]
                    
                    for txt in txtList:

                        ##GET "tokens_total"
                        tokens_total = self.getNrTokensFull(txt)
                        if(tokens_total > maxTokensBySentence):
                            tokens = tokenize.word_tokenize(txt, language='portuguese')
                            for i in range(0,len(tokens),maxTokensBySentence):
                                lim = i+maxTokensBySentence
                                if(lim > len(tokens) ):
                                    lim = len(tokens)
                                subtxt = ' '.join(tokens[i:lim])

                                id_al = randint(1,9999999)
                                idSentenca = f'{id_doc_base}_SENT_{id_al}'
                                dictSentence = self.getDictSentence(idSentenca, position, id_doc_base, subtxt, category)
                                sentenceList.append(dictSentence)
                                position = position + 1
                        else:
                            id_al = randint(1,9999999)
                            idSentenca = f'{id_doc_base}_SENT_{id_al}'
                            dictSentence = self.getDictSentence(idSentenca, position, id_doc_base, txt, category)
                            sentenceList.append(dictSentence)
                            position = position + 1
                
        return sentenceList

    def getDictSentence(self, p_idSentenca, p_position, p_id_doc_base, p_sentence, p_category):

         return {    "id_sentenca": p_idSentenca
                                                    ,"ordem":p_position
                                                    ,"id_doc_base": p_id_doc_base
                                                    ,"tokens_total":self.getNrTokensFull(p_sentence)
                                                    ,"tokens_no_stopwords":self.getNrTokensNoStopWords(p_sentence)
                                                    ,"cat_sentenca":p_category
                                                    ,"text_sentenca":p_sentence
                                            }
