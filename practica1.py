#!/usr/bin/python3

import webapp

class acortaURLs(webapp.webApp):

    urlsReales = {}
    urlsAcortadas = {}
    def parse(self, request):
        """De todo el chorizo, solo lo que me interesa """
        return request.split()

    def process(self, parsedRequest):
        print(parsedREquest);


if __name__ == "__main__":
    testWebApp = acortaURLs("localhost", 1234)
