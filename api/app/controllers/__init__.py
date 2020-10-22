from flask import Flask, current_app

from app.controllers.tasks import register_api as register_api_task

def register_apis(api) -> None:
    register_api_task(api)
    


