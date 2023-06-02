import os
import secrets
import sqlite3
from os import mkdir
from os.path import exists
from datetime import datetime
from passlib.hash import sha256_crypt
from flask import render_template, Blueprint
from forms import (
    loginForm,
    signUpForm,
    commentForm,
    createPostForm,
    changePasswordForm,
    changeUserNameForm,
)

from aitextgen import aitextgen
from pytrends.request import TrendReq
import pandas

from flask import (
    request,
    session,
    flash,
    redirect,
    render_template,
    send_from_directory,
    Flask,
    Blueprint,
)

def currentDate():
    return datetime.now().strftime("%d.%m.%y")


def currentTime(seconds=False):
    match seconds:
        case False:
            return datetime.now().strftime("%H:%M")
        case True:
            return datetime.now().strftime("%H:%M:%S")


def message(color, message):
    print(
        f"\n\033[94m[{currentDate()}\033[0m"
        f"\033[95m {currentTime(True)}]\033[0m"
        f"\033[9{color}m {message}\033[0m\n"
    )
    logFile = open("log.log", "a")
    logFile.write(f"[{currentDate()}" f"|{currentTime(True)}]" f" {message}\n")
    logFile.close()


def addPoints(points, user):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'update users set points = points+{points} where userName = "{user}"'
    )
    connection.commit()
    message("2", f'{points} POINTS ADDED TO "{user}"')

def getProfilePicture(userName):
    connection = sqlite3.connect("db/users.db")
    cursor = connection.cursor()
    cursor.execute(
        f'select profilePicture from users where lower(userName) = "{userName.lower()}"'
    )
    return cursor.fetchone()[0]

def get_trending_title():
    pytrends = TrendReq(hl='en-US', tz=360)
    India = pytrends.realtime_trending_searches(pn='IN')
    india_df = pandas.DataFrame(India)
    india_df_split = india_df.loc[0].title
    india_df_splitted = india_df_split.split(",")
    trending_title = india_df_splitted[0].strip()

    return trending_title

def ai_text(title, max_length=1500):
    ai_text_init = aitextgen(model="EleutherAI/gpt-neo-125M", to_gpu=False)
    generate_text = ai_text_init.generate_one(
        max_length=max_length,
        prompt=title,
        no_repeat_ngram_size=3
    )
    return generate_text


def addPoints():
    pass