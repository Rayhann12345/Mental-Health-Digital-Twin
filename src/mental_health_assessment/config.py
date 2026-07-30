MODEL_NAME = "qwen/qwen3.6-27b"

GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# A draft scoring at least this much is accepted without revision.
PASS_SCORE = 85

# Only one revision is allowed.
MAX_REVISIONS = 1

# Generation settings
ASSESSMENT_MAX_TOKENS = 900
EVALUATION_MAX_TOKENS = 700
REVISION_MAX_TOKENS = 900

# Qwen's recommended non-thinking dialogue temperature is around 0.7.
# We use slightly lower values for more consistent medical-adjacent writing.
ASSESSMENT_TEMPERATURE = 0.55
EVALUATION_TEMPERATURE = 0.20
REVISION_TEMPERATURE = 0.40