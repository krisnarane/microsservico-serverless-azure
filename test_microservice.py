#!/usr/bin/env python3
"""
Simple test script to validate the CPF validation microservice implementation.
This can be run without Azure Functions runtime installed.
"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from cpf_validator import validate_cpf, VALID_TEST_CPFS, INVALID_TEST_CPFS
except ImportError as e:
    print(f"❌ Error importing cpf_validator: {e}")
    sys.exit(1)


def test_basic_validation():
    """Test basic CPF validation functionality."""
    print("🧪 Testing Basic CPF Validation")
    print("-" * 40)
    
    passed = 0
    failed = 0
    
    # Test valid CPFs
    for cpf in VALID_TEST_CPFS:
        result = validate_cpf(cpf)
        if result:
            print(f"✅ {cpf} - Valid (as expected)")
            passed += 1
        else:
            print(f"❌ {cpf} - Should be valid but was invalid")
            failed += 1
    
    # Test invalid CPFs
    for cpf in INVALID_TEST_CPFS:
        result = validate_cpf(cpf)
        if not result:
            print(f"✅ {cpf} - Invalid (as expected)")
            passed += 1
        else:
            print(f"❌ {cpf} - Should be invalid but was valid")
            failed += 1
    
    return passed, failed


def test_api_simulation():
    """Test the API logic simulation."""
    print("\n🌐 Testing API Logic Simulation")
    print("-" * 40)
    
    test_cases = [
        ("GET", "123.456.789-09", None, True),
        ("GET", "11111111111", None, False),
        ("POST", None, {"cpf": "52998224725"}, True),
        ("POST", None, {"cpf": "123.456.789-00"}, False),
        ("GET", None, None, None),  # Missing CPF
    ]
    
    passed = 0
    failed = 0
    
    for method, query_cpf, json_body, expected in test_cases:
        # Simulate the function logic
        cpf = None
        if method == "GET":
            cpf = query_cpf
        elif method == "POST" and json_body:
            cpf = json_body.get('cpf')
        
        if not cpf:
            result = None  # Error case
            response = {
                "error": "CPF not provided",
                "valid": False
            }
        else:
            result = validate_cpf(cpf)
            response = {
                "cpf": cpf,
                "valid": result,
                "message": "CPF is valid" if result else "CPF is invalid"
            }
        
        if result == expected:
            print(f"✅ {method} {cpf or 'None'} - {response}")
            passed += 1
        else:
            print(f"❌ {method} {cpf or 'None'} - Expected {expected}, got {result}")
            failed += 1
    
    return passed, failed


def main():
    """Run all tests."""
    print("🚀 CPF Validation Microservice - Test Suite")
    print("=" * 50)
    
    # Test basic validation
    basic_passed, basic_failed = test_basic_validation()
    
    # Test API simulation
    api_passed, api_failed = test_api_simulation()
    
    # Summary
    total_passed = basic_passed + api_passed
    total_failed = basic_failed + api_failed
    total_tests = total_passed + total_failed
    
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("-" * 20)
    print(f"Total tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Success rate: {(total_passed/total_tests)*100:.1f}%")
    
    if total_failed == 0:
        print("\n🎉 All tests passed! The microservice is ready for deployment.")
        return True
    else:
        print(f"\n💥 {total_failed} tests failed. Please review the implementation.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)