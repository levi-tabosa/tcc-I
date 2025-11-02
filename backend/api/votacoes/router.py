from fastapi import APIRouter, HTTPException, Query
from datetime import date
import psycopg2
import logging

import database.db as db


router =  APIRouter(
    prefix="/votacoes",
    tags=["Votações"]
)



