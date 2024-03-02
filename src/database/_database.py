from datetime import datetime
from dateutil.relativedelta import relativedelta

from motor.motor_asyncio import AsyncIOMotorClient

from src.common import config


class MongoDB:
    def __init__(self, host: str, port: int, db_name: str, collection: str = 'sample_collection') -> None:
        self.client = AsyncIOMotorClient(f'mongodb://{host}:{port}')
        self.collection = self.client[db_name][collection]

    async def aggregate(self, dt_from: datetime, dt_upto: datetime, group_type: str) -> dict[str, int]:
        group_types = {
            'hour': "%Y-%m-%dT%H",
            'day': "%Y-%m-%d",
            'month': "%Y-%m"
        }

        pipeline = [
            {
                '$match': {
                    'dt': {
                        '$gte': dt_from,
                        '$lte': dt_upto
                    }
                }
            },
            {
                '$group': {
                    '_id': {
                        'dt': {
                          '$dateToString': {'format': group_types[group_type], 'date': "$dt"}
                        },
                    },
                    'total_value': {
                        '$sum': '$value'
                        }
                    }
            },
            {
                '$sort': {
                    '_id': 1
                }
            }
        ]

        res = {
            datetime.strptime(item['_id']['dt'], group_types[group_type]).isoformat(): item['total_value']
            async for item in self.collection.aggregate(pipeline)
        }

        return res

    async def get_dataset(self, dt_from: datetime, dt_upto: datetime, group_type: str, labels: list[str]) -> list[int]:
        res = await self.aggregate(dt_from, dt_upto, group_type)
        dataset = [res.get(label, 0) for label in labels]

        return dataset

    @staticmethod
    def get_labels(dt_from: datetime, dt_upto: datetime, group_type: str) -> list[str]:
        group_type += 's'
        labels = []
        while dt_from <= dt_upto:
            labels.append(dt_from.isoformat())
            dt_from += relativedelta(**{group_type: 1})

        return labels


db = MongoDB(config.DB_HOST, config.DB_PORT, config.DB_NAME)
