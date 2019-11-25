from appJar import gui
import socket
import threading
from threading import Thread

win = gui("Chat client ...")

host = 'localhost'
port = 12390
encoding = 'utf-8'

buffer_size = 1024
message_string = ''
pos = 0

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((str(host), int(port)))
except ConnectionRefusedError:
    print("Server is not active, unable to connect.")


def receive_from_server(conn):
    global message_string
    items_list = []
    with conn:
        while True:
            data = conn.recv(buffer_size)
            if len(data) < 1:
                print("Close the connection to server...")
                break
            else:
                message_string = data.decode(encoding)
                print('\nReceived from the server:', message_string)
                #win.setLabel("Response", message_string)
                #win.setTextArea("Response", message_string, end=False)
                items_list.append(message_string)
                win.updateListBox("Response", items_list, select=False)
                #win.addListItem("Response", message_string, select=True)

    # conn.close()

"""Set focus method"""
def enter_press(btn):
    win.setEntry("clientMsg", '')
    win.setFocus("clientMsg")

def press(btn):
    if btn == "Send":
        clientMessage = win.getEntry("clientMsg").encode()

        #win.clearTextArea("Response")
        win.clearListBox("Response")

        win.clearEntry("clientMsg")
        win.setFocus("clientMsg")

        s.sendall(clientMessage)

        #response = s.recv(buffer_size)
       # win.setLabel("Response", response.decode())

"""Login sub-windows to get client name from the user """
def login_press(btn):
    if btn == "Cancel":
        win.stop()
    else:

        clientName = win.getEntry("clientName").encode()
       # login_message = ('login' + ">>" + clientName).encode()
        #s.send(login_message)
        s.send(clientName)

        win.hideSubWindow("Login")
        win.show()
        win.setLabel("client", clientName)
        win.clearListBox("Response")

def Main():

    """Create login windows to get the client name"""
    win.startSubWindow("Login", modal=True)
    win.setSize(300, 150)
    win.setBg("gray")
    win.setTransparency(95)
    win.addLabel("loginLabel", "Enter a your name to start chat:")
    win.addEntry("clientName")
    win.addButtons(["Submit", "Cancel"], login_press)
    win.setFocus("clientName")
    win.stopSubWindow()

    """add labels to show client name"""
    win.addLabel("clientName", "Client Name: ", 0, 0)
    win.setLabelBg("clientName", "Azure")
    win.getLabelWidget("clientName").config(font="Verdana 12 overstrike")
    win.setLabelRelief("clientName", "ridge")
    win.setLabelAlign("clientName", win.NW)

    win.addEmptyLabel("client", 0, 1, 6)
    win.setLabelBg("client", "Azure")
    win.getLabelWidget("client").config(font="Verdana 12 overstrike")
    win.setLabelRelief("client", "ridge")
    win.setLabelAlign("client", win.NW)

    """
    # add the respond label - specify row/column/colspan
    win.addEmptyLabel("Response", 1, 0, 4)
    win.setLabelRelief("Response", win.GROOVE)
    win.setLabelAlign("Response", win.NW)
    win.setLabelHeight("Response", 20)
    win.setLabel("Response", "Waiting for messages")
    
    win.addScrolledTextArea('Response', 1, 0, 4)
    win.setTextAreaRelief("Response", "sunken")
    win.setTextArea("Response", "Connected to chat server.", end=True)
    win.setTextAreaBg('Response', 'Ivory')
    win.setTextAreaState('Response', 'disabled')

    """
    win.addListBox("onlineClients", [], 1, 0)
    win.setListBoxMulti("onlineClients", multi=True)

    win.addListBox("Response", [], 1, 2)
    """

    # win.registerEvent()
    # win.addListBox()
    # win.updateListBox()
    """

    win.addLabel("selectClient", "To client/s:", 2, 0)
    win.setLabelAlign("selectClient", "left")
    win.addTickOptionBox("Clients List", [], 2, 1, 4, 2)

    win.addLabel("dataFromClient", "Message:", 4, 0)
    win.setLabelAlign("dataFromClient", "left")
    win.addEntry("clientMsg", 4, 1)

    win.addButton("Send", press, 4, 3, 4)
    win.setFocus("clientMsg")



    win.enableEnter(enter_press)

    recv_thread = Thread(target=receive_from_server, args=(s,))
    recv_thread.start()

    # Client app starts with the login window as a sub-window
    win.go(startWindow="Login")

    # message = "You are connected to server..."
    # while True:
    #     message = input('\nGive a new text or <RETURN> to quit: ')
    #     if message == '':
    #         break
    #     else:
    #         s.send(message.encode(encoding))

    recv_thread.join()

    # close the connection
    s.close()

if __name__ == '__main__':
    Main()
