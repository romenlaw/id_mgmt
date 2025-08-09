from datetime import datetime
from typing import List, Annotated
from pydantic import validate_call, Field
from faker import Faker
from sqlalchemy import exists

from .models import IdStatus, IdType, ID, session

def _save_id(type:IdType, value:str, status:IdStatus)->None:
    # print(f"saving id: {type=}, {value=}")
    id = ID(
        value = value,
        type = type,
        status = status,
        last_updated_dt = datetime.now()
    )
    if session.query(exists().where((ID.value == value) & (ID.type == type))).scalar():
        raise ValueError(f"{type} {value} has already been allocated. Try another value.")
    session.add(id)
    session.commit()

fake = Faker('en_AU')

class FidManager():
    FID_PATTERN = "#"*10  # faker bothify pattern

    @staticmethod
    def generate(pattern:str = None)->str:
        try:
            id_value = fake.bothify(pattern if pattern else FidManager.FID_PATTERN)
        except:
            id_value = fake.bothify(FidManager.FID_PATTERN)
        _save_id(IdType.FID, value=id_value, status=IdStatus.ALLOCATED)
        return id_value

class OidManager():
    OID_PATTERN = "#"*15  # faker bothify pattern

    @staticmethod
    def generate(pattern:str = None)->str:
        try:
            id_value = fake.bothify(pattern if pattern else OidManager.OID_PATTERN)
        except:
            id_value = fake.bothify(FidManager.OID_PATTERN)
        _save_id(IdType.OID, value=id_value, status=IdStatus.ALLOCATED)
        return id_value

class TidManager():
    TID_PATTERN = "?"*6+"00"  # faker bothify pattern
    LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789' # faker bothify letters

    @staticmethod
    @validate_call
    def generate(pattern:str = None, 
                 quanity: Annotated[int, Field(ge=1, le=100)] = 1
                 )->List[str]:
        ids = []
        try:
            id_value = fake.bothify(text = pattern if pattern else TidManager.TID_PATTERN, 
                                    letters=TidManager.LETTERS)
        except:
            id_value = fake.bothify(text=TidManager.TID_PATTERN, letters=TidManager.LETTERS)
        _save_id(IdType.TID, value=id_value, status=IdStatus.ALLOCATED)
        ids.append(id_value)

        for i in range(quanity-1):
            id_value = TidManager.next_value(id_value)
            # check if the id is already allocated, if so, skip it and get next again
            while session.query(exists().where((ID.value == id_value) & (ID.type == IdType.TID))).scalar():
                id_value = TidManager.next_value(id_value)
            _save_id(IdType.TID, value=id_value, status=IdStatus.ALLOCATED)
            ids.append(id_value)
        # print(f"tid generate: returning {ids}")
        return ids
    
    @staticmethod
    def next_value(current_value):
        prefix = current_value[:6]
        suffix = current_value[-2:]
        new_suf = f"{(int(suffix)+1):02d}"
        next_value = f"{prefix}{new_suf}"

        return next_value
        

class IdManager():
    map = {
        IdType.FID: FidManager,
        IdType.OID: OidManager,
        IdType.TID: TidManager,
    }
    @staticmethod
    def generate(type:IdType, pattern:str=None):
        try:
            mgr = map[type]
            return mgr.generate(pattern)
        except Exception as e:
            raise ValueError(e)
