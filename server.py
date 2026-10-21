"""Transport HTTP minimal fourni pour l’exercice, pas un serveur de production."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pipeline import analyze

class Handler(BaseHTTPRequestHandler):
    def send_json(self, code, data):
        body=json.dumps(data,ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/health':
            self.send_json(200,{'status':'ok','model_mode':os.getenv('MODEL_MODE','reel')})
        else:
            self.send_json(404,{'error':'route inconnue'})

    def do_POST(self):
        if self.path != '/analyze':
            self.send_json(404,{'error':'route inconnue'}); return
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0 < size <= 100_000: raise ValueError('Taille de requête invalide')
            req=json.loads(self.rfile.read(size))
            if not isinstance(req,dict) or not isinstance(req.get('entretien_id'),str):
                raise ValueError('entretien_id doit être une chaîne')
            result=analyze(req['entretien_id'])
            self.send_json(200,result)
        except (ValueError, KeyError) as exc:
            self.send_json(400,{'error':str(exc)})
        except NotImplementedError as exc:
            self.send_json(501,{'error':str(exc)})
        except Exception as exc:
            self.send_json(500,{'error':type(exc).__name__})

if __name__ == '__main__':
    ThreadingHTTPServer(('0.0.0.0',int(os.getenv('PORT','8000'))),Handler).serve_forever()
