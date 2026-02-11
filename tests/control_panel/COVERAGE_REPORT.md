# Control Panel Test Coverage Report

Generated: Wed Feb 11, 2025

## Summary
- Total tests: 33
- Coverage: 33.1%
- Status: ⚠️ NEEDS IMPROVEMENT

## Coverage by Module

| Module | Coverage | Status |
|--------|----------|--------|
| blueprints/identities | 17.2% | ⚠️ |
| blueprints/messages | 30.4% | ⚠️ |
| blueprints/logs | 66.0% | ⚠️ |
| blueprints/queue | 36.2% | ⚠️ |
| blueprints/bounties | 13.4% | ⚠️ |
| blueprints/quests | 19.2% | ⚠️ |

## Untested Lines

Files with coverage below 100%:

- vivarium/runtime/control_panel/blueprints/bounties/routes.py: 13.4%
- vivarium/runtime/control_panel/blueprints/artifacts/routes.py: 14.3%
- vivarium/runtime/control_panel/blueprints/system/routes.py: 15.9%
- vivarium/runtime/control_panel/blueprints/rollback/routes.py: 16.8%
- vivarium/runtime/control_panel/blueprints/identities/routes.py: 17.2%
- vivarium/runtime/control_panel/blueprints/chatrooms/routes.py: 17.5%
- vivarium/runtime/control_panel/blueprints/dm/routes.py: 18.6%
- vivarium/runtime/control_panel/blueprints/quests/routes.py: 19.2%
- vivarium/runtime/control_panel/blueprints/spawner/routes.py: 25.8%
- vivarium/runtime/control_panel/blueprints/messages/routes.py: 30.4%
- vivarium/runtime/control_panel/blueprints/groq_key/routes.py: 35.5%
- vivarium/runtime/control_panel/blueprints/queue/routes.py: 36.2%
- vivarium/runtime/control_panel/blueprints/human_request/routes.py: 38.1%
- vivarium/runtime/control_panel/blueprints/completed_requests/routes.py: 42.1%
- vivarium/runtime/control_panel/blueprints/stop_toggle/routes.py: 43.8%
- vivarium/runtime/control_panel/blueprints/ui_settings/routes.py: 44.4%
- vivarium/runtime/control_panel/blueprints/runtime_speed/routes.py: 54.0%
- vivarium/runtime/control_panel/blueprints/logs/routes.py: 66.0%
- vivarium/runtime/control_panel/blueprints/insights/routes.py: 67.5%
- vivarium/runtime/control_panel/middleware.py: 86.2%
- vivarium/runtime/control_panel/blueprints/worker/routes.py: 96.0%

## Action Items
- [ ] Push coverage to 80%+
- [ ] Add property-based tests for queue operations
- [ ] Fuzz test API inputs
