from chat_utils import *
import json
from DES import des


class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ""
        self.me = ""
        self.out_msg = ""
        self.s = s

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = json.dumps({"action": "connect", "target": peer})
        mysend(self.s, msg)
        response = json.loads(myrecv(self.s))
        if response["status"] == "success":
            self.peer = peer
            self.out_msg += f"You are connected with {self.peer}" + "\n"
            return True
        elif response["status"] == "busy":
            self.out_msg += "User is busy. Please try again later\n"
        elif response["status"] == "self":
            self.out_msg += "Cannot talk to yourself (sick)\n"
        else:
            self.out_msg += "User is not online, try again later\n"
        return False

    def disconnect(self):
        msg = json.dumps({"action": "disconnect"})
        mysend(self.s, msg)
        self.out_msg += f"You are disconnecte from {self.peer}" + "\n"
        self.peer = ""

    def proc(self, my_msg, peer_msg):
        self.out_msg = ""
        # ==============================================================================
        # Once logged in, do a few things: get peer listing, connect, search
        # And, of course, if you are so bored, just go
        # This is event handling instate "S_LOGGEDIN"
        # ==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == "q":
                    self.state = S_OFFLINE

                elif my_msg == "time":
                    mysend(self.s, json.dumps({"action": "time"}))
                    time_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += f"Time is: {time_in}"

                elif my_msg == "find_friend":
                    mysend(self.s, json.dumps({"action": "find_friends"}))
                    people = json.loads(myrecv(self.s))["results"]
                    print(people)
                    print(type(people))
                    print(self.get_myname())
                    import random

                    if len(people) == 1:
                        self.out_msg += "No one is online, try again later\n"
                    else:
                        while True:
                            person = random.choice(list(people))
                            if person != self.get_myname():
                                break
                        if self.connect_to(person) == True:
                            self.state = S_CHATTING
                            self.out_msg += f"Connect to {person}" + ". Chat away!\n\n"
                            self.out_msg += "-----------------------------------\n"
                        else:
                            self.out_msg += "Connection unsuccessful\n"

                elif my_msg == "who":
                    mysend(self.s, json.dumps({"action": "list"}))
                    logged_in = json.loads(myrecv(self.s))["results"]
                    self.out_msg += "Here are all the users in the system:\n"
                    self.out_msg += logged_in

                elif my_msg[0] == "c":
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += f"Connect to {peer}" + ". Chat away!\n\n"
                        self.out_msg += "-----------------------------------\n"
                    else:
                        self.out_msg += "Connection unsuccessful\n"

                elif my_msg[0] == "?":
                    term = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action": "search", "target": term}))
                    search_rslt = json.loads(myrecv(self.s))["results"].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + "\n\n"
                    else:
                        self.out_msg += "'" + term + "'" + " not found\n\n"

                elif my_msg[0] == "p" and my_msg[1:].isdigit():
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, json.dumps({"action": "poem", "target": poem_idx}))
                    poem = json.loads(myrecv(self.s))["results"]
                    if len(poem) > 0:
                        self.out_msg += poem + "\n\n"
                    else:
                        self.out_msg += f"Sonnet {poem_idx}" + " not found\n\n"

            if len(peer_msg) > 0:
                try:
                    peer_msg = json.loads(peer_msg)
                except Exception as err:
                    self.out_msg += f" json.loads failed {str(err)}"
                    return self.out_msg

                if peer_msg["action"] == "connect":

                    # ----------your code here------#
                    self.peer = peer_msg["from"]
                    self.out_msg += f"Request from {self.peer}" + "\n"
                    self.out_msg += f"You are connected with {self.peer}"
                    self.out_msg += ". Chat away!\n\n"
                    self.out_msg += "------------------------------------\n"
                    self.state = S_CHATTING
                    # ----------end of your code----#

        elif self.state == S_CHATTING:
            if len(my_msg) > 0:  # my stuff going out
                my_message = des().encryption(my_msg)
                mysend(
                    self.s,
                    json.dumps(
                        {
                            "action": "exchange",
                            "from": f"[{self.me}]",
                            "message": my_message,
                        }
                    ),
                )

                if my_msg == "bye":
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ""

            if len(peer_msg) > 0:  # peer's stuff, coming in
                try:
                    peer_msg = json.loads(peer_msg)
                except Exception as err:
                    self.out_msg += f" json.loads failed {str(err)}"
                    return self.out_msg

                if peer_msg["action"] == "disconnect":
                    self.out_msg += peer_msg["msg"] + "\n"
                    self.state = S_LOGGEDIN

                if peer_msg["action"] == "connect":
                    # ----------your code here------#
                    self.peer = peer_msg["from"]
                    self.out_msg += f"({self.peer} joined)"

                if peer_msg["action"] == "exchange":
                    msg = des().decryption(peer_msg["message"])
                    sender = peer_msg["from"]
                    self.out_msg += sender + msg

        else:
            self.out_msg += "How did you wind up here??\n"
            print_state(self.state)

        return self.out_msg
