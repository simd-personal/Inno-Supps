from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, Float, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
import uuid
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/inno_supps")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workspace_memberships = relationship("WorkspaceMembership", back_populates="user")
    generations = relationship("Generation", back_populates="user")
    compliance_checks = relationship("ComplianceCheck", back_populates="reviewer")

class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    billing_plan = Column(String, default="free")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    memberships = relationship("WorkspaceMembership", back_populates="workspace")
    generations = relationship("Generation", back_populates="workspace")

class WorkspaceMembership(Base):
    __tablename__ = "workspace_memberships"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    role = Column(String, default="member")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="workspace_memberships")
    workspace = relationship("Workspace", back_populates="memberships")

class PromptTemplate(Base):
    __tablename__ = "prompt_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    version = Column(String, nullable=False)
    schema_json = Column(JSON, nullable=False)
    system_prompt = Column(Text, nullable=False)
    output_schema = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    generations = relationship("Generation", back_populates="template")

class Generation(Base):
    __tablename__ = "generations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    template_id = Column(UUID(as_uuid=True), ForeignKey("prompt_templates.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    inputs_json = Column(JSON, nullable=False)
    output_json = Column(JSON, nullable=False)
    score = Column(Float)
    compliance_risk = Column(Float)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    template = relationship("PromptTemplate", back_populates="generations")
    user = relationship("User", back_populates="generations", foreign_keys=[user_id])
    workspace = relationship("Workspace", back_populates="generations")
    reviewer = relationship("User", foreign_keys=[reviewer_id])
    compliance_checks = relationship("ComplianceCheck", back_populates="generation")

class KBDoc(Base):
    __tablename__ = "kb_docs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String, nullable=False)
    title = Column(String, nullable=False)
    url = Column(String)
    text = Column(Text, nullable=False)
    vector = Column(Vector(1536))  # OpenAI embedding dimension
    meta_data = Column(JSON)  # Renamed from metadata to avoid SQLAlchemy conflict
    created_at = Column(DateTime, default=datetime.utcnow)

class ApprovedLanguage(Base):
    __tablename__ = "approved_language"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category = Column(String, nullable=False)
    text = Column(Text, nullable=False)
    citations = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    item_type = Column(String, nullable=False)  # 'generation', 'template', etc.
    item_id = Column(UUID(as_uuid=True), nullable=False)
    generation_id = Column(UUID(as_uuid=True), ForeignKey("generations.id"))
    risk_score = Column(Float, nullable=False)
    issues_json = Column(JSON, nullable=False)
    resolved = Column(Boolean, default=False)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    generation = relationship("Generation", back_populates="compliance_checks")
    reviewer = relationship("User", back_populates="compliance_checks")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)
