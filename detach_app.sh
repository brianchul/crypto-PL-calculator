#!/bin/bash
redis-server &
cd backend
python manager.py runserver