# Risky deployment skill fixture

This fixture intentionally declares a dangerous combination for scanner tests.

It reads an API token from `.env`, invokes a bash shell, and uses curl to send data to an HTTPS endpoint.

It is test data only and contains no executable script or real endpoint.