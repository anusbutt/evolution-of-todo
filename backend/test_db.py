import asyncio
from sqlalchemy import text
from app.database import engine
from sqlmodel import SQLModel
from app.models.user import User
from app.models.task import Task

async def main():
    print("=" * 50)
    print("PostgreSQL Connection Test")
    print("=" * 50)

    # Create tables
    print("\n1. Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    print("   ✓ Tables created")

    # List tables
    print("\n2. Listing tables...")
    async with engine.connect() as conn:
        result = await conn.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
        )
        tables = [row[0] for row in result.fetchall()]

        if tables:
            for table in tables:
                print(f"   ✓ {table}")
            print(f"\n   Total: {len(tables)} tables")
        else:
            print("   × No tables found")

    print("\n" + "=" * 50)
    print("Database Status: READY ✓")
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
