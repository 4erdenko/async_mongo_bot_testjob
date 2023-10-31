import json
from datetime import datetime
from typing import Dict, Union

from aggregator.utils import daterange
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
        dataset = [0] * (int((self.dt_upto - self.dt_from).days) + 1)
        labels = list(daterange(self.dt_from, self.dt_upto))

        for record in result:
            total_value = record['total_value']
            year = record['_id']['year']
            month = record['_id']['month']
            day = record['_id'].get('day', 1)
            hour = record['_id'].get('hour', 0)

            date_index = (datetime(year, month, day, hour) - self.dt_from).days
            dataset[date_index] = total_value

        labels = [dt.strftime('%Y-%m-%dT%H:%M:%S') for dt in labels]
        response = {'dataset': dataset, 'labels': labels}
        json_response = json.dumps(response)
        return json_response
