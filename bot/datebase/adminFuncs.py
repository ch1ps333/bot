import aiosqlite

from config import datebasePath, siteDatebasePath

async def getAdminList():
    try:
        async with aiosqlite.connect(datebasePath) as con:
            async with con.cursor() as cur:
                await cur.execute("SELECT tg_id FROM users WHERE admin = ?;", (1,))
                adminList = [item[0] for item in (await cur.fetchall())]

                return adminList
    except Exception as err:
        print(err)

async def isAdmin(userId):
    try:
        async with aiosqlite.connect(datebasePath) as con:
            async with con.cursor() as cur:
                await cur.execute("SELECT admin FROM users WHERE id = ?;", (userId,))
                res = (await cur.fetchone())[0]
                if res == 0:
                    return False
                elif res == 1:
                    return True
    except Exception as err:
        print(err)

async def addAdmin(login, password):
    try:
        async with aiosqlite.connect(siteDatebasePath) as con:
            async with con.cursor() as cur:
                await cur.execute("INSERT INTO user (username, password) VALUES (?, ?);", (login, password))
                await con.commit()
    except Exception as err:
        print(err)