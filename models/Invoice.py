from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, func, DateTime, Date, DECIMAL

class Invoice(Base):
    __tablename__ = "invoices"
    
    id = Column(Integer, primary_key=True,index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    invoice_number = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    due_date = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)