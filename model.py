from sqlalchemy import String, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine('sqlite+aiosqlite:///database.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

class Base(DeclarativeBase):
    pass

class Image(Base):
    __tablename__ = "images"

    id: Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String(25))
    address: Mapped[str] = mapped_column(String(256))

async def update_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def add_image(filename, file_address):
    image = Image(name=filename, address=file_address)
    async with new_session() as session:
        session.add(image)
        await session.commit()

async def get_address(id: int):
    async with new_session() as session:
        address = await session.scalar(select(Image.address).where(Image.id == id))
        return address
