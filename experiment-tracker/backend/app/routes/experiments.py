from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app import models, schemas
from datetime import datetime

router = APIRouter(prefix="/api/experiments", tags=["experiments"])

@router.post("", response_model=schemas.ExperimentResponse)
def create_experiment(exp_create: schemas.ExperimentCreate, db: Session = Depends(get_db)):
    exp = models.Experiment(**exp_create.model_dump())
    db.add(exp)
    db.commit()
    db.refresh(exp)
    return exp

@router.get("", response_model=list[schemas.ExperimentResponse])
def list_experiments(
    skip: int = Query(0),
    limit: int = Query(10),
    status: str = Query(None),
    user: str = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(models.Experiment)
    
    if status:
        query = query.filter(models.Experiment.status == status)
    if user:
        query = query.filter(models.Experiment.user == user)
    
    return query.order_by(models.Experiment.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/{exp_id}", response_model=schemas.ExperimentResponse)
def get_experiment(exp_id: int, db: Session = Depends(get_db)):
    exp = db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return exp

@router.patch("/{exp_id}", response_model=schemas.ExperimentResponse)
def update_experiment(
    exp_id: int,
    exp_update: schemas.ExperimentUpdate,
    db: Session = Depends(get_db)
):
    exp = db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    update_data = exp_update.model_dump(exclude_unset=True)
    exp.updated_at = datetime.utcnow()
    
    for field, value in update_data.items():
        if field == "params" and value:
            exp.params = {**exp.params, **value}
        elif field == "metrics" and value:
            exp.metrics = {**exp.metrics, **value}
        else:
            setattr(exp, field, value)
    
    db.commit()
    db.refresh(exp)
    return exp

@router.post("/compare")
def compare_experiments(
    compare: schemas.ExperimentCompare,
    db: Session = Depends(get_db)
):
    exps = db.query(models.Experiment).filter(
        models.Experiment.id.in_(compare.experiment_ids)
    ).all()
    
    if not exps:
        raise HTTPException(status_code=404, detail="No experiments found")
    
    return {
        "experiments": exps,
        "comparison": {
            "count": len(exps),
            "params_keys": set().union(*[set(e.params.keys()) for e in exps]),
            "metrics_keys": set().union(*[set(e.metrics.keys()) for e in exps])
        }
    }

@router.delete("/{exp_id}")
def delete_experiment(exp_id: int, db: Session = Depends(get_db)):
    exp = db.query(models.Experiment).filter(models.Experiment.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    db.delete(exp)
    db.commit()
    return {"message": "Experiment deleted"}
