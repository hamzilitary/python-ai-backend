from fastapi import APIRouter,HTTPException
from app.api.schemas.runs import CreateRunRequest
from app.api.schemas.runs   import GetRunRequest
from app.api.schemas.runs import UpdateStatus, AgentRun
from app.db.quireies import create_run
from app.db.quireies import get_all_runs
from app.db.quireies import get_run 
from app.db.quireies import update_status
from app.services.llm_service import LLLService, RunNotFoundError, InvalidStatusError
router = APIRouter()

@router.get("/")
def root():
    return {"message": "AI project is running"}


@router.get("/runs", response_model=list[AgentRun])
def get_runs():
    get_every_run = get_all_runs()
    return get_every_run

@router.post("/runs", response_model=AgentRun)
def create_run_route(request: CreateRunRequest):
    new_run = create_run(
        request.goal,
        request.context
    )
    return new_run       

@router.get("/runs/{run_id}", response_model=AgentRun)
def get_run_route(run_id: int):
        run  = get_run(
        run_id
        )
        if run is None:
             print("No rows found")
             raise HTTPException(
                  status_code= 404,
                  detail="No rows found with this ID")
        
        return run

@router.patch("/runs/{run_id}/status", response_model=AgentRun)
def update_status_route(run_id: int, request: UpdateStatus):
     print("status:", repr(request.status))
     print("type:", type(request.status))
     if request.status not in ("pending", "completed", "running", "failed"):
          raise HTTPException(status_code=400,
                              detail="Invalid request")
     update_run = update_status(
          run_id,
          request.status
     )
     if update_run is None:
          print("No rows found")
          raise HTTPException(status_code=404,
                              detail= "No rows found to update with that ID")
     return update_run

@router.post("/runs/{run_id}/execute", response_model=AgentRun)
def execute_run_route(run_id: int):
    try:
        execute_run_func = LLLService().execute_run(run_id)
        return execute_run_func
    except RunNotFoundError as e:
          raise HTTPException(status_code=404,
                              detail=str(e))
    except InvalidStatusError as e:
         raise HTTPException(status_code=400,
                             detail=str(e))
    except RuntimeError as e:
          raise HTTPException(status_code=500,
                              detail=str(e))
          
          
     
     

        

##$ docker exec -it ai-postgres psql -U postgres -d agent_db
