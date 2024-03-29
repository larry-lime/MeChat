# Local imports
from chat_utils import *
import chat_group as grp
import indexer

# Module imports
import time
import socket
import select
import json
import pickle as pkl

# ==============================================================================
class Server:
    def __init__(self):
        self.new_clients = []  # list of new sockets of which the user id is not known
        self.logged_name2sock = {}  # dictionary mapping username to socket
        self.logged_sock2name = {}  # dict mapping socket to user name
        self.all_sockets = []
        self.group = grp.Group()
        # start server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(SERVER)
        self.server.listen(100)
        # self.server.listen(5)
        self.all_sockets.append(self.server)
        # initialize past chat indices
        self.indices = {}
        # sonnet
        self.sonnet = indexer.PIndex("AllSonnets.txt")

    def new_client(self, sock):
        print("new client...")
        sock.setblocking(0)
        self.new_clients.append(sock)
        self.all_sockets.append(sock)

    def login(self, sock):
        try:
            msg = json.loads(myrecv(sock))
            if len(msg) > 0:
                if msg["action"] == "login":
                    # Add the username and password to user_and_pass
                    user_and_pass, name, password = self.get_username_and_passwords(
                        msg)
                    self.validate_user(user_and_pass, name, password, sock)
                else:
                    print("wrong code received")
            else:  # client died unexpectedly
                self.logout(sock)

        except Exception:
            self.all_sockets.remove(sock)

    def validate_user(self, user_and_pass, name, password, sock):
        if name not in user_and_pass.keys():
            # Save the username and password to the file
            user_and_pass[name] = password
            pkl.dump(user_and_pass, open("username_and_passwords.pk", "wb"))
            user_and_pass = pkl.load(open("username_and_passwords.pk", "rb"))
            # Check for duplicate username
            self.check_duplicate_user(name, sock)

        elif user_and_pass[name] == password:
            # Check for duplicate username
            self.check_duplicate_user(name, sock)

        else:
            mysend(sock, json.dumps({"action": "login", "status": "wrong"}))
            print(f"{name}bad login attempt")

    def check_duplicate_user(self, name, sock):
        if self.group.is_member(name) != True:
            self.successful_login(sock, name)
        else:  # a client under this name has already logged in
            mysend(sock, json.dumps(
                {"action": "login", "status": "duplicate"}))
            print(f"{name} duplicate login attempt")

    def get_username_and_passwords(self, msg):
        name = msg["name"]
        password = msg["password"]
        try:
            user_and_pass = pkl.load(open("username_and_passwords.pk", "rb"))
        except Exception:
            user_and_pass = {}
        return user_and_pass, name, password

    def successful_login(self, sock, name):
        self.new_clients.remove(sock)
        self.logged_name2sock[name] = sock
        self.logged_sock2name[sock] = name
        if name not in self.indices.keys():
            try:
                self.indices[name] = pkl.load(open(f"{name}.idx", "rb"))
            except IOError:
                self.indices[name] = indexer.Index(name)
        print(f"{name} logged in")
        self.group.join(name)
        mysend(sock, json.dumps({"action": "login", "status": "ok"}))

    def logout(self, sock):
        # remove sock from all lists
        name = self.logged_sock2name[sock]
        pkl.dump(self.indices[name], open(f"{name}.idx", "wb"))
        del self.indices[name]
        del self.logged_name2sock[name]
        del self.logged_sock2name[sock]
        self.all_sockets.remove(sock)
        sock.close()
        self.group.leave(name)

    # ==============================================================================
    # main command switchboard
    # ==============================================================================
    def handle_msg(self, from_sock):
        # read msg code
        msg = myrecv(from_sock)
        if len(msg) > 0:
            msg = json.loads(msg)
            if msg["action"] == "connect":
                to_name = msg["target"]
                from_name = self.logged_sock2name[from_sock]
                if to_name == from_name:
                    msg = json.dumps({"action": "connect", "status": "self"})
                # connect to the peer
                elif self.group.is_member(to_name):
                    to_sock = self.logged_name2sock[to_name]
                    self.group.connect(from_name, to_name)
                    the_guys = self.group.list_me(from_name)
                    msg = json.dumps(
                        {"action": "connect", "status": "success"})
                    for g in the_guys[1:]:
                        to_sock = self.logged_name2sock[g]
                        mysend(
                            to_sock,
                            json.dumps(
                                {
                                    "action": "connect",
                                    "status": "request",
                                    "from": from_name,
                                }
                            ),
                        )
                else:
                    msg = json.dumps(
                        {"action": "connect", "status": "no-user"})
                mysend(from_sock, msg)

            elif msg["action"] == "exchange":
                self.send_message(from_sock, msg)

            elif msg["action"] == "disconnect":
                from_name = self.logged_sock2name[from_sock]
                the_guys = self.group.list_me(from_name)
                self.group.disconnect(from_name)
                the_guys.remove(from_name)
                if len(the_guys) == 1:  # only one left
                    g = the_guys.pop()
                    to_sock = self.logged_name2sock[g]
                    mysend(
                        to_sock,
                        json.dumps(
                            {
                                "action": "disconnect",
                                "msg": "everyone left, you are alone",
                            }
                        ),
                    )

            elif msg["action"] == "find_friends":
                g = self.group
                people = g.list_ppl()
                mysend(from_sock, json.dumps(
                    {"action": "list", "results": people}))

            elif msg["action"] == "list":
                g = self.group
                msg = g.list_all()
                mysend(from_sock, json.dumps(
                    {"action": "list", "results": msg}))

            elif msg["action"] == "poem":
                index = int(msg["target"])
                poem = "".join(i + "\n" for i in self.sonnet.get_poem(index))
                poem = poem.strip()
                mysend(from_sock, json.dumps(
                    {"action": "poem", "results": poem}))

            elif msg["action"] == "send_key":
                key = msg["key"]
                print("TEST:", key)
                mysend(from_sock, json.dumps(
                    {"action": "send_key", "key": key}))

            elif msg["action"] == "time":
                # This is the actual time
                ctime = time.strftime("%d.%m.%y,%H:%M", time.localtime())
                # What mysend is is what is being sent from the sever to the client
                mysend(from_sock, json.dumps(
                    {"action": "time", "results": ctime}))
            elif msg["action"] == "search":

                self.message_search(msg, from_sock)
        else:
            # client died unexpectedly
            self.logout(from_sock)

    def message_search(self, msg, from_sock):
        result = []
        word = msg["target"]
        print(self.indices)
        for i in self.indices.keys():
            k = self.indices[i].index.keys()
            if word in k:
                result.extend(
                    (i, self.indices[i].msgs[j]) for j in self.indices[i].index[word]
                )

        search_rslt = "".join(str(l) + "\n" for l in result)
        print("search_rslt:\n", search_rslt)
        mysend(from_sock, json.dumps(
            {"action": "search", "results": search_rslt}))

    def send_message(self, from_sock, msg):
        from_name = self.logged_sock2name[from_sock]
        """
        Finding the list of people to send to and index message
        """
        my_msg = msg["message"]
        self.indices[from_name].add_msg_and_index(my_msg)
        the_guys = self.group.list_me(from_name)[1:]
        for g in the_guys:
            to_sock = self.logged_name2sock[g]
            mysend(
                to_sock,
                json.dumps(
                    {"action": "exchange",
                        "from": f"[{from_name}]", "message": my_msg}
                ),
            )

    # ==============================================================================
    # main loop, loops *forever*
    # ==============================================================================
    def run(self):
        print("starting server...")
        while 1:
            read, write, error = select.select(self.all_sockets, [], [])
            print("checking logged clients..")
            for logc in list(self.logged_name2sock.values()):
                if logc in read:
                    self.handle_msg(logc)
            print("checking new clients..")
            for newc in self.new_clients[:]:
                if newc in read:
                    self.login(newc)
            print("checking for new connections..")
            if self.server in read:
                # new client request
                sock, address = self.server.accept()
                self.new_client(sock)


def main():
    server = Server()
    server.run()


if __name__ == "__main__":
    main()
