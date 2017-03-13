#!/usr/bin/python3

import webapp
import csv
import os
import urllib

class acortaURLs(webapp.webApp):

    urlsReales = {}
    urlsAcortadas = {}
    contador = -1

    def diccAcsv(self, fich):
        try:
            fd = open("urls.csv", "w")
            escribir = csv.writer(fd)
            for url in diccionario:
                key = url
                valor = diccionario[key]
                escribir.writerow([key] + [valor])
        except FileNotFoundError:
            print("Imposible abrir el diccionario")


    def csvAdicc(self, fich):
        try:
            fd = open(fich, "r")
            escribir = csv.writer(fd)
            for url in diccionario:
                key = url
                valor = diccionario[key]
                escribir.writerow([key] + [valor])
        except FileNotFoundError:
            print("Imposible abrir el diccionario")

        return None;


    def parse(self, request):
        """Me tengo que quedar tanto con el metodo, como recurso como cuerpo """
        #request = request.replace("%2F",'/').replace("%3A", ':')
        #return request.split()
        print ("La request es: " + str(request))
        metodo = request.split()[0]
        try:
        		recurso = request.split()[1]
        except IndexError:
            recurso = ""
        try:
            qs = request.split()[1][4:]
        except IndexError:
            qs = ""

        print ("El metodo es: " + str(metodo))
        print ("El recurso es: " + str(recurso))
        print ("La qs es: " + str(qs))
        return metodo, recurso, qs

    def process(self, parsedRequest):

        print(parsedRequest);
        metodo, recurso, qs = parsedRequest;
        try:
        		variable = int(recurso[1:])
        except ValueError:
        		variable = ""

        print("METODO, RECURSO, QS, VARIABLE en el process: " + str(metodo) + str(recurso) + str(qs) + str(variable))
        if metodo == GET:
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
                            serf.csvAdicc("urls.csv")
                    return  ("200 OK", "<html><body>" \
                            + "<form method='POST' action>" \
                            + "URL: <input type='text' name='Url'><br>" \
                            + "<input type='submit' value='Enviar'>" \
                            + "</form><body></html>")
                elif variable in self.urlsAcortadas:
                    urlReal = self.urlsAcortadas[int(recurso[1:])]
                    urlAcortada = self.urlsReales[urlReal]
                    #Redirigo
                    return("303 See other","<html><head>" +
                            '<meta http-equiv="refresh" content="0;url=' +
                            url_real + '" />' + "</head></html>")
                else:
                    return("404 Not Found", "<html><body><h1>Recurso no disponible</h1></body></html>")

        elif parsedRequest[0] == POST:
            if len(qs)== 0:
                return("405 Method Not Allowed", "<html><body><h1>Go away!</h1></body></html>")
            else:
                if urllib.unquote(qs[0:13]) == "http://":
                    urlReal = "http://" + qs[13:]
                elif urllib.unquote(qs[0:14]) == "https://":
                    urlReal = "https://" + qs[14:]
                else:
                    urlReal = "http://" + qs

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
                        str(url_acortada) + '">Esta es tu url acortada</a></p>' +
                         '<p><a href=' + url_real + '/>' +
                         'Esta es tu url real</a></p>' +
                         "</body><html>")
        else:
            return("405 Method Not Allowed", "<html><body><h1>Go away!</h1></body></html>")


if __name__ == "__main__":
    testWebApp = acortaURLs("localhost", 1234)
