import random
from datetime import date, datetime
from pathlib import Path

import requests
import toml
import wikipedia
from flask import Flask, render_template, request

version = "0.0.1"
app = Flask(__name__)
app.config.from_object("pybot.config")
data = toml.load(str(Path(__file__).parent / "data.toml"))
command_funcs = []


def command_func(func):
    command_funcs.append(func)
    return func


def main():
    app.run(app.config.get("HOST"), app.config.get("PORT"), use_reloader=True)


@app.route("/", methods=["GET", "POST"])
def index():
    command = "ヘルプ"
    message = "コマンドヲ入力シテクダサイ"
    if request.method == "POST":
        command = request.form.get("command", "")
        message = bot(command)
    return render_template("index.html", command=command, message=message)


def bot(command):
    if "ヘルプ" in command:
        lst = [f"<li>{func.__doc__}</li>" for func in command_funcs]
        return f"使い方<br><ul>{''.join(lst)}</ul>"
    inst, args = (command + " ").split(" ", maxsplit=1)
    args = args.rstrip()
    for func in command_funcs:
        if message := func(command=command, inst=inst, args=args):
            return message
    return "ヨク、ワカラナイ"


@command_func
def greeting_command(*, command, **_):
    for k, v in data["greeting"].items():
        if k in command:
            return v
    return None


greeting_command.__doc__ = f"""挨拶コマンド: {'、'.join(data['greeting'])}"""


@command_func
def length_command(*, inst, args, **_):
    """長さコマンド: 長さ [文字列]"""
    if "長さ" != inst:
        return None
    return f"長さハ、{len(args)}文字デス"


@command_func
def wareki_command(*, inst, args, **_):
    """和暦コマンド: 和暦 [西暦の年]"""
    if inst != "和暦":
        return None
    try:
        year = int(args)
        for k, v in data["wareki"].items():
            if year >= v:
                return f"西暦{year}年ハ、{k}{year - v + 1}年デス"
        return f"西暦{year}年ハ、{k}ヨリ前デス"
    except ValueError:
        return f'"{wareki_command.__doc__}" ダヨ'


@command_func
def eto_command(*, inst, args, **_):
    """干支コマンド: 干支 [西暦の年]"""
    if inst != "干支":
        return None
    try:
        year = int(args)
        val = "子丑寅卯辰巳午未申酉戌亥"[(year + 8) % 12]
        return f"{year}年生マレノ干支ハ、「{val}」デス"
    except ValueError:
        return f'"{eto_command.__doc__}" ダヨ'


@command_func
def choice_command(*, inst, args, **_):
    """選ぶコマンド: 選ぶ … … …"""
    if inst != "選ぶ":
        return None
    val = random.choice(args.split(" "))
    return f"「{val}」ガ選バレマシタ"


@command_func
def dice_command(*, inst, **_):
    """さいころコマンド: さいころ"""
    if inst != "さいころ":
        return None
    val = random.randint(1, 6)
    return f"「{val}」ガ出マシタ"


@command_func
def today_command(*, inst, **_):
    """今日コマンド: 今日"""
    if inst != "今日":
        return None
    val = date.today()
    return f"今日ノ日付ハ {val}デス"


@command_func
def now_command(*, inst, **_):
    """現在コマンド: 現在"""
    if inst != "現在":
        return None
    val = datetime.now().replace(microsecond=0)
    return f"現在ノ時刻ハ {val}デス"


@command_func
def weekday_command(*, inst, args, **_):
    """曜日コマンド: 曜日 [yyyy-mm-dd]"""
    if inst != "曜日":
        return None
    try:
        val = date.fromisoformat(args)
        return f"{val}ハ、{'月火水木金土日'[val.weekday()]}曜日デス"
    except ValueError:
        return f'"{weekday_command.__doc__}" ダヨ'


@command_func
def weather_command(*, inst, args, **_):
    if inst != "天気":
        return None
    try:
        city = data["weather"]["code"][args]
        val = requests.get(f"{data['weather']['url1']}?city={city}").json()
        label = val["forecasts"][0]["dateLabel"]
        telop = val["forecasts"][0]["telop"]
        return f"{args}ノ{label}ノ天気ハ「{telop}」デス"
    except KeyError:
        return f'"{weather_command.__doc__}" ダヨ'


weather_command.__doc__ = (
    f'天気コマンド: 天気 [{"|".join(data["weather"]["code"])}] '
    f'(<a href="{data["weather"]["url2"]}" target="_blank">都市</a>)'
)


@command_func
def wikipedia_command(*, inst, args, **_):
    """事典コマンド: 事典 [キーワード]"""
    if inst != "事典":
        return None
    try:
        wikipedia.set_lang("ja")
        page = wikipedia.page(args)
        title = page.title
        summary = page.summary
        return f"タイトル: {title}<br>{summary}"
    except wikipedia.exceptions.WikipediaException:
        return f'"{wikipedia_command.__doc__}" ダヨ'
    except wikipedia.exceptions.PageError:
        return f"「{args}」ノ意味ガ見ツカリマセンデシタ"
