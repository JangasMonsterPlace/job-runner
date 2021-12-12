import logging
import sys

from kafka import producer
from orm import ORM

from time import sleep


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
fmt = logging.Formatter("%(asctime)s %(levelname)-8s %(name)-30s %(message)s")
sh = logging.StreamHandler(sys.stderr)
sh.setFormatter(fmt)
logger.addHandler(sh)


def main():
    logger.info("Start Process")
    while True:
        try:
            jobs = ORM.get_jobs_to_execute()
            for job in jobs:
                if job.type == "source":
                    producer.produce("jobs-source", job.info)
                    logger.info("Job to collect new data from source was sent")
                elif job.type == "nlp":
                    producer.produce("jobs-nlp", job.info)
                    logger.info("Job to execute a new nlp process was sent")
                else:
                    logger.warning(f"Job w. type {job.type} is not supported yet.")
                ORM.update_job(job)
            logger.info("Waiting for jobs zZzZzZzzzZZz")
            sleep(1)
        except Exception as e:
            logger.exception(str(e))
            sleep(60)



if __name__ == "__main__":
    main()
