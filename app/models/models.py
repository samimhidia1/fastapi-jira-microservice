from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base

class Epic(Base):
    __tablename__ = "epics"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    summary = Column(String, index=True)
    description = Column(Text)
    project_key = Column(String)
    custom_fields = Column(Text)

    stories = relationship("Story", back_populates="epic")

class Story(Base):
    __tablename__ = "stories"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    summary = Column(String, index=True)
    description = Column(Text)
    project_key = Column(String)
    custom_fields = Column(Text)
    epic_id = Column(UUID(as_uuid=True), ForeignKey("epics.id"))

    epic = relationship("Epic", back_populates="stories")
    tasks = relationship("Task", back_populates="story")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    summary = Column(String, index=True)
    description = Column(Text)
    project_key = Column(String)
    custom_fields = Column(Text)
    story_id = Column(UUID(as_uuid=True), ForeignKey("stories.id"))

    story = relationship("Story", back_populates="tasks")
    test_cases = relationship("TestCase", back_populates="task")

class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    summary = Column(String, index=True)
    description = Column(Text)
    project_key = Column(String)
    custom_fields = Column(Text)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.id"))

    task = relationship("Task", back_populates="test_cases")
