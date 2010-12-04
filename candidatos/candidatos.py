# -*- coding: utf-8 -*-

################################################################################
# open data hackathon 2010                   ###################################
#                                                             ##################
# vilson@void.cc ~ http://automata.cc ~ http://musa.cc    ######################
################################################################################

from urllib import urlopen
from xml.etree.ElementTree import parse
from os import listdir
from itertools import groupby
import pylab

#
# Coleta
#

def xml2dict(el):
    d={}
    if el.text:
        d[el.tag] = el.text
    else:
        d[el.tag] = {}
    children = el.getchildren()
    if children:
        d[el.tag] = map(xml2dict, children)
    return d

def dict2class(d):
    class Candidato:
        pass

    c = Candidato
    for elem in d.keys():
        c.__dict__[elem] = d[elem]
    return c

def candidatos2dict(start=1, end=22297):
    candidatos = []
    for i in range(start, end+1):
        print 'crawling candidato ', i
        tree = parse(urlopen('http://www.williamprogrammer.com/EleicoesAbertas/apiEleicoes/beta/2010/candidatos/' + str(i)))
        root = tree.getroot()
        candidato = xml2dict(root)
        d = {}
        for c in candidato['candidato']:
            for x in c:
                d[x] = c[x]
        candidatos.append(d)
        serialize(candidatos, 'candidatos_backup.pkl')
    return candidatos

def candidatos2objects(start=1, end=22597):
    candidatos = candidatos2dict(start, end)
    objetos = [dict2class(c) for c in candidatos]
    return objetos

def backup2objects(path):
    files = listdir(path)
    objs = []
    for f in files:
        objs += [dict2class(c) for c in unserialize(path + f)]
    return objs

def getDespesas(candidato):
    if candidato.__dict__.has_key('urlDadosDespesa'):
        f = urlopen(candidato.urlDadosDespesa)
        s = f.read()
        if s is not '':
            l = s.split('\n')
            t = [li.split(';') for li in l]
            return t[:len(t)-1]
        return ''
    return ''

def getTotalDespesas(candidato):
    d = getDespesas(candidato)
    t = [reais2float(x[4]) for x in d[1:]]
    return sum(t)

#
# Utils
#

def reais2float(s):
    return float(s.replace('.', '').replace(',', '.').replace('R$ ', ''))

#
# Serialização
#

# serializando para arquivo
def serialize(dado, arquivo='dado.pkl'):
    import pickle

    saida = open(arquivo, 'wb')
    pickle.dump(dado, saida)
    saida.close()

# "deserializando" do arquivo
def unserialize(arquivo='dado.pkl'):
    import pickle

    entrada = open(arquivo, 'rb')
    dado = pickle.load(entrada)
    entrada.close()

    return dado

#
# Análise
#

def plotCandidatoPor(atributo, candidatos):
    if atributo is 'partido':
        conjunto = [c.partido[1]['sigla'] for c in candidatos]
    elif atributo is 'ocupacao':
        conjunto = [c.ocupacao[0]['ocupacao'] for c in candidatos]
    elif atributo is 'cargo':
        conjunto = [c.cargo[0]['cargo'] for c in candidatos]
    elif atributo is 'grauInstrucao':
        conjunto = [c.grauInstrucao[0]['grauInstrucao'] for c in candidatos]
    elif atributo is 'estado':
        conjunto = [c.estado[1]['uf'] for c in candidatos]
    elif atributo is 'coligacao':
        conjunto = [c.coligacao[0]['coligacao'] for c in candidatos]
    elif atributo is 'estadoCivil':
        conjunto = [c.estadoCivil[0]['estadoCivil'] for c in candidatos]
    elif atributo is 'nacionalidade':
        conjunto = [c.nacionalidade[0]['nacionalidade'] for c in candidatos]
    elif atributo is 'situacao':
        conjunto = [c.situacao[0]['situacao'] for c in candidatos]
    elif atributo is 'sexo':
        conjunto = [c.sexo[0]['sexo'] for c in candidatos]
    elif atributo is 'resultadoEleicao':
        conjunto = [c.resultadoEleicao[0]['resultadoEleicao'] for c in candidatos]
    elif atributo is 'estadoNascimento':
        conjunto = [c.cidadeNascimento[1]['estado'][1]['uf'] for c in candidatos]
    elif atributo is 'cidadeNascimento':
        conjunto = [c.cidadeNascimento[0]['cidade'] for c in candidatos]

    s = [(x,len(list(y))) for x,y in groupby(sorted(conjunto))]
    s = sorted(s, key=lambda x: x[1])
    siglas = [x[0] for x in s]
    qtd = [x[1] for x in s]
    posicoesY = pylab.arange(len(siglas)) + .5
    posicoesX = qtd
    pylab.title('quantidade de candidatos por ' + atributo)
    pylab.barh(posicoesY, posicoesX, align='center')
    pylab.grid(True)
    pylab.yticks(posicoesY, tuple(siglas))
    pylab.ylabel(atributo)
    pylab.xlabel('quantidade de candidatos')
    y = 0
    for x in posicoesX:
        pylab.text(x+5, posicoesY[y]-.5, x)
        y += 1
    pylab.show()

#
# Testes
#

def run():
    cs = backup2objects('/home/vilson/meu-src/hackathon2010/candidatos/')
    return cs
