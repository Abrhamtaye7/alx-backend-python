import aiosqlite
import asyncio

async def async_fetch_users(db_file):
    async with aiosqlite.connect(db_file) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()

async def async_fetch_older_users(db_file):
    async with aiosqlite.connect(db_file) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()

async def fetch_concurrently(db_file):
    results = await asyncio.gather(
        async_fetch_users(db_file),
        async_fetch_older_users(db_file)
    )
    all_users, older_users = results
    return all_users, older_users

if __name__ == "__main__":
    db_file = "airbnb.db"

    all_users, older_users = asyncio.run(fetch_concurrently(db_file))

    print("All Users:")
    for user in all_users:
        print(user)

    print("\nUsers Older Than 40:")
    for user in older_users:
        print(user)
