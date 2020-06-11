## 前提

Herokuのアカウントを作成しておくこと

https://signup.heroku.com/

## 手順
```
git clone https://github.com/SaitoTsutomu/pybot.git
cd pybot
heroku login  # ブラウザでログインすること
heroku create --buildpack heroku/python
git push heroku master
heroku logs
heroku open
```

## 終了

```
heroku ps:scale web=0
```
