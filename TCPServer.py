from Extractor import Extractor
import inspect
import socket


class Server:
    def __init__(self, host="localhost", port=8080):
        self.SENDSIZE = 8192
        self.host = host
        self.port = port
        self.address = (host, port)
        self.methods = {}
        self.desc = "Comandos do servidor:\n\nhelp: descrição das utilidades do servidor.\
            \nf-list: lista de funções.\
            \ndesc_função: descrição de uma função.\
            \nfunção_params: executa função."
        
    def create_response(self,status_code, body):
        response = f"HTTP/1.1 {status_code}\r\n"
        response += "Content-Type: text/html\r\n"
        response += f"Content-Length: {len(body)}\r\n"
        response += f"Access-Control-Allow-Origin: *\r\n"
        response += "\r\n"
        response += body
        return response

    def register_instance(self, instance):
        for func_name, function in inspect.getmembers(
            instance, predicate=inspect.ismethod
        ):
            if not func_name.startswith(
                "__"
            ) and not func_name.startswith("sup"):
                self.methods.update({func_name: function})

    def response_handler(self, resp):
        # para o retorno de informações extras
        if resp[0] == "f-list":
            send = ", ".join(list(self.methods.keys()))
        elif resp[0] == "desc":
            send = self.methods[resp[1]].__doc__
        elif resp[0] == "help":
            send = self.desc
        else:
            # para a utilização das funções
            send = self.methods[resp[0]](*resp[1:])
        return send

    def run(self):
        # criação do socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(self.address)
            s.listen(1)

            # início da conexão
            print(f"servidor {self.address} ativo.")
            client_socket, client_address = s.accept()
            print(f"conexão com: {client_address}")
            # recebimento da mensagem do cliente
            while True:
                start_post = False
                try:
                    data = client_socket.recv(self.SENDSIZE).decode("utf-8")
                    if data.startswith("POST"): start_post = True
                    resp = data.split("\r\n\r\n", 1)[1].replace('"', '').split('.')
                    print(f"resp aqui {resp}")
                    send = self.response_handler(resp)
                # Tratamentos de erros com envio de mensagens personalizadas
                #except IndexError:
                #    send = "Parâmetros estão faltando"
                #    print(send)
                except KeyError:
                    send = "Comando desconhecido"
                    print(send)
                except (ValueError, TypeError):
                    send = (
                        "Parâmetros de entrada inválidos ou incompletos"
                    )
                    print(send)
                except (ConnectionAbortedError, KeyboardInterrupt):
                    print(f"Servidor {self.address} interrompido")
                    s.close()
                    break

                # envio da resposta para o socket cliente
                if start_post: 
                    send = self.create_response(200, str(send))
                client_socket.sendall(str(send).encode("utf-8"))


def main():
    server = Server()
    inst = Extractor()
    server.register_instance(inst)
    server.run()


if __name__ == "__main__":
    main()
