#!/usr/bin/env python3
"""
Demonstration script showing the fallback functionality of the model router.
This script shows how the router automatically falls back to mistral-small when other models fail.
"""

import sys
import os

# Import from the ultimate_llm_toolkit package
from ultimate_llm_toolkit.model_router import model_router


def demo_fallback_functionality():
    """Demonstrate the fallback functionality."""
    print("🔄 Model Router Fallback Demo")
    print("=" * 50)
    
    # Test 1: Valid model (should work normally)
    print("\n1️⃣ Testing with valid model (anthropic-sonnet):")
    try:
        result = model_router(
            prompt="Say hello in one word",
            model="anthropic-sonnet",
            max_tokens=10
        )
        print(f"✅ Success: {result['content']}")
        print(f"   Model used: {result['model']}")
        print(f"   Provider: {result['provider']}")
        if 'fallback_used' in result:
            print(f"   ⚠️  Fallback was used!")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 2: Invalid model (should fallback to mistral-small)
    print("\n2️⃣ Testing with invalid model (non-existent-model):")
    try:
        result = model_router(
            prompt="Say hello in one word",
            model="non-existent-model",
            max_tokens=10
        )
        print(f"✅ Success: {result['content']}")
        print(f"   Model used: {result['model']}")
        print(f"   Provider: {result['provider']}")
        if 'fallback_used' in result:
            print(f"   ⚠️  Fallback was used!")
            print(f"   Original model: {result['original_model']}")
            print(f"   Fallback reason: {result['fallback_reason']}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Azure model (should work normally)
    print("\n3️⃣ Testing with Azure model (gpt-4.1-mini):")
    try:
        result = model_router(
            prompt="Say hello in one word",
            model="gpt-4.1-mini",
            max_tokens=10
        )
        print(f"✅ Success: {result['content']}")
        print(f"   Model used: {result['model']}")
        print(f"   Provider: {result['provider']}")
        if 'fallback_used' in result:
            print(f"   ⚠️  Fallback was used!")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 4: Already using mistral-small (should work normally, no fallback)
    print("\n4️⃣ Testing with mistral-small (no fallback needed):")
    try:
        result = model_router(
            prompt="Say hello in one word",
            model="mistral-small",
            max_tokens=10
        )
        print(f"✅ Success: {result['content']}")
        print(f"   Model used: {result['model']}")
        print(f"   Provider: {result['provider']}")
        if 'fallback_used' in result:
            print(f"   ⚠️  Fallback was used!")
        else:
            print(f"   ✅ No fallback needed (using requested model)")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Fallback Demo Complete!")
    print("The model router automatically falls back to 'mistral-small' when:")
    print("  • The requested model doesn't exist")
    print("  • The requested model fails to respond")
    print("  • There are API errors with the requested model")
    print("  • Any other failure occurs")


if __name__ == "__main__":
    demo_fallback_functionality() 