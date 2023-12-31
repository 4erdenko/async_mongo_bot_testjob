import json
from datetime import datetime
from typing import Dict, Union

from aggregator.utils import fill_missing_dates
from database.db import MongoBase


class SalaryAggregator:
    def __init__(self, parameters: Dict[str, Union[str, datetime]]):
        self.pre_dt_from = parameters.get('dt_from')
        self.pre_dt_upto = parameters.get('dt_upto')
        self.group_type = parameters.get('group_type')
        self.dt_from = datetime.fromisoformat(self.pre_dt_from)
        self.dt_upto = datetime.fromisoformat(self.pre_dt_upto)

    async def aggregate(self, db_accessor: MongoBase) -> json:
        group_id = {}
        if self.group_type == 'day':
            group_id = {
                'year': {'$year': '$dt'},
                'month': {'$month': '$dt'},
                'day': {'$dayOfMonth': '$dt'},
            }
        elif self.group_type == 'month':
            group_id = {'year': {'$year': '$dt'}, 'month': {'$month': '$dt'}}
        elif self.group_type == 'hour':
            group_id = {
                'year': {'$year': '$dt'},
                'month': {'$month': '$dt'},
                'day': {'$dayOfMonth': '$dt'},
                'hour': {'$hour': '$dt'},
            }
        pipeline = [
            {'$match': {'dt': {'$gte': self.dt_from, '$lte': self.dt_upto}}},
            {'$group': {'_id': group_id, 'total_value': {'$sum': '$value'}}},
            {'$sort': {'_id': 1}},
        ]

        result = await db_accessor.aggregate(pipeline)
        dataset = []
        labels = []

        for record in result:
            total_value = record['total_value']
            dataset.append(total_value)

            year = record['_id']['year']
            month = record['_id']['month']

            if self.group_type == 'day':
                day = record['_id']['day']
                labels.append(f'{year}-{month:02d}-{day:02d}T00:00:00')
            elif self.group_type == 'month':
                labels.append(f'{year}-{month:02d}-01T00:00:00')
            elif self.group_type == 'hour':
                day = record['_id']['day']
                hour = record['_id']['hour']
                labels.append(f'{year}-{month:02d}-{day:02d}T{hour:02d}:00:00')
        labels, dataset = fill_missing_dates(
            labels, dataset, self.dt_from, self.dt_upto, self.group_type
        )
        labels = [dt.strftime('%Y-%m-%dT%H:%M:%S') for dt in labels]
        response = {'dataset': dataset, 'labels': labels}
        json_response = json.dumps(response)
        return json_response
