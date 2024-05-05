from fastapi import FastAPI, HTTPException
from typing import List
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///db.sqlite3')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class Tag(Base):
    __tablename__='img_app_tag'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class Image(Base):
    __tablename__='img_app_image'

    id = Column(Integer, primary_key=True, index=True)
    image = Column(String)
    name = Column(String)
    published = Column(DateTime)
    tags = relationship("Tag", secondary='img_app_image_tags')
    description = Column(Text)


image_tags = Table('img_app_image_tags', Base.metadata,
                   Column('image_id', Integer, ForeignKey('img_app_image.id')),
                   Column('tag_id', Integer, ForeignKey('img_app_tag.id'))
                   )


def database():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()


# Endpoint listujący wszystkie tagi wraz z liczbą obrazków przypisanych do danego tagu
@app.get("/tags")
async def get_tags():
    db = database()
    tags = db.query(Tag.name, func.count('*')).join(image_tags).group_by(Tag.name).all()
    return {tag_name: count for tag_name, count in tags}


# Endpoint listujący wszystkie obrazki wraz z ich tagami
@app.get("/images")
async def get_images():
    db = database()
    
    images = db.query(Image).all()
    return [{"id": image.id, "published": image.published, "name": image.name,
             "description": image.description,
             "tags": [tag.name for tag in image.tags]} for image in images]



# Endpoint listujący wszystkie obrazki przypisane do danego tagu
@app.get("/images/{tag}")
async def get_images_by_tag(tag: str):
    db = database()
    
    images = db.query(Image).join(image_tags).join(Tag).filter(Tag.name == tag).all()
    return [{"id": image.id, "published": image.published, "name": image.name,
             "description": image.description,
             "tags": [tag.name for tag in image.tags]} for image in images]



# Endpoint kasujący obrazki
@app.delete("/images/del")
async def delete_images(image_ids: List[int]):
    db = database()
    success = 0
    failure = 0

    for image_id in image_ids:
        image = db.query(Image).filter(Image.id == image_id).first()
        if not image:
            failure += 1
            continue
        db.delete(image)
        db.commit()
        success += 1

    return {"ok": success, "no_such_image": failure}
