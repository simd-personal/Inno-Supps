"""
Database models and configuration for Inno Supps
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, JSON, Float, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from datetime import datetime
from enum import Enum
import uuid

# Database URL
DATABASE_URL = "postgresql://postgres:password@localhost:5432/innosupps"

# Create engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Enums
class MembershipRole(str, Enum):
    ADMIN = "admin"
    CONTRIBUTOR = "contributor"
    VIEWER = "viewer"

class IntegrationType(str, Enum):
    EMAIL_GMAIL = "email_gmail"
    EMAIL_M365 = "email_m365"
    CALENDAR_GCAL = "calendar_gcal"
    CALENDAR_OUTLOOK = "calendar_outlook"
    CALENDLY = "calendly"
    SLACK = "slack"
    HUBSPOT = "hubspot"
    SALESFORCE = "salesforce"
    APOLLO = "apollo"
    TWILIO = "twilio"
    ZOOM = "zoom"

class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"

class JobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"

class MessageDirection(str, Enum):
    INBOUND = "inbound"
    OUTBOUND = "outbound"

# Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    memberships = relationship("Membership", back_populates="user")
    audit_events = relationship("AuditEvent", back_populates="actor")

class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    memberships = relationship("Membership", back_populates="workspace")
    integrations = relationship("Integration", back_populates="workspace")
    prospects = relationship("Prospect", back_populates="workspace")
    accounts = relationship("Account", back_populates="workspace")
    contacts = relationship("Contact", back_populates="workspace")
    campaigns = relationship("Campaign", back_populates="workspace")
    email_templates = relationship("EmailTemplate", back_populates="workspace")
    threads = relationship("Thread", back_populates="workspace")
    meetings = relationship("Meeting", back_populates="workspace")
    calls = relationship("Call", back_populates="workspace")
    research_briefs = relationship("ResearchBrief", back_populates="workspace")
    growth_plans = relationship("GrowthPlan", back_populates="workspace")
    jobs = relationship("Job", back_populates="workspace")
    audit_events = relationship("AuditEvent", back_populates="workspace")
    agent_memories = relationship("AgentMemory", back_populates="workspace")
    metric_dailies = relationship("MetricDaily", back_populates="workspace")

class Membership(Base):
    __tablename__ = "memberships"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    role = Column(SQLEnum(MembershipRole), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="memberships")
    workspace = relationship("Workspace", back_populates="memberships")

class Integration(Base):
    __tablename__ = "integrations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    type = Column(SQLEnum(IntegrationType), nullable=False)
    status = Column(String(50), nullable=False)  # connected, disconnected, error
    auth_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="integrations")

class Prospect(Base):
    __tablename__ = "prospects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    email = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    company = Column(String(255))
    title = Column(String(255))
    phone = Column(String(50))
    linkedin_url = Column(String(500))
    enrichment_json = Column(JSON)
    score = Column(Float, default=0.0)
    summary_embedding = Column(Vector(1536))  # OpenAI embedding dimension
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="prospects")
    meetings = relationship("Meeting", back_populates="prospect")
    calls = relationship("Call", back_populates="prospect")

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    name = Column(String(255), nullable=False)
    domain = Column(String(255))
    industry = Column(String(100))
    size = Column(String(50))
    website = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="accounts")
    contacts = relationship("Contact", back_populates="account")

class Contact(Base):
    __tablename__ = "contacts"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    account_id = Column(UUID(as_uuid=True), ForeignKey("accounts.id"))
    email = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    title = Column(String(255))
    phone = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="contacts")
    account = relationship("Account", back_populates="contacts")

class Campaign(Base):
    __tablename__ = "campaigns"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    sequence_json = Column(JSON)
    status = Column(SQLEnum(CampaignStatus), default=CampaignStatus.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="campaigns")
    sequence_steps = relationship("SequenceStep", back_populates="campaign")

class SequenceStep(Base):
    __tablename__ = "sequence_steps"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    campaign_id = Column(UUID(as_uuid=True), ForeignKey("campaigns.id"), nullable=False)
    order = Column(Integer, nullable=False)
    channel = Column(String(50), nullable=False)  # email, linkedin, call
    template_ref = Column(String(255))
    wait_hours = Column(Integer, default=24)
    branch_rule_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    campaign = relationship("Campaign", back_populates="sequence_steps")

class EmailTemplate(Base):
    __tablename__ = "email_templates"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    name = Column(String(255), nullable=False)
    subject = Column(String(500))
    body_md = Column(Text)
    variables_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="email_templates")

class Thread(Base):
    __tablename__ = "threads"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    provider_thread_id = Column(String(255), nullable=False)
    subject = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="threads")
    messages = relationship("Message", back_populates="thread")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    thread_id = Column(UUID(as_uuid=True), ForeignKey("threads.id"), nullable=False)
    provider_message_id = Column(String(255), nullable=False)
    direction = Column(SQLEnum(MessageDirection), nullable=False)
    from_email = Column(String(255))
    to_email = Column(String(255))
    subject = Column(String(500))
    body_text = Column(Text)
    body_html = Column(Text)
    headers_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    thread = relationship("Thread", back_populates="messages")

class Meeting(Base):
    __tablename__ = "meetings"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    prospect_id = Column(UUID(as_uuid=True), ForeignKey("prospects.id"))
    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)
    calendar_link = Column(String(500))
    source = Column(String(100))  # calendly, manual, auto_booked
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="meetings")
    prospect = relationship("Prospect", back_populates="meetings")

class Call(Base):
    __tablename__ = "calls"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    prospect_id = Column(UUID(as_uuid=True), ForeignKey("prospects.id"))
    recording_url = Column(String(500))
    transcript_text = Column(Text)
    transcript_vector = Column(Vector(1536))
    analysis_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="calls")
    prospect = relationship("Prospect", back_populates="calls")

class ResearchBrief(Base):
    __tablename__ = "research_briefs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    inputs_json = Column(JSON)
    output_md = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="research_briefs")

class GrowthPlan(Base):
    __tablename__ = "growth_plans"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    inputs_json = Column(JSON)
    plan_md = Column(Text)
    kpis_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="growth_plans")

class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    type = Column(String(100), nullable=False)
    payload_json = Column(JSON)
    status = Column(SQLEnum(JobStatus), default=JobStatus.QUEUED)
    attempts = Column(Integer, default=0)
    last_error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="jobs")

class AuditEvent(Base):
    __tablename__ = "audit_events"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    actor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    verb = Column(String(100), nullable=False)  # created, updated, deleted, sent, etc.
    entity_type = Column(String(100), nullable=False)  # prospect, campaign, etc.
    entity_id = Column(UUID(as_uuid=True), nullable=False)
    metadata_json = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="audit_events")
    actor = relationship("User", back_populates="audit_events")

class AgentMemory(Base):
    __tablename__ = "agent_memories"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    key = Column(String(255), nullable=False)
    value_json = Column(JSON)
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="agent_memories")

class MetricDaily(Base):
    __tablename__ = "metric_dailies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id"), nullable=False)
    metric_name = Column(String(100), nullable=False)
    value = Column(Float, nullable=False)
    recorded_on = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    workspace = relationship("Workspace", back_populates="metric_dailies")

# Database functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize the database with all tables"""
    Base.metadata.create_all(bind=engine)