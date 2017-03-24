# -*- coding: utf-8 -*-

def ler_arquivo_conf_banco(path):
    _file = open(path, "r")
    _result = {}
    linha = _file.readline()
    while linha:
        linha = linha.split()
        for i in linha:
            item = i.split('|')
            _result[item[0]] = item[1]
        linha = _file.readline()
    _file.close()
    return _result