from app.db.connection import get_connection
from app.api.schemas.runs import AgentRun
from psycopg.rows import dict_row


def get_all_runs() -> list[AgentRun]:
    with get_connection() as con:
        with con.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
            SELECT * FROM agent_runs;
            """)

            rows = cursor.fetchall()
            
            return [AgentRun.model_validate(row) for row in rows]
        
def get_run(run_id: int) -> AgentRun | None:
    with get_connection() as con:
        with con.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
            SELECT * FROM agent_runs WHERE agent_runs.id = %s
            """,
            (run_id,))
            row =  cursor.fetchone()
            if row is None:
                return None
            
            return AgentRun.model_validate(row)

def create_run(goal: str, context: str) -> AgentRun | None:
    with get_connection() as con:
        with con.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
            INSERT INTO agent_runs (goal, context) VALUES (%s, %s)
            RETURNING *;
            """,
            (goal, context))
            row =  cursor.fetchone()
            if row is None:
                return None
            return AgentRun.model_validate(row) 

def update_status(run_id: int, status: str) -> AgentRun | None:
    with get_connection() as con:
        with con.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
            UPDATE agent_runs 
            SET status = %s
            WHERE id = %s
            RETURNING *
            """,
            (status, run_id))
            row =  cursor.fetchone()
            if row is None:
                return None
            return AgentRun.model_validate(row)
        
def complete_run(run_id: int, response: str) -> AgentRun | None:
    with get_connection() as con:
        with con.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
            UPDATE agent_runs
            SET 
               status = 'completed',
               response = %s
            WHERE id = %s
            RETURNING *
            """,
            (response, run_id))
            row = cursor.fetchone()
            if row is None:
                return None
            return AgentRun.model_validate(row)

def fail_run(run_id: int, message: str) -> AgentRun | None:
    with get_connection() as con:
        with con.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
            UPDATE agent_runs
            SET 
                status = 'failed',
                error = %s
            WHERE id = %s
            RETURNING *
            """,
            (message, run_id))
            row = cursor.fetchone()
            if row is None:
                return None
            return AgentRun.model_validate(row)

def claim_run(run_id: int) -> AgentRun | None:
    with get_connection() as con:
        with con.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
            UPDATE agent_runs
            SET status = 'running'
            WHERE id = %s AND status = 'pending'
            RETURNING *
            """,
            (run_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return AgentRun.model_validate(row)

