from appJar import gui
import socket
import threading
from threading import Thread

win = gui("Chat client ...")

# local host IP '127.0.0.1'
host = 'localhost'
port = 12346
encoding = 'utf-8'

buffer_size = 1024

"""Client tries to connect to server via socket"""
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((str(host), int(port)))
except ConnectionRefusedError:
    print("Server is not active, unable to connect.")


def receive_from_server(conn):
    with conn:
        while True:
            data = conn.recv(buffer_size)
            if len(data) < 1:
                print("Close the connection to server...")
                break
            print('\nReceived from the server:', (data.decode(encoding)))
            win.setLabel("Response", data.decode(encoding))

    # conn.close()

# Set focus method
def enter_press(btn):
    win.setEntry("clientMsg", '')
    win.setFocus("clientMsg")

def press(btn):
    if btn == "Send":
        clientMessage = win.getEntry("clientMsg").encode()

        win.clearEntry("clientMsg")
        win.setFocus("clientMsg")

        s.sendall(clientMessage)

        response = s.recv(buffer_size)
        win.setLabel("Response", response.decode())

"""Login sub-windows to get client name from the user """
def login_press(btn):
    if btn == "Cancel":
        win.stop()
    else:

        # clientName = win.getEntry("clientName").encode()
        # s.send(clientName)
        win.hideSubWindow("Login")
        win.show()


def Main():


    # recv_thread = Thread(target=receive_from_server, args=(s,))
    # recv_thread.start()


    # Create login windows to get the client name
    win.startSubWindow("Login", modal=True)
    win.setSize(200, 100)
    win.setBg("gray")
    win.setTransparency(95)
    win.addLabel("loginLabel", "Enter a your name to start chat:")
    win.addEntry("clientName")
    win.addButtons(["Submit", "Cancel"], login_press)
    win.setFocus("clientName")
    win.stopSubWindow()

    # add labels to show server and client addresses
    win.addLabel("clientName", "Client Name", 0, 0)
    win.addEmptyLabel("client", 0, 1)
    win.addLabel("serverName", "Server Name: ", 0, 2)
    win.addEmptyLabel("server", 0, 3)

    # add the respond label - specify row/column/colspan
    win.addEmptyLabel("Response", 1, 0, 4)
    #win.addScrolledTextArea('Response')

    # win.registerEvent()
    # win.addListBox()
    # win.updateListBox()


    win.setLabelRelief("Response", win.GROOVE)
    win.setLabelAlign("Response", win.NW)
    win.setLabelHeight("Response", 20)
    win.setLabel("Response", "Waiting for messages")

    win.addLabel("selectClient", "Select delivery  client/s:", 2, 0)
    win.addTickOptionBox("Clients List", [], 2, 1, 2, 2)

    win.addLabel("dataFromClient", "Message", 4, 0)
    win.addEntry("clientMsg", 4, 1, 2, 2)

    win.addButton("Send", press, 4, 3, 4)
    win.setFocus("clientMsg")



    win.enableEnter(enter_press)

    #win.go()
    # Client app starts with the login window as a sub-window
    win.go(startWindow="Login")

    # message = "You are connected to server..."
    # while True:
    #     message = input('\nGive a new text or <RETURN> to quit: ')
    #     if message == '':
    #         break
    #     else:
    #         s.send(message.encode(encoding))


    #recv_thread.join()

    # close the connection
    s.close()

if __name__ == '__main__':
    Main()
