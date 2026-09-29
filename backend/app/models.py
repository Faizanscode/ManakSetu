from sqlalchemy import Column, String, Text, Integer, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base
from pgvector.sqlalchemy import Vector

class AnalysisHistory(Base):
    __tablename__ = "analysis_history"
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    procurement_requirement = Column(Text, nullable=False)
    category = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    
    extracted_requirement = Column(JSONB, nullable=True)
    recommendations = Column(JSONB, nullable=True)
    gaps = Column(JSONB, nullable=True)
    specification = Column(JSONB, nullable=True)
    
    status = Column(String, default="COMPLETED")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Sector(Base):
    __tablename__ = "sectors"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    categories = relationship("Category", back_populates="sector")
    standards = relationship("Standard", back_populates="sector")

class Category(Base):
    __tablename__ = "categories"
    id = Column(String, primary_key=True)
    sector_id = Column(String, ForeignKey("sectors.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sector = relationship("Sector", back_populates="categories")
    standards = relationship("Standard", back_populates="category")

class Standard(Base):
    __tablename__ = "standards"
    id = Column(String, primary_key=True)
    standard_number = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    short_description = Column(Text)
    issuing_body = Column(String, default="Bureau of Indian Standards")
    sector_id = Column(String, ForeignKey("sectors.id"), nullable=True)
    category_id = Column(String, ForeignKey("categories.id"), nullable=True)
    status = Column(String, nullable=False, default="CURRENT")
    embedding = Column(Vector(768), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    sector = relationship("Sector", back_populates="standards")
    category = relationship("Category", back_populates="standards")
    versions = relationship("StandardVersion", back_populates="standard")
    scopes = relationship("StandardScope", back_populates="standard")
    keywords = relationship("StandardKeyword", back_populates="standard")
    sources = relationship("StandardSource", back_populates="standard")
    relationships_as_source = relationship("StandardRelationship", foreign_keys="StandardRelationship.source_standard_id", back_populates="source_standard")
    relationships_as_target = relationship("StandardRelationship", foreign_keys="StandardRelationship.target_standard_id", back_populates="target_standard")

class StandardVersion(Base):
    __tablename__ = "standard_versions"
    id = Column(String, primary_key=True)
    standard_id = Column(String, ForeignKey("standards.id"), nullable=False)
    edition = Column(String, nullable=False)
    publication_date = Column(String)
    effective_date = Column(String)
    status = Column(String, nullable=False)
    amendment_information = Column(Text)
    supersedes_version_id = Column(String, nullable=True)
    source_id = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    standard = relationship("Standard", back_populates="versions")

class StandardScope(Base):
    __tablename__ = "standard_scopes"
    id = Column(String, primary_key=True)
    standard_id = Column(String, ForeignKey("standards.id"), nullable=False)
    scope_text = Column(Text, nullable=False)
    included_products = Column(String)
    excluded_products = Column(String)
    applications = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    standard = relationship("Standard", back_populates="scopes")

class Keyword(Base):
    __tablename__ = "keywords"
    id = Column(String, primary_key=True)
    word = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class StandardKeyword(Base):
    __tablename__ = "standard_keywords"
    standard_id = Column(String, ForeignKey("standards.id"), primary_key=True)
    keyword_id = Column(String, ForeignKey("keywords.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    standard = relationship("Standard", back_populates="keywords")
    keyword = relationship("Keyword")

class StandardRelationship(Base):
    __tablename__ = "standard_relationships"
    id = Column(String, primary_key=True)
    source_standard_id = Column(String, ForeignKey("standards.id"), nullable=False)
    target_standard_id = Column(String, ForeignKey("standards.id"), nullable=False)
    relationship_type = Column(String, nullable=False)
    description = Column(Text)
    source_id = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    source_standard = relationship("Standard", foreign_keys=[source_standard_id], back_populates="relationships_as_source")
    target_standard = relationship("Standard", foreign_keys=[target_standard_id], back_populates="relationships_as_target")

class StandardSource(Base):
    __tablename__ = "standard_sources"
    id = Column(String, primary_key=True)
    standard_id = Column(String, ForeignKey("standards.id"), nullable=False)
    organization = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    title = Column(String)
    url = Column(String)
    document_name = Column(String)
    page = Column(String)
    section = Column(String)
    retrieved_at = Column(DateTime(timezone=True), server_default=func.now())
    notes = Column(Text)

    standard = relationship("Standard", back_populates="sources")
