import logging
import sys
import json

from kafka import producer
from orm import ORM

from time import sleep


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fmt = logging.Formatter("%(asctime)s %(levelname)-8s %(name)-30s %(message)s")
sh = logging.StreamHandler(sys.stderr)
file_logger = logging.FileHandler("app.log")
sh.setFormatter(fmt)
logger.addHandler(sh)
logger.addHandler(file_logger)


def main():
    logger.info("Start Process")
    while True:
        try:
            jobs = ORM.get_jobs_to_execute()
            for job in jobs:
                msg = json.dumps({"id": job.id, "info": job.info})
                if job.type == "source":
                    producer.produce("jobs-source", msg)
                    logger.info("Job to collect new data from source was sent")
                elif job.type == "nlp":
                    producer.produce("jobs-nlp", msg)
                    logger.info("Job to execute a new nlp process was sent")
                else:
                    logger.warning(f"Job w. type {job.type} is not supported yet.")
                ORM.update_job(job)
            logger.info("Waiting for jobs zZzZzZzzzZZz")
            sleep(6)
        except Exception as e:
            logger.exception(str(e))
            sleep(60)


if __name__ == "__main__":
    main()
