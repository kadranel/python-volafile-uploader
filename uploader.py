from volapi import Room
import argparse
import config
import os
import requests


def upload_process(room, passwd, user, userpasswd, files):
    if len(files) == 0:
        print("[X] No files were recognised! - Aborting upload")
        return False
    if room == "":
        print(f"[X] You must provide a room! - Aborting upload!")
        return False
    if user == "" and config.VOLAFILE_USER == "":
        local_user = "volapi"
        upw_set = False
    elif user == "" and config.VOLAFILE_USER != "":
        local_user = config.VOLAFILE_USER
        if config.VOLAFILE_USER_PASSWORD != "":
            local_password = config.VOLAFILE_USER_PASSWORD
            upw_set = True
        else:
            upw_set = False
    else:
        local_user = user
        if userpasswd != "":
            local_password = userpasswd
            upw_set = True
        else:
            upw_set = False

    if passwd == "":
        rpw_set = False
    else:
        rpw_set = True

    try:
        if rpw_set and passwd[0:4] == "#key":
            local_room = Room(name=room, key=passwd[4:], user=local_user)
        elif rpw_set:
            local_room = Room(name=room, password=passwd, user=local_user)
        else:
            local_room = Room(name=room, user=local_user)
    except RuntimeError:
        print(
            f"[X] Could not connect to the specified room: {room} - Aborting upload.")
        return False

    if upw_set:
        try:
            local_room.user.login(local_password)
        except RuntimeError:
            print(
                f"[X] Could not login user: {local_user} with the provided password - Aborting upload."
            )
            return False
    filenum = 0
    for f in files:
        if os.path.isfile(f):
            filenum += 1
            handle_file(f, local_room, filenum)
        elif os.path.isdir(f):
            for filename in os.listdir(f):
                if os.path.isfile(os.path.join(f, filename)):
                    filenum += 1
                    handle_file(os.path.join(f, filename), local_room, filenum)
                else:
                    print(
                        f"[X] Subfolders are not handled, please specify seperately: {f} -  Continue to next specified file"
                    )

        else:
            print(
                f"[X] File/Folder could not be recognised: {f} -  Continue to next specified file/folder"
            )
            continue
    local_room.close()


def handle_file(file, room, filenum):
    callback = CallbackInfo(file.split("/")[-1], filenum, room)
    try:
        file_id = room.upload_file(file, callback=callback, allow_timeout=True)
    except ValueError:
        print(
            f"[{filenum}] Uploading to {room.name} | ERROR: File was too big to upload!",
            end="\r",
        )
    except requests.exceptions.ConnectionError:
        print(
            f"[{filenum}] Uploading to {room.name} | ERROR: Connection timed out!",
            end="\r",
        )
    except ConnectionError:
        print(
            f"[{filenum}] Uploading to {room.name} | ERROR: Connection timed out!",
            end="\r",
        )
    if file_id:
        print("")
        print(
            f"[{filenum}] {file.split('/')[-1]} uploaded to https://volafile.org/get/{file_id}/"
        )
    else:
        print("")


class CallbackInfo:
    def __init__(self, name, num, room):
        self.name = name
        self.num = num
        self.room = room.name

    def __call__(self, current, total):
        print(
            f"[{self.num}] Uploading to {self.room} | {self.name} -> {current / (1024 * 1024.0):.2f}MB/{total / (1024 * 1024.0):.2f}MB -> {float(current) / total:.2%} completed!",
            end="\r",
        )


def parse_args():
    """Parses user arguments"""
    parser = argparse.ArgumentParser(description="volafile uploader")
    parser.add_argument(
        "--room",
        "-r",
        dest="room",
        type=str,
        required=True,
        help="Room name, as in https://volafile.org/r/ROOMNAME",
    )
    parser.add_argument(
        "--passwd",
        "-p",
        dest="passwd",
        type=str,
        default="",
        help="Room password to enter the room",
    )
    parser.add_argument(
        "--user",
        "-u",
        dest="user",
        type=str,
        default="",
        help="Overwrite for VOLAFILE_USER in config.py",
    )
    parser.add_argument(
        "--userpasswd",
        "-up",
        dest="userpasswd",
        type=str,
        default="",
        help="Overwrite for VOLAFILE_USER_PASSWORD in config.py",
    )
    parser.add_argument(
        "-f",
        "--files",
        metavar="FILE",
        type=str,
        nargs="+",
        help="Files/folders to upload",
    )
    return parser.parse_args()


def main():
    """Main method"""
    args = parse_args()
    upload_process(args.room, args.passwd, args.user,
                   args.userpasswd, args.files)


if __name__ == "__main__":
    main()
