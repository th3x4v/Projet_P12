import sentry_sdk
from sentry_sdk.integrations.argv import ArgvIntegration

sentry_sdk.init(
    "https://09a98f0d850dee8f63c4f96cca2d32d1@o4506476129681408.ingest.sentry.io/4506476133351424",
    integrations=[ArgvIntegration()],
    enable_tracing=True,
)
