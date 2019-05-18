#!/usr/bin/python3
import json
from os import path, system, makedirs, sep, chdir
from time import sleep
import random
import argparse

import git

parser = argparse.ArgumentParser()

parser.add_argument("words")
parser.add_argument("-w" "--wait", type=int)

args = parser.parse_args()

split_file_name = args.words.split(".")

if ".json" != split_file_name[-1]:
    split_file_name.append(".json")

if args.wait:
    wait_time = args.wait

save_file = ".".join(split_file_name)

data_folder = "wordtester"

if not path.exists(data_folder):
    makedirs(data_folder)
chdir(data_folder)

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
