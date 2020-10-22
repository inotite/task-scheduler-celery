import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    'postgresql://martin:root1234@localhost:15432/martin_mcguire', convert_unicode=True,
    pool_recycle=3600, pool_size=10)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))