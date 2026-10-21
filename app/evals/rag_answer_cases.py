RAG_ANSWER_EVAL_CASES = [
    {
        "question": "When will my package arrive?",
        "expected_answer_contains": ["five business days"],
    },
    {
        "question": "How long do I have to request a refund?",
        "expected_answer_contains": ["14 days|fourteen days"],
    },
    {
        "question": "How do I reset my password?",
        "expected_answer_contains": ["reset", "email"],
    },
    {
        "question": "How should I wash the clothing?",
        "expected_answer_contains": ["cold water", "inside out"],
    },
    {
        "question": "Can I pay with cryptocurrency?",
        "expected_answer_contains": [],
    },
    {
        "question": "How long does delivery take and how do I reset my password?",
        "expected_answer_contains": ["five business days", "reset", "email"],
    },
    {
        "question": "What should I do if my order is delayed during the holidays?",
        "expected_answer_contains": ["holidays|high demand", "tracking"],
    },
    {
        "question": "Can I bleach the clothing if I wash it in cold water?",
        "expected_answer_contains": ["do not use bleach|don't use bleach|not use bleach"],
    },
    {
        "question": "If I forgot my password, will the reset link be sent to a different email address?",
        "expected_answer_contains": ["associated email|email address associated"],
    },
    {
        "question": "Can I return an item after 30 days?",
        "expected_answer_contains": ["14 days|fourteen days"],
    },
]