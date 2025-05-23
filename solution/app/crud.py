# -*- coding: utf-8 -*-
from typing import Dict,Any,Optional
from datetime import datetime
from app import db
from app.models import ElevatorDemand,ElevatorState
from app.validations import validate_floor, validate_state

def create_demand(data:Dict[str,Any]) -> None:
    actual_floor = data.get("actual_floor")
    target_floor = data.get("target_floor")
    if not validate_floor(actual_floor) or not validate_floor(target_floor):
        raise ValueError("Floor is not an integer")
    new_demand = ElevatorDemand(actual_floor=actual_floor,target_floor=target_floor)
    db.session.add(new_demand)
    db.session.commit()
    return


def create_state(data:Dict[str,Any]) -> None:
    floor = data.get("floor")
    vacant = data.get("vacant")
    if not validate_floor(floor):
        raise ValueError("Floor is not an integer")
    if not validate_state(vacant):
        raise ValueError("Vacant invalid")
    new_state = ElevatorState(floor=data['floor'], vacant=data['vacant'])
    db.session.add(new_state)
    db.session.commit()
    return
    
def change_state(state_id:int, data:Dict[str,str]) -> Optional[ElevatorState]:
    end_time = data.get("end_time")
    end_time = datetime.fromisoformat(end_time)
    state = ElevatorState.query.filter_by(id=state_id).first()
    if not state:
        return state
    state.end_time = end_time
    state.duration_sec = int((end_time - state.start_time).total_seconds())
    
    #Business Rule: Idle Relocation
    state.relocation_flag = state.duration_sec > 300
    db.session.commit()
    return state    

    
        
        
        
        
        
    