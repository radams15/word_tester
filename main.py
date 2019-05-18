#!/usr/bin/python3
import json
from os import path, system, makedirs, chdir, execv, rename, remove
from shutil import move, rmtree
from time import sleep
import random
import argparse
import glob
import urllib.request
from sys import argv

github_repo = "git://github.com/radams15/word_tester.git"

def internet_connected():
    try:
        urllib.request.urlopen("https://www.google.co.uk", timeout=1)
        return True
    except urllib.request.URLError:
        return False

def needs_updating():
    if not internet_connected():
        return False
    else:
        """TODO"""
        return True

def update():
    import git

    if not path.exists("./.download"):
        makedirs("./.download")
    rename(path.basename(__file__), ".old_main.py")
    git.Repo.clone_from(github_repo, "./.download")

    for file in glob.glob("./.download/*.py"):
        move(file, f"./{path.basename(file)}")

    remove(".old_main.py")

    rmtree("./.download/")


def clear():
    system("clear")

clear()

def get_words_from_file(file_name):
    if not path.exists(file_name):
        open(file_name, "w").close()

    try:
        raw = open(file_name, "r").read()
        return json.loads(raw)
    except json.decoder.JSONDecodeError:
        print("Words File Empty")
        exit()

if __name__ == "__main__":
    if needs_updating():
        update()
        execv(path.basename(__file__), argv.append("--noupdate"))
        exit()

    parser = argparse.ArgumentParser()

    parser.add_argument("words")
    parser.add_argument("-u", "--noupdate", action='store_true')
    parser.add_argument("-w" "--wait", type=float, dest="wait")

    args = parser.parse_args()

    wait_time = 2
    if args.wait:
        wait_time = args.wait

    split_file_name = args.words.split(".")

    if "json" != split_file_name[-1]:
        split_file_name.append("json")

    save_file = ".".join(split_file_name)

    data_folder = "wordtester"

    if not path.exists(data_folder):
        makedirs(data_folder)
    chdir(data_folder)

    words = get_words_from_file(save_file)
    while True:
        prompt = random.choice(list(words.keys()))
        answer = words[prompt]
        print(prompt)
        response = input(">> ")
        if response.lower() == answer.lower():
            print("Correct!")
        else:
            print("Wrong!\n{} means {}".format(prompt, answer))
        sleep(wait_time)
        clear()
