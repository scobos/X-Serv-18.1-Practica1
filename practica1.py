#!/usr/bin/python3

import webapp
import csv
import os
import urllib.parse

class acortaURLs(webapp.webApp):

    urlsReales = {}
    urlsAcortadas = {}
    contador = -1

    def diccAcsv(self, diccionario):
        try:
            fd = open("urls.csv", "w")
            escribir = csv.writer(fd)
            for url in diccionario:
                key = url
                valor = diccionario[key]
                escribir.writerow([key] + [valor])
        except FileNotFoundError:
            print("Imposible abrir el diccionario")
        return None;

    def csvAdicc(self, fich):
        try:
            fd = open(fich, "r")
            leido = csv.reader(fd)
            for row in leido:
                key = int(row[0]) # es el numero, la url acortada
                if self.contador < key:
                    self.contador = key
                valor = row[1] #es la url real
                self.urlsAcortadas[key] = valor
                self.urlsReales[valor] = key
        except FileNotFoundError:
            print("Imposible abrir el diccionario")

    def parse(self, request):
        """Me tengo que quedar tanto con el metodo, como recurso como cuerpo """
        request = request.replace("%2F",'/').replace("%3A", ':')
        metodo = request.split()[0]
        try:
        		recurso = request.split()[1]
        except IndexError:
            recurso = ""
        try:
            qs = request.split('\r\n\r\n', 1)[1]
            if qs.startswith('Url='): #de esta forma le quito el Url=
                qs= qs.split('=')[1]
        except IndexError:
            qs = ""

        print ("El metodo es: " + str(metodo))
        print ("El recurso es: " + str(recurso))
        print ("La qs es: " + str(qs))
        return metodo, recurso, qs

    def process(self, parsedRequest):

        metodo, recurso, qs = parsedRequest;
        try:
        		variable = int(recurso[1:])
        except ValueError:
        		variable = ""
        print("METODO, RECURSO, QS, VARIABLE en el process: " + str(metodo) + str(recurso) + str(qs) + str(variable))
        if metodo == "GET":
            if recurso == '/':
                #Si el diccionario está vacio y el fichero existe voy al diccionario
                if len(self.urlsReales)== 0:
                    if os.access("urls.csv", 0):
                        try:
                            fd = open("urls.csv", "r")
                        except FileNotFoundError:
                            fd = open('urls.csv', 'w+')

                        reader = csv.reader(fd)
                        vacio = True
                        for row in reader:
                            vacio = False
                        if not vacio: #si no esta vacio tengo que pasar el csv al diccionario
                            self.csvAdicc("urls.csv")
                    return  ("200 OK", "<html><body>" +
                             "<form method='POST' action>" +
                             "URL: <input type='text' name='Url'><br>" +
                             "<input type='submit' value='Enviar'>" +
                             "</form><body></html>")
            elif variable in self.urlsAcortadas:
                print("He entrado en redirigir")
                urlReal = self.urlsAcortadas[int(recurso[1:])]
                urlAcortada = self.urlsReales[urlReal]
                #Redirigo
                return("303 See other","<html><head>" +
                        '<meta http-equiv="refresh" content="0;url=' +
                        urlReal + '" />' + "</head></html>")
            else:
                return("404 Not Found", "<html><body><h1>Recurso no disponible</h1></body></html>")

        elif parsedRequest[0] == "POST":
            if len(qs)== 0:
                print("He entrado en el len qs=0")
                return("405 Method Not Allowed", "<html><body><h1>Go away!</h1></body></html>")
            else:
                if (qs.startswith('http://') or qs.startswith('https://')):
                    print("HE ENTRADO EN EMPIEZA POR HTTP o HTTPS")
                    urlReal = qs
                else:
                    print("HE ENTRADO EN NO EMPIEZA POR HTTP O HTTPS")
                    urlReal = "http://" + qs
                    print("Se deberia añadir http a la url: "+ urlReal)

                if urlReal in self.urlsReales: #si ya ha sido acortada
                    print(urlReal + " está en las URLs reales")
                    urlAcortada = self.urlsReales[urlReal]
                else: #no está en el diccionario, la acorto y la añado
                    self.contador = self.contador +1
                    urlAcortada = self.contador
                    self.urlsReales[urlReal] = urlAcortada
                    self.urlsAcortadas[self.contador] = urlReal
                    self.diccAcsv(self.urlsAcortadas)

                return("200 OK", "<html><body>" + '<p><a href="' +
                        str(urlAcortada) + '">Esta es tu url acortada</a></p>' +
                         "http://localhost:1234/" + str(urlAcortada) +
                         '<p><a href="' + urlReal + '">Esta es tu url real</a></p>' +
                         urlReal +  "<form method='POST' action>" +
                         "URL: <input type='text' name='Url'><br>" +
                         "<input type='submit' value='Enviar'>" +
                         "<body></html>")
        else:
            return("405 Method Not Allowed", "<html><body><h1>Go away!</h1></body></html>")


if __name__ == "__main__":
    testWebApp = acortaURLs("localhost", 1234
