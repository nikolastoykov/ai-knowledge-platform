RAG_EVAL_CASES = [
    {
        "question": "When will my package arrive?",
        "expected_source_ids": ["shipping-policy"],
    },
    {
        "question": "How long do I have to request a refund?",
        "expected_source_ids": ["refund-policy-long"],
    },
    {
        "question": "How do I reset my password?",
        "expected_source_ids": ["account-security"],
    },
    {
        "question": "How should I wash the clothing?",
        "expected_source_ids": ["product-care"],
    },
    {
        "question": "Do you offer same-day delivery?",
        "expected_source_ids": [],
    },
    {
        "question": "Can I pay with cryptocurrency?",
        "expected_source_ids": [],
    },
    {
        "question": "How long does delivery take and how do I reset my password?",
        "expected_source_ids": ["shipping-policy", "account-security"],
    },
]