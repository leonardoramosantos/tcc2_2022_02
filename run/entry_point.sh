#!/bin/bash

uvicorn src.main:app --reload --reload-dir ./src/ --host 0.0.0.0