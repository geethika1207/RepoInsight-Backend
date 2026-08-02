from sqlalchemy import Column, String, INTEGER, ForeignKey, JSON, Text, Float
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from pgvector.sqlalchemy import Vector

class USER(Base):
    __tablename__ = "Users"

    id = Column(INTEGER, primary_key = True)
    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone=True), nullable = False, server_default = text('now()'))


class Repository(Base):
    __tablename__ = "Repositories"

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    repo_url = Column(String, nullable=False)
    repo_name = Column(String, nullable=False)
    repo_owner = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))


class Chunk(Base):
    __tablename__ = "Chunks"

    id = Column(INTEGER, primary_key=True)

    repository_id = Column(INTEGER, ForeignKey("Repositories.id", ondelete="CASCADE"), nullable=False)
    chunk_index = Column(INTEGER, nullable=False)
    chunk_text = Column(Text, nullable=False)
    chunk_embedding = Column(Vector(384), nullable=False)
    chunk_metadata = Column(JSON, nullable=False)


class Analysis(Base):
    __tablename__ = "Analysis"

    id = Column(INTEGER, primary_key=True)

    repository_id = Column(INTEGER, ForeignKey("Repositories.id", ondelete="CASCADE"), nullable=False)


    architecture_report = Column(Text)

    api_review = Column(Text)

    security_review = Column(Text)

    database_review = Column(Text)

    code_quality_review = Column(Text)

    documentation_review = Column(Text)

    strengths = Column(Text)

    beginner_contributions = Column(Text)

    intermediate_contributions = Column(Text)

    advanced_contributions = Column(Text)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
