import sys,time,network,gc,socket
gc.collect()

class MicroServer:
    
    HOST = '0.0.0.0'
    PORT = 80
    MAX_REQUESTS = 1
    CLIENT_SOCKET_TIMEOUT = 0
    client_count = 0
    
    def application(self,client_socket,client_address,client_count):

        data = f"Client {client_count} at {client_address[0]}"
        

        response = f"HTTP/1.1 200 OK\nContent-Type: text/plain\nContent-Length: {len(data)}\n\n"
        
        yield response.encode()
        yield data.encode()
    
    def serve(self):
        
        self.server_address = socket.getaddrinfo(self.HOST,self.PORT)[0][-1]

        while True:

            try:
                server_socket = socket.socket()
                server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
                server_socket.bind(self.server_address)
                server_socket.listen(self.MAX_REQUESTS)
                print(f"MicroServer Started at http://192.168.4.1:{self.PORT}/")

                while True:
                    client_socket,client_address = server_socket.accept()
                    t1 = time.ticks_ms()
                    self.client_count += 1
                    client_socket.settimeout(self.CLIENT_SOCKET_TIMEOUT) 
                    print(f"Client {self.client_count}: {client_address[0]} - ",end='')

                    bytecount = 0
                    for block in self.application(client_socket,client_address,self.client_count):
                        try:
                            bytecount += client_socket.write(block)
                        except:
                            pass
                    
                    client_socket.close()
                    gc.collect()
                    print(f"sent {bytecount} bytes in {round(time.ticks_diff(time.ticks_ms(),t1)/1000.0,2)} secs.")

            except KeyboardInterrupt:
                print('KeyboardInterrupt: End server loop.')
                break

            except Exception as e:
                print('Exception: Go to socket reset.')
                sys.print_exception(e)

            finally:
                try:
                    gc.collect()
                    print('Closing main socket...',end=' ')
                    server_socket.close()
                    print('closed.')
                except:
                    print('FAILED!')
 
