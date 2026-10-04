#!/usr/bin/env bash
echo "Reply with exactly: OK" | ./scripts/gemini_call.py gemini-3.8-flash | grep -q "OK"
