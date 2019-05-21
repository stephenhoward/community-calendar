from sqlalchemy import Column, VarChar, Text, LargeBinary, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

class Image(Base):
    __tablename__ = 'images'

    id   = Column( UUID, primary_key=True )
    data = Column( LargeBinary )
    info = relationship( ImageInfo, back_populates="image")

class ImageInfo(Base):
    __tablename__ = 'image_info'

    id          = Column( UUID,    primary_key=True, ForeignKey("image.id") )
    language    = Column( VarChar, primary_key=True )
    title       = Column( Text )
    description = Column( Text )