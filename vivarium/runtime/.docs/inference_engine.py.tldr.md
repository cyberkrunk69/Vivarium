<!-- FACT_CHECKSUM: 31301cabac224d96b96fa75a179548a506ae40858939d0dbf4b5a74915a1cd94 -->

# ELIV
This module coordinates specialized helpers with awareness of constraints and activity.

## Module Constants
- `logger`: (used at lines 76, 81, 83, 84)
- `_COMPLEXITY_KEYWORDS`: ['algorithm', 'optimize', 'refactor', 'benchmark', 'scale', 'performance', 'thread', 'process', 'async', 'concurrency', 'distributed', 'pipeline', 'sql', 'database', 'api', 'authentication', 'encryption', 'docker', 'kubernetes', 'microservice', 'cache', 'index', 'migration'] (used at lines 66)

# EngineType
Available inference backends.

## Constants
- None

## Methods
- `__init__`: description
- None

# estimate_complexity
Return a numeric complexity score. Higher scores -> more demanding request.

    Scoring factors:
    - Base score = token count // 10
    - +2 for each recognized complexity keyword present
    - +5 ...

## Constants
- None

## Methods
- `estimate_complexity(request: str) -> int`: description

# get_engine_type_from_env
Determine engine type from INFERENCE_ENGINE environment variable.

## Constants
- None

## Methods
- `get_engine_type_from_env() -> EngineType`: description