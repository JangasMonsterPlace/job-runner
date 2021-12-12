import logging
from typing import List, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from psycopg2.extras import execute_values
from db import _db


logger = logging.getLogger(__name__)


@dataclass
class Job:
    id: int
    type: str
    timestamp: datetime
    info: str
    last_execution: datetime
    next_execution: datetime
    frequency: int


class ORM:
    @classmethod
    def get_jobs_to_execute(cls) -> List[Job]:
        logger.info("Start Fetching Jobs")
        sql = f"""
            SELECT {",".join(Job.__annotations__.keys())} FROM jobs
            WHERE next_execution < %s OR next_execution IS NULL
        """
        _db.cur.execute(sql, (datetime.now(timezone.utc),))
        jobs = [Job(*job) for job in _db.cur.fetchall()]
        logger.info(f"Retrieved jobs to execute: {len(jobs)}")
        return jobs

    @classmethod
    def update_job(cls, job: Job):
        sql = """
                UPDATE jobs
                SET last_execution = %s, next_execution = %s
                WHERE id = %s
            """
        now = datetime.now(timezone.utc)
        next_execution = now + timedelta(minutes=job.frequency)
        _db.cur.execute(sql, (datetime.now(timezone.utc), next_execution, job.id))
