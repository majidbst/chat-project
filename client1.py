from appJar import gui
import socket
from threading import Thread

win = gui("Chat client ...", "450x320")

#host = 'localhost'
host = socket.gethostbyname(socket.gethostname())
port = 12345
encoding = 'utf-8'

buffer_size = 1024
message_string = ''
pos = 0
clientName = ""

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
                items_list.append(message_string)
                win.updateListBox("Response", items_list, select=False)

    # conn.close()

"""Set focus method"""
def enter_press(btn):
    win.setEntry("clientMsg", '')
    win.setFocus("clientMsg")

def press(btn):
    if btn == "Send":
        #clientMessage = win.getEntry("clientMsg").encode()
        clientMessage = win.getEntry("clientMsg")

        win.clearListBox("Response")
        win.clearEntry("clientMsg")
        win.setFocus("clientMsg")

        destination_client = win.getListBox("onlineClients")


        msg = "msg" + ":" + clientName + ":" + "all" + ":" + clientMessage
        s.sendall(msg.encode())
        #s.sendall(clientMessage)

"""Login sub-windows to get client name from the user """
def login_press(btn):
    global clientName
    if btn == "Cancel":
        win.stop()
    else:

        #clientName = win.getEntry("clientName").encode()
        clientName = win.getEntry("clientName")
        login_msg = "Login" + ":" + clientName
        s.send(login_msg.encode())
        #s.send(clientName)

        win.hideSubWindow("Login")
        win.show()
        win.setLabel("client", clientName)
        win.clearListBox("Response")

def Main():

    """Create login windows to get the client name"""
    win.startSubWindow("Login", modal=True)
    win.startLabelFrame("Login Details")
    win.setSticky("ew")
    win.setFont(14)
    #win.setTransparency(95)
    win.addLabel("loginLabel", "Name", 0, 0)
    win.addEntry("clientName", 0, 1)
    win.addButtons(["Submit", "Cancel"], login_press, 2, 0, 2)
    win.stopLabelFrame()
    win.setFocus("clientName")
    win.stopSubWindow()

    win.startFrame("TOP", row=0, column=0)
    win.startLabelFrame("Client Name", row=0, column=0)
    win.setSticky("NEW")
    win.addEmptyLabel("client", 0, 1)
    win.setLabelBg("client", "Azure")
    win.getLabelWidget("client").config(font="Verdana 14 bold italic overstrike")
    win.setLabelAlign("client", "center")
    win.stopLabelFrame()
    win.stopFrame()

    win.startFrame("CENTER", row=1, column=0)

    win.startFrame("LEFT", row=1, column=0)
    win.addLabel("OnlineClients", "Online Clients", row=1, column=0)
    win.getLabelWidget("OnlineClients").config(font="Verdana 12 italic overstrike")
    win.setLabelAlign("OnlineClients", win.SW)
    win.addListBox("onlineClients", [], 2, 0)
    win.setListBoxMulti("onlineClients", multi=True)
    win.stopFrame()

    win.startFrame("MIDDLE", row=2, column=1)
    win.addLabel("MIDDLE", [], 2, 0)
    win.stopFrame()

    win.startFrame("RIGHT", row=1, column=2)
    win.addLabel("Messages", row=1, column=2)
    win.getLabelWidget("Messages").config(font="Verdana 12 italic overstrike")
    win.setLabelAlign("Messages", win.SW)
    win.setSticky("NEW")
    win.addListBox("Response", [], 2, 2)
    win.stopFrame()

    win.stopFrame()

    win.startFrame("BOTTOM", row=2, column=0)
    win.addLabel("Message", row=2, column=0)
    win.getLabelWidget("Message").config(font="Verdana 12 italic overstrike")
    win.setLabelAlign("Message", win.SW)

    win.addEntry("clientMsg", 3, 0)
    win.setEntrySticky("clientMsg", "both")
    win.addButton("Send", press, 3, 3)
    win.setButtonSticky("Send", "both")

    win.setFocus("clientMsg")
    win.stopFrame()

    win.enableEnter(enter_press)

    recv_thread = Thread(target=receive_from_server, args=(s,))
    recv_thread.start()

    # Client app starts with the login window as a sub-window
    win.go(startWindow="Login")
    recv_thread.join()

    # close the connection
    s.close()

if __name__ == '__main__':
    Main()
