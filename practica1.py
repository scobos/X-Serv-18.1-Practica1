#!/usr/bin/python3

import webapp

class acortaURLs(webapp.webApp):

    urlsReales = {}
    urlsAcortadas = {}
    def parse(self, request):
        """De todo el chorizo, solo lo que me interesa """
        return request.split()

    def process(self, parsedRequest):
        print(parsedRequest);

        if parsedRequest[0] == GET:
            respuesta = "200 OK", "<html><body>"
                        + '<form method="POST" action="">'
                        + 'URL: <input type="text" name="Url"><br>'
                        + '<input type="submit" value="Enviar">'
                        + "</form><body></html>"
                        
        elif parsedRequest[0] == POST:



if __name__ == "__main__":
    testWebApp = acortaURLs("localhost", 1234)
