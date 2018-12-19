#!/usr/bin/python3           # This is python_server1.py file
import socket
import threading
import pickle

from section import generate_rooms
import sql


def main():
    print('start server')

    # create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # get local machine name
    host = socket.gethostname()
    port = 9999

    # bind to the port
    server_socket.bind((host, port))

    # queue up to 5 requests
    server_socket.listen(5)
    print('waiting connection...')

    while True:
        # establish a connection
        client_socket, address = server_socket.accept()
        print("Got a connection from %s" % str(address))

        # threadを設定
        p = threading.Thread(target=work_thread, args=(client_socket,))
        p.start()


def work_thread(client_socket):
    global all_room
    try:
        # ゲームのステージ構成を送信
        client_socket.send(pickle.dumps(generate_rooms()))
        print("send stage")

        room = None;
        client_name = "GuestUser"

        while True:
            receive_msg = client_socket.recv(1024).decode("ascii")
            print("Receive request from ", client_name, ":", receive_msg)

            # ウィンドウが閉じられたときの処理
            if receive_msg == "-10":
                print("-10")
                if room is not None:
                    room.remove_player(client_socket)
                    if len(room.players) == 0:
                        play_rooms.rooms.remove(room)
                    client_socket.send(send_msg.encode("ascii"))
                break

            # ルーム作成者がルームを退出したときの処理
            elif receive_msg == "c_leave_room":
                print("delete_room")
                room.remove_player(client_socket)
                play_rooms.rooms.remove(room)
                client_socket.send("leave_room".encode("ascii"))
                for join_player in room.players:
                    if client_socket is not join_player:
                        join_player.send("room_deleted".encode("ascii"))

            # ルーム作成者がルームを退出したときの処理
            elif receive_msg == "j_leave_room":
                print("leave_room")
                room.remove_player(client_socket)
                client_socket.send("leave_room".encode("ascii"))

            # クライアントからユーザ名を受け取る
            elif receive_msg == "system_start":
                client = pickle.loads(client_socket.recv(4096))
                client_name = client.get_name()
                if client_name == "":
                    client_name = "Guest"
                print("create account:", client.get_name())

            # ルームリストを送信する
            elif receive_msg == "request_RoomList":
                print("request_RoomList")
                client.position = (pickle.loads(client_socket.recv(8192))).position
                req_part = client.position[0]
                req_section = client.position[1]
                req_part_section = client.position[2]

                room = None
                for part in all_room:
                    if req_part.number == part.number:
                        for section in part.sections:
                            if req_section.number == section.number:
                                for part_section in section.word_parts:
                                    if req_part_section.part_name == part_section.part_name:
                                        play_rooms = part_section
                                        print(play_rooms.address)
                                        break

                # ルームリストを送信
                room_list = list()
                for r in play_rooms.rooms:
                    if r.check_vacancy() is True:
                        room_list.append(
                            {"name": r.name, "player_num": str(len(r.players)) + "/" + str(r.max_num), "id": r.hashcode,
                             "reception": r.reception})
                client_socket.send(pickle.dumps(room_list))
                print("send RoomList")

            # ルームに関するリクエストに対応
            elif receive_msg == "request_room":
                print("request_room")
                req_room = pickle.loads(client_socket.recv(4096))
                if req_room[2] is "c":
                    if req_room[0] == "":
                        room = play_rooms.create_room("AnonymousRoom", req_room[1])
                    else:
                        room = play_rooms.create_room(req_room[0], req_room[1])
                    print("create Room")
                    room.add_player(client_socket)
                elif req_room[3] is "j":
                    for r in play_rooms.rooms:
                        print(r.hashcode)
                        if req_room[2] == r.hashcode:
                            room = r
                            room.add_player(client_socket)
                            print(room.name)

            # ステージに適した単語リストを送信する
            elif receive_msg == "request_words":
                print("request_words")
                # 単語関連の設定＆送信
                words = sql_session.query(sql.Word). \
                    filter(sql.Word.part == req_part.number). \
                    filter(sql.Word.section == req_section.number). \
                    filter(sql.Word.part_section == req_part_section.part_name). \
                    all()

                for word in words:
                    print(word.english)
                client_socket.send(pickle.dumps(words))
                print("send words")

                send_msg = "You entered in Room: " + room.name
                client_socket.send(send_msg.encode("ascii"))

            # ゲームの開始
            elif receive_msg == "game_start":
                print("game_start")
                for player in room.players:
                    player.send("correct_answer".encode("ascii"))
                    room.reception = False

            # 受け取った回答が正解か判定
            elif receive_msg == "answer":
                print("answer")
                receive_msg = client_socket.recv(1024).decode("ascii")
                send_msg = client.get_name() + ": " + receive_msg

                for player in room.players:
                    player.send(send_msg.encode('ascii'))
                    if receive_msg == words[room.index].english:
                        if room.index + 1 == len(words):
                            player.send("game_finish".encode("ascii"))
                        else:
                            player.send("correct_answer".encode("ascii"))
                if receive_msg == words[room.index].english:
                    room.index += 1

    finally:
        client_socket.close()
        print("disconnection")


if __name__ == '__main__':
    all_room = generate_rooms()
    sql_session = sql.get_session()
    # sql.add_words()
    main()
