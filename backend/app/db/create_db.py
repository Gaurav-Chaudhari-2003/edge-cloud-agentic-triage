from app.db.models import Base
from app.core.database import engine

Base.metadata.create_all(
    bind=engine
)

print("done")