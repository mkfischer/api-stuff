#!/usr/bin/env python

import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from termcolor import colored
import uvicorn
import ssl

app = FastAPI()


class ApplicationMetrics(BaseModel):
    application_status: str
    start_time: str
    database_status: str
    image: str
    cpu_utilisation: float
    memory_utilisation: float


class ReplicationProcess(BaseModel):
    target_table: str
    process_id: str
    date: str
    status: str = "running"


class ValidationResponse(BaseModel):
    msg: str


@app.get("/health/ping", response_model=str)
async def ping_health():
    if random.randint(1, 20) == 1:
        print(colored("Unsuccessful ping", "yellow"))
        raise HTTPException(status_code=500, detail="Ping failed")
    return colored("pong", "yellow")


@app.get("/health/detailed", response_model=ApplicationMetrics)
async def check_detailed_health():
    if random.randint(1, 20) == 1:
        print(colored("Unsuccessful health check", "yellow"))
        raise HTTPException(status_code=500, detail="Health check failed")
    return ApplicationMetrics(
        application_status="OK",
        start_time="2024-04-30T08:35:00",
        database_status="Connected",
        image="fastapi:latest",
        cpu_utilisation=0.5,
        memory_utilisation=0.75,
    )


@app.post("/v1/replication", response_model=ReplicationProcess)
async def start_replication():
    if random.randint(1, 20) == 1:
        print(colored("Replication process failed", "yellow"))
        raise HTTPException(status_code=500, detail="Replication failed")
    return ReplicationProcess(
        target_table="user_data",
        process_id="123e4567-e89b-12d3-a456-426614174000",
        date="2024-04-30T08:40:00",
    )


@app.get("/v1/validation/credentials", response_model=ValidationResponse)
async def validate_key(apikey: str, service: str):
    if random.randint(1, 20) == 1:
        print(colored("Invalid credentials", "yellow"))
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return ValidationResponse(msg="Credentials are valid")


if __name__ == "__main__":
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_context=ssl_context)
