import os
import re
class Pacote:
    def __init__(self):
        self.id = ""
        self.FROM = ""
        self.TO = ""
        self.conteudo = []
class Log:

    def __init__(self):
        self.arqs = []
        self.callid = []
        self.bilhetes = []
        self.bilhetes_escolhidos = []
        self.call = ""        
        self.separadow = ""
        self.f = []
        self.arquivofinal = ""
        self.resultadoFinal = []
        self.bilheteSozinho = Pacote
        self.bilheteSozinhoConteudo = []
        self.call_id = ""
        self.nlSIP = re.compile('[0-9*]{2}:[0-9*]{2}:[0-9*]{2}.[0-9*]{3}')
        self.nlRM = re.compile('[0-9*]{4}-[0-9*]{2}-[0-9*]{2}')
        self.appType = ""
        self.IDAPP = {"RM":{"iniPacote":"CCPSIPMessageInterceptor","reg":'[0-9*]{4}-[0-9*]{2}-[0-9*]{2}'}
                    ,"SIPServer":{"iniPacote":" [0,UDP] ","reg":'[0-9*]{2}:[0-9*]{2}:[0-9*]{2}.[0-9*]{3}'}}
        self.TO = ""
        self.FROM = ""


    def ArquivoFinal(self):
        self.separadow = open(input("Digite o nome do arquivo final sem extensão: ") + '.txt', 'w')
        
    def defineArqFinal(self):
        self.separadow = open(self.arquivofinal, 'w')

    def DirecionaFolder(self):
        os.chdir(input("Digite a pasta: "))

    def listArqs(self):
        self.arqs = os.listdir()

    def busca(self):
        self.call = input("Digite o numero: ")


    def criaListaCallid(self,linha):
        if linha.find("Call-ID: ") >= 0:
            callidstr = linha[linha.find("Call-ID: ") + 9:linha.find("@")]
            self.call_id = callidstr
            if callidstr not in self.callid:
                self.callid.append(callidstr)
    
    def identificaANI(self,linha):
        if linha.find("From:") >= 0:
            self.FROM = linha[linha.find("ip:") + 3:linha.find("@")]

        elif linha.find("To:") >= 0:
            self.TO = linha[linha.find("ip:") + 3:linha.find("@")]

        else:
            pass


    def openFile(self):
        for a in self.arqs:
            if a.find("rm_") < 0:
                continue
            with open(a, 'r', encoding='utf-8', errors='ignore') as file:
                self.f = file.readlines()
            file.close()
            self.preencheBilhetes(self.f)

        self.preencheBilhetesEscolhidos()

    def preencheBilhetes(self,f):
        sip = False
        for linha in f:
            if linha.find(self.IDAPP[self.appType]['iniPacote']) > 1:
                sip = True
                self.bilheteSozinhoConteudo.append(linha)
            else:
                regApp = re.compile(self.IDAPP[self.appType]['reg'])

                if sip == True and (regApp.match(linha) == None):
                    if len(linha) > 2:
                        self.bilheteSozinhoConteudo.append(linha)
                        self.criaListaCallid(linha)
                        if (linha.find("From:") >= 0  or linha.find("To:") >= 0) and linha.find("@") >= 0:
                            self.identificaANI(linha)
                else:
                    if sip == True:
                        pacote = Pacote()
                        pacote.id,pacote.FROM,pacote.TO,pacote.conteudo = self.call_id,self.FROM,self.TO,self.bilheteSozinhoConteudo
                        self.bilhetes.append(pacote)
                        self.call_id = ""
                        self.TO = ""
                        self.FROM = ""
                        self.bilheteSozinhoConteudo = []
                    sip = False
        
    def preencheBilhetesEscolhidos(self):
        for linhab in self.bilhetes_escolhidos:
            acabou = False
            count = linhab
            direcao = ""
            while acabou is not True:
                if len(str(self.bilhetes[count])) < 3:
                    acabou = True
                    self.resultadoFinal.append("\n")
                else:
                    if "Message sent" in str(self.bilhetes[count]):
                        direcao = ">>"
                    elif "Message received" in str(self.bilhetes[count]):
                        direcao = "<<"
                    else:
                        direcao = direcao
                    self.resultadoFinal.append(direcao + " " + self.bilhetes[count])
                    count = count + 1

if __name__ == '__main__':
    log = Log()
    log.DirecionaFolder()
    log.ArquivoFinal()
    log.listArqs()
    log.busca()
    log.openFile()