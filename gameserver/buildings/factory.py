from datetime import datetime
import schemas
import models


class Factory(models.Building):
    def install_job(self, job: schemas.BuildingJobCreate):
        pass

    def time_till_completion() -> datetime:
        pass
