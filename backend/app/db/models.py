from sqlalchemy.orm import declarative_base
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import JSON

Base=declarative_base()

class Request(Base):

    __tablename__="requests"

    id=Column(
        Integer,
        primary_key=True
    )

    input_type=Column(
        String
    )

    content=Column(
        Text
    )

    status=Column(
        String,
        default="QUEUED"
    )

    current_agent=Column(
        String,
        nullable=True
    )

    route=Column(
        String,
        nullable=True
    )
    
    output=Column(
        JSON,
        nullable=True
    )

class AgentLog(Base):

    __tablename__="agent_logs"

    id=Column(
        Integer,
        primary_key=True
    )

    request_id=Column(
        Integer
    )

    agent=Column(
        String
    )

    duration_ms=Column(
        Integer
    )

    decision=Column(
        String
    )