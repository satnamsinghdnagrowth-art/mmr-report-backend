from database._PostgresIntegration.dbConnection import get_connection
from core.models.base.ResultModel import Result

async def createTable(tableName: str, schema: dict) -> Result:
    try:
        conn =  await get_connection()

        if not conn:
            return Result(Status=0, Message="Database connection failed")
        
        # Add standard audit columns
        schema["CreatedOn"] = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        schema["CreatedBy"] = "INT"
        schema["UpdatedOn"] = "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        schema["UpdatedBy"] = "INT"


        columns = ", ".join([f"{col} {dtype}" for col, dtype in schema.items()])
        query = f"CREATE TABLE IF NOT EXISTS {tableName} ({columns});"

        with conn.cursor() as cur:
            cur.execute(query)
            conn.commit()

        conn.close()
        return Result(Status=1, Message=f"Table '{tableName}' created successfully.")

    except Exception as ex:
        return Result(Status=0, Message=f"Error in createTable: {ex}")


# 2. Insert records into any table
async def insertRecord(tableName: str, data: dict) -> Result:
    try:
        conn = await get_connection()
        if not conn:
            return Result(Status=0, Message="Database connection failed")

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {tableName} ({columns}) VALUES ({placeholders})"

        with conn.cursor() as cur:
            cur.execute(query, values)
            conn.commit()
        conn.close()

        return Result(Status=1, Message=f"Record inserted into '{tableName}'")

    except Exception as ex:
        return Result(Status=0, Message=f"Error in insertRecord: {ex}")


# 3. Read (SELECT) records using raw query
async def readRecords(query: str) -> Result:
    try:
        conn = await get_connection()
        if not conn:
            return Result(Status=0, Message="Database connection failed")

        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            result = [dict(zip(columns, row)) for row in rows]
        conn.close()

        return Result(Status=1, Message="Records fetched successfully", Data=result)

    except Exception as ex:
        return Result(Status=0, Message=f"Error in readRecords: {ex}")


# 4. Update record by ID
async def updateRecord(tableName: str, idColumn: str, recordId: int, updates: dict) -> Result:
    try:
        conn = await get_connection()
        if not conn:
            return Result(Status=0, Message="Database connection failed")

        set_clause = ", ".join([f"{key} = %s" for key in updates.keys()])
        values = list(updates.values()) + [recordId]

        query = f"UPDATE {tableName} SET {set_clause} WHERE {idColumn} = %s"

        with conn.cursor() as cur:
            cur.execute(query, values)
            conn.commit()
        conn.close()

        return Result(Status=1, Message=f"Record in '{tableName}' updated successfully")

    except Exception as ex:
        return Result(Status=0, Message=f"Error in updateRecord: {ex}")

# 5. Delete record by ID
async def deleteRecord(tableName: str, idColumn: str, recordId: int) -> Result:
    try:
        conn = await get_connection()
        if not conn:
            return Result(Status=0, Message="Database connection failed")

        query = f"DELETE FROM {tableName} WHERE {idColumn} = %s"

        with conn.cursor() as cur:
            cur.execute(query, (recordId,))
            conn.commit()
        conn.close()

        return Result(Status=1, Message=f"Record from '{tableName}' deleted successfully")

    except Exception as ex:
        return Result(Status=0, Message=f"Error in deleteRecord: {ex}")
