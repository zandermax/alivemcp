# Impact Map — Runtime Dispatch & Thread Safety

## Overview

This map documents the constraints and validation needed when editing runtime dispatch, socket transport, or queue processing logic. These changes are high-risk because they affect thread-safety and Live main-thread execution.

## Trigger Files

- `ALiveMCP_Remote/__init__.py` (ALiveMCP class, `update_display` processing)
- `ALiveMCP_Remote/socket_server.py` (socket handling and queuing)
- `ALiveMCP_Remote/liveapi_tools.py` (dispatch methods exposed to `ALiveMCP`)
- `mcp_server.py` (MCP binding layer)

## Invariants

- All Live API calls execute on the main thread via `update_display()`.
- Socket threads must only enqueue requests and wait on response queues.
- `MAX_COMMANDS_PER_TICK` and queue draining parameters must be bounded to avoid blocking Ableton.

## Required Validation Commands

- `pytest tests/test_alivemcp_socket.py -q`
- `pytest tests/test_mcp_server.py -q`
- Integration smoke test with Ableton connected (manual): run `examples/test_connection.py` and observe no main-thread exceptions.

## Regression Signatures

- Deadlocks or unprocessed queue items observed in `Log.txt`.
- Exceptions logged from `update_display()`.
- Response latencies increase significantly under load.

## Rollback Strategy

- Revert dispatch/queue changes and re-run unit tests, then perform an integration smoke test.

## Where to Start

- Run the socket and mcp_server unit tests in the `tests/` directory.
- If making changes to `update_display()`, ensure thorough test coverage for queue boundaries.
