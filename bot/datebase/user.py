import aiosqlite

from config import datebasePath, siteDatebasePath

async def regUser(tgId, phoneNumber, lang):
    try:
        async with aiosqlite.connect(datebasePath) as con:
            async with con.cursor() as cur:
                await cur.execute("SELECT tg_id FROM users WHERE tg_id=?;", (tgId,))
                data = await cur.fetchone()

                if data is None:
                    usersList = (tgId, phoneNumber, lang)
                    await cur.execute("INSERT INTO users (tg_id, phoneNumber, lang) VALUES (?, ?, ?);", usersList)
                    await con.commit()
                    return True
                else:
                    return False
    except Exception as err:
            print(err)

async def isReg(tgId):
    try:
        async with aiosqlite.connect(datebasePath) as con:
            async with con.cursor() as cur:
                await cur.execute("SELECT tg_id FROM users WHERE tg_id=?;", (tgId,))
                data = await cur.fetchone()
                if data is None:
                    return False
                else:
                    return True
    except Exception as err:
            print(err)

async def getLang(tgId):
    try:
        async with aiosqlite.connect(datebasePath) as con:
            async with con.cursor() as cur:
                await cur.execute("SELECT lang FROM users WHERE tg_id=?;", (tgId,))
                lang_row = await cur.fetchone()
                if lang_row:
                    lang = lang_row[0]
                    return lang
                else:
                    return None
    except Exception as err:
            print(err)

async def getUserPhoneNumber(tgId):
    try:
        async with aiosqlite.connect(datebasePath) as con:
            async with con.cursor() as cur:
                await cur.execute("SELECT phoneNumber FROM users WHERE tg_id=?;", (tgId,))
                number_row = await cur.fetchone()
                if number_row:
                    phoneNumber = number_row[0]
                    return phoneNumber
                else:
                    return None
    except Exception as err:
        print(err)

async def getUserInfo(tgId):
    try:
        async with aiosqlite.connect(siteDatebasePath) as con:
            async with con.cursor() as cur:
                phoneNumber = await getUserPhoneNumber(tgId)
                if phoneNumber[0] is None:
                    return None
                await cur.execute("SELECT * FROM users WHERE phoneNumber=?;", (phoneNumber,))
                userInfo = await cur.fetchall()

                if userInfo[0] is None:
                    return None
                else:
                    return userInfo
                
    except Exception as err:
        print(err)

async def changeLang(tgId, lang):
    try:
        async with aiosqlite.connect(datebasePath) as con:
            async with con.cursor() as cur:
                await cur.execute("UPDATE users SET lang = ? WHERE tg_id = ?;", (lang, tgId))
                await con.commit()
                
    except Exception as err:
        print(err)

async def logout(tgId):
    try:
        async with aiosqlite.connect(datebasePath) as con:
            async with con.cursor() as cur:
                await cur.execute("DELETE FROM users WHERE tg_id = ?;", (tgId,))
                await con.commit()
                
    except Exception as err:
        print(err)