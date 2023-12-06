import socket
from extractor import genius_extractor

def create_response(status_code, body):
  response = f"HTTP/1.1 {status_code}\r\n"
  response += "Content-Type: text/html\r\n"
  response += f"Content-Length: {len(body)}\r\n"
  response += f"Access-Control-Allow-Origin: *\r\n"
  response += "\r\n"
  response += body
  return response

def main():
  host = 'localhost'
  port = 8080

  server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_socket.bind((host, port))
  server_socket.listen(1)

  print(f"Servidor HTTP rodando em http://{host}:{port}")

  while True:
      client_socket, client_address = server_socket.accept()
      print(f"Conexão recebida de {client_address[0]}:{client_address[1]}")

      data = client_socket.recv(8192).decode('utf-8')
      print(f"Recebido:\n{data}")

      # Verifica se a requisição é um POST
      if data.startswith("POST"):
          # Obtém o corpo da requisição POST
          body = data.split("\r\n\r\n", 1)[1].replace('"', '')
          
          # Exibe o corpo da requisição no console
          print(f"Conteúdo da requisição POST:\n{body}")
          msg = genius_extractor.extractor(body)
          
          # Aqui você pode processar o corpo da requisição POST como desejado
          # Por exemplo, você pode salvar os dados em um arquivo de log ou banco de dados

          # Para uma resposta simples, você pode retornar o corpo de volta
          response = create_response(200, msg)
      else:
          # Para outras requisições, retorne uma resposta padrão
          response = create_response(200, msg)

      client_socket.send(response.encode('utf-8'))
      client_socket.close()

if __name__ == "__main__":
  main()