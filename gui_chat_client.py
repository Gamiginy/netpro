#!/usr/bin/python3           # This is python_client1.py file

import socket
import threading
from time import sleep
import pickle
import tkinter as tk
from tkinter import messagebox
import re
import random

from client import Client


# -------------------------------------------------------------------------------------------------------- #
# 通信

# メッセージを送信
def send_message(msg):
    soc.send(msg.encode("ascii"))


# オブジェクトを送信
def send_object(obj):
    soc.send(pickle.dumps(obj))


# メッセージを受信
def receive_message():
    msg = soc.recv(1024).decode("ascii")
    return msg


# オブジェクトを受信
def receive_object():
    obj = pickle.loads(soc.recv(16384))
    return obj


# ------------------------------------------------------------------------------------------------------- #
# GUI

def start_window():
    print("start window")

    def start_game():
        name = name_form.get()
        if name == "":
            name = "GuestUser" + str(random.randint(0, 100001))
        client.set_name(name)
        send_message("system_start")
        send_object(client)

        main_frame.destroy()
        part_window()

    main_frame = tk.Frame(root)
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    label1 = tk.Label(main_frame, text="ゲーム内で表示されるユーザ名を入力してください。")
    label2 = tk.Label(main_frame, text="name")
    label1.pack()
    label2.place(relx=0.39, rely=0.39)
    name_form = tk.Entry(main_frame)
    name_form.place(relx=0.39, rely=0.43, relwidth=0.25, relheight=0.05)

    sign_in_btn = tk.Button(main_frame, text="start", command=start_game)
    sign_in_btn.place(relx=0.48, rely=0.5, relwidth=0.07, relheight=0.05)


def part_window():
    def select_room(part):
        client.enter(part)
        print(part.number)
        main_frame.destroy()
        section_window(part)

    def back():
        start_window()

    main_frame = tk.Frame(root)
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    label1 = tk.Label(main_frame, text="Partを選択してください。")
    label1.pack()

    button1 = tk.Button(main_frame, text="Part" + str(rooms[0].number), command=lambda: select_room(rooms[0]))
    button2 = tk.Button(main_frame, text="Part" + str(rooms[1].number), command=lambda: select_room(rooms[1]))
    button3 = tk.Button(main_frame, text="Part" + str(rooms[2].number), command=lambda: select_room(rooms[2]))

    button1.place(relx=0.05, rely=0.2, relwidth=0.3, relheight=0.5)
    button2.place(relx=0.35, rely=0.2, relwidth=0.3, relheight=0.5)
    button3.place(relx=0.65, rely=0.2, relwidth=0.3, relheight=0.5)

    back_button = tk.Button(main_frame, text="戻る", command=back)
    back_button.place(relx=0.95, rely=0.95, relwidth=0.05, relheight=0.05)


def section_window(part):
    def select_room(section):
        main_frame.destroy()
        client.enter(section)
        print(section.number)
        part_section_window(section)

    def back():
        client.leave()
        part_window()

    main_frame = tk.Frame(root)
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    label1 = tk.Label(main_frame, text="Sectionを選択してください。")
    label1.pack()

    button1 = tk.Button(main_frame, text="Section" + str(part.sections[0].number),
                        command=lambda: select_room(part.sections[0]))
    button1.place(relx=0.04, rely=0.05, relwidth=0.23, relheight=0.3)
    button2 = tk.Button(main_frame, text="Section" + str(part.sections[1].number),
                        command=lambda: select_room(part.sections[1]))
    button2.place(relx=0.27, rely=0.05, relwidth=0.23, relheight=0.3)
    button3 = tk.Button(main_frame, text="Section" + str(part.sections[2].number),
                        command=lambda: select_room(part.sections[2]))
    button3.place(relx=0.5, rely=0.05, relwidth=0.23, relheight=0.3)
    button4 = tk.Button(main_frame, text="Section" + str(part.sections[3].number),
                        command=lambda: select_room(part.sections[3]))
    button4.place(relx=0.73, rely=0.05, relwidth=0.23, relheight=0.3)

    if len(part.sections) > 4:
        button5 = tk.Button(main_frame, text="Section" + str(part.sections[4].number),
                            command=lambda: select_room(part.sections[4]))
        button5.place(relx=0.04, rely=0.35, relwidth=0.23, relheight=0.3)
        button6 = tk.Button(main_frame, text="Section" + str(part.sections[5].number),
                            command=lambda: select_room(part.sections[5]))
        button6.place(relx=0.27, rely=0.35, relwidth=0.23, relheight=0.3)
        button7 = tk.Button(main_frame, text="Section" + str(part.sections[6].number),
                            command=lambda: select_room(part.sections[6]))
        button7.place(relx=0.5, rely=0.35, relwidth=0.23, relheight=0.3)
        button8 = tk.Button(main_frame, text="Section" + str(part.sections[7].number),
                            command=lambda: select_room(part.sections[7]))
        button8.place(relx=0.73, rely=0.35, relwidth=0.23, relheight=0.3)
        if len(part.sections) > 8:
            button9 = tk.Button(main_frame, text="Section" + str(part.sections[8].number),
                                command=lambda: select_room(part.sections[8]))
            button9.place(relx=0.04, rely=0.65, relwidth=0.23, relheight=0.3)

        back_button = tk.Button(main_frame, text="戻る", command=back)
        back_button.place(relx=0.95, rely=0.95, relwidth=0.05, relheight=0.05)


def part_section_window(section):
    def select_room(part_section):
        main_frame.destroy()
        client.enter(part_section)
        print(part_section.part_name)
        room_select_window(part_section)

    def back():
        section_window(client.leave())

    main_frame = tk.Frame(root)
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    label1 = tk.Label(main_frame, text="品詞を選択してください")
    label1.pack()

    button1 = tk.Button(main_frame, text=section.word_parts[0].part_name,
                        command=lambda: select_room(section.word_parts[0]))
    button1.place(relx=0.04, rely=0.05, relwidth=0.23, relheight=0.45)
    button2 = tk.Button(main_frame, text=section.word_parts[1].part_name,
                        command=lambda: select_room(section.word_parts[1]))
    button2.place(relx=0.27, rely=0.05, relwidth=0.23, relheight=0.45)
    button3 = tk.Button(main_frame, text=section.word_parts[2].part_name,
                        command=lambda: select_room(section.word_parts[2]))
    button3.place(relx=0.5, rely=0.05, relwidth=0.23, relheight=0.45)
    button4 = tk.Button(main_frame, text=section.word_parts[3].part_name,
                        command=lambda: select_room(section.word_parts[3]))
    button4.place(relx=0.73, rely=0.05, relwidth=0.23, relheight=0.45)
    if len(section.word_parts) > 4:
        button5 = tk.Button(main_frame, text=section.word_parts[4].part_name,
                            command=lambda: select_room(section.word_parts[4]))
        button5.place(relx=0.04, rely=0.5, relwidth=0.23, relheight=0.45)

    back_button = tk.Button(main_frame, text="戻る", command=back)
    back_button.place(relx=0.95, rely=0.95, relwidth=0.05, relheight=0.05)


def room_select_window(part_section):
    def create_room():
        main_frame.destroy()
        create_room_window()

    def join_room():
        send_message("request_room")
        for i in room_listbox.curselection():
            msg = room_listbox.get(i)
            join_room_info = re.findall("(?<=ルーム名:).*(?=,　制限人数:)|(?<=制限人数:).*(?=,　ルームID:)|(?<=ルームID:).*$", msg)
            join_room_info.append("j")
            send_object(join_room_info)
        main_frame.destroy()
        play_window("j")

    def back():
        part_section_window(client.leave())

    send_message("request_RoomList")
    # クライアント情報をサーバに送信
    send_object(client)
    # ルームリストを受信
    room_list = receive_object()

    main_frame = tk.Frame(root)
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    label1 = tk.Label(main_frame, text="ルームリスト")
    label2 = tk.Label(main_frame, text="※左のリストからルームを選択してから参加ボタンを押してください。", font=("", 6))
    label1.place(relx=0.05, rely=0.01)
    label2.place(relx=0.66, rely=0.7)

    room_list_frame = tk.Frame(main_frame)
    room_list_frame.place(relx=0.05, rely=0.05, relwidth=0.51, relheight=0.9)
    room_listbox = tk.Listbox(room_list_frame)
    for room in room_list:
        if room["reception"] is True:
            room_listbox.insert(0,
                                "ルーム名:" + room["name"] + ",　制限人数:" + room["player_num"] + ",　ルームID:" + room["id"])
    room_listbox.place(relx=0, rely=0, relwidth=1, relheight=1)
    scroll_bar = tk.Scrollbar(room_list_frame, command=room_listbox.yview)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    room_listbox.config(yscrollcommand=scroll_bar.set)

    create_room_button = tk.Button(main_frame, text="ルーム作成", command=create_room)
    join_room_button = tk.Button(main_frame, text="参加する", command=join_room)
    back_button = tk.Button(main_frame, text="戻る", command=back)
    create_room_button.place(relx=0.66, rely=0.3, relwidth=0.24, relheight=0.1)
    join_room_button.place(relx=0.66, rely=0.6, relwidth=0.24, relheight=0.1)
    back_button.place(relx=0.95, rely=0.95, relwidth=0.05, relheight=0.05)


def create_room_window():
    def create_room():
        room_name = room_name_form.get()
        room_max = room_maxnum_form.get()
        if room_name == "":
            room_name = "AnonymousRoom" + str(random.randint(0, 100001))
        if room_max == "":
            room_max = "4"
        if int(room_max) > 4:
            room_max = "4"
        create_room_info = (room_name, room_max, "c")
        send_message("request_room")
        send_object(create_room_info)
        main_frame.destroy()
        play_window("c")

    main_frame = tk.Frame(root)
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    label1 = tk.Label(main_frame, text="Room Name")
    label2 = tk.Label(main_frame, text="制限人数")
    label1.place(relx=0.4, rely=0.25)
    label2.place(relx=0.4, rely=0.45)

    room_name_form = tk.Entry(main_frame)
    room_maxnum_form = tk.Entry(main_frame)
    room_name_form.place(relx=0.4, rely=0.3, relwidth=0.2, relheight=0.05)
    room_maxnum_form.place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.05)

    create_button = tk.Button(main_frame, text="作成", command=create_room)
    create_button.place(relx=0.45, rely=0.6, relwidth=0.1, relheight=0.08)


def play_window(permission):
    def send_btn():
        send_message("answer")
        send_message(msg_form.get())
        msg_form.delete(0, tk.END)

    def back_btn():
        if permission == "c":
            send_message("c_leave_room")
        else:
            send_message("j_leave_room")
        main_frame.destroy()
        room_select_window(client.position[2])

    def send_entry(event):
        send_message("answer")
        send_message(msg_form.get())
        msg_form.delete(0, tk.END)

    def display_msg():
        index = 0
        while reception is True:
            msg = receive_message()
            print(msg)
            if msg == "correct_answer":
                display_word(index)
                index += 1
                sleep(1)
                display_score()
                sleep(1)
                print("getScoreList")
            elif msg == "leave_room":
                break
            elif msg == "game_finish":
                display_score()
                sleep(1)
                end_frame = tk.Frame(main_frame)
                end_frame.place(relx=0, rely=0.1, relwidth=0.8, relheight=0.9)
                end_msg = tk.Label(end_frame, text="ゲームが終了しました。戻るボタンを押してルームリストに戻ってください。")
                end_msg.place(relx=0.3, rely=0.4)
            elif msg == "room_deleted":
                deleted_label = tk.Label(main_frame, text="この部屋は作成者によって削除されました。戻るボタンから退出してください。")
                deleted_label.place(relx=0.3, rely=0.3)
                message_list_frame.destroy()
                msg_form.destroy()
                send_button.destroy()
            else:
                message_list.insert(0, msg)
                sleep(1)

    def display_word(index):
        word_frame = tk.Frame(main_frame)
        word_frame.place(relx=0, rely=0, relwidth=0.8, relheight=1)

        word = words[index]
        word_label = tk.Label(word_frame, text=word.japanese, font=("", int(300 / len(word.japanese))))
        word_label.pack(expand=1, fill=tk.BOTH)

    def display_score():
        score = receive_object()

        score_list = ""
        rank = 1
        for k, v in score.items():
            score_list += str(rank) + "位:" + k + "," + str(v) + "p ; "
            rank += 1
        score_label = tk.Label(main_frame, text=score_list)
        score_label.place(relx=0, rely=0)

    main_frame = tk.Frame(root)
    main_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    # メッセージリスト(frame, listbox, scrollbar)の設定
    message_list_frame = tk.Frame(main_frame)
    message_list_frame.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.9)
    message_list = tk.Listbox(message_list_frame)
    message_list.place(relx=0, rely=0, relwidth=1, relheight=1)
    scroll_bar = tk.Scrollbar(message_list_frame, command=message_list.yview)
    scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
    message_list.config(yscrollcommand=scroll_bar.set)

    # 単語リストを受信
    send_message("request_words")
    words = receive_object()
    print("receive words")

    # メッセージ入力欄の設定
    msg_form = tk.Entry(main_frame, width=30)
    msg_form.place(relx=0.8, rely=0.9, relwidth=0.15, relheight=0.05)
    msg_form.bind("<Return>", send_entry)

    # sendボタンの設定
    send_button = tk.Button(main_frame, text="send", command=lambda: send_btn())
    send_button.place(relx=0.95, rely=0.9, relwidth=0.05, relheight=0.05)

    back_button = tk.Button(main_frame, text="戻る", command=lambda: back_btn())
    back_button.place(relx=0.95, rely=0.95, relwidth=0.05, relheight=0.05)

    if permission is "c":
        label1 = tk.Label(main_frame, text="ゲームを開始する場合は「Start」を押してください。", font=("", 20))
        label1.place(relx=0, rely=0)

        button2 = tk.Button(main_frame, text="Start", command=lambda: send_message("game_start"))
        button2.place(relx=0.3, rely=0.4, relwidth=0.3, relheight=0.2)

    if permission is "j":
        label1 = tk.Label(main_frame, text="部屋作成者によってゲームが開始されるまで待機してください。", font=("", 15))
        label1.place(relx=0, rely=0)

    # メッセージ受信用のスレッドを起動
    p = threading.Thread(target=display_msg)
    p.start()


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        msg = "-10"
        send_message(msg)

        root.destroy()


# ----------------------------------------------------------------------------------------------------------- #
# Main

# create a socket object
soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# get local machine name
host = socket.gethostname()
port = 9999

print('start client')
# connection to hostname on the port.
soc.connect((host, port))
client = Client()
rooms = receive_object()

reception = True

root = tk.Tk()
root.title("Room")
root.geometry("800x500")
root.protocol("WM_DELETE_WINDOW", on_closing)

start_window()
root.mainloop()

reception = False
soc.close()
print("disconnection")
