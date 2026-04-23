#!/bin/bash
pkill -f uvicorn || true
sleep 1
export PYTHONPATH=/home/ec2-user/environment/backend
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > /home/ec2-user/environment/backend/uvicorn.log 2>&1 &
