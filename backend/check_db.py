import asyncio
from sqlalchemy import text
from app.database import engine
from sqlmodel import SQLModel
from app.models.user import User
from app.models.task import Task

async def main():
    print("=" * 50)
    print("PostgreSQL Connection & Setup Test")
    print("=" * 50)

    # Create tables
    print("\n[1/3] Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("      SUCCESS: Tables created/verified")

    # List tables
    print("\n[2/3] Checking tables...")
    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
        )
        tables = [row[0] for row in result.fetchall()]

        if tables:
            for table in tables:
                print(f"      - {table}")
            print(f"\n      Total: {len(tables)} tables")
        else:
            print("      WARNING: No tables found")

    # Test queries
    print("\n[3/3] Testing queries...")
    async with engine.connect() as conn:
        # Count users
        result = await conn.execute(text("SELECT COUNT(*) FROM users"))
        user_count = result.scalar()
        print(f"      Users: {user_count}")

        # Count tasks
        result = await conn.execute(text("SELECT COUNT(*) FROM tasks"))
        task_count = result.scalar()
        print(f"      Tasks: {task_count}")

    print("\n" + "=" * 50)
    print("Database Status: READY & OPERATIONAL")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
