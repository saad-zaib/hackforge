#!/usr/bin/env python3
"""
Test AI Docker Generation
"""

import sys
sys.path.append('/home/claude')

# Mock config for testing
class MockConfig:
    machine_id = "test_sqli_001"
    difficulty = 2
    variant = "Error-based SQL Injection"
    blueprint_id = "sql_injection_001"
    application = {"context": "login_system"}
    constraints = {"filters": []}
    flag = {"content": "FLAG{test_flag_12345}"}
    metadata = {"exploit_hints": ["Try basic UNION payloads", "Check error messages"]}


def test_dockerfile_generation():
    """Test Dockerfile generation"""
    print("\n" + "="*60)
    print("TEST 1: Dockerfile Generation")
    print("="*60)
    
    from ai_docker_generator import AIDockerGenerator
    
    gen = AIDockerGenerator()
    
    # Test SQL Injection Dockerfile
    print("\n📝 Generating Dockerfile for SQL Injection...")
    dockerfile = gen.generate_dockerfile("SQL Injection", "sql_injection")
    
    print("\n✓ Generated Dockerfile:")
    print("-"*60)
    print(dockerfile)
    print("-"*60)
    
    # Verify requirements
    checks = {
        "Has FROM php:8.0-apache": "FROM php:8.0-apache" in dockerfile,
        "Has MySQL extensions": "mysqli" in dockerfile or "pdo_mysql" in dockerfile,
        "Has network tools": "iputils-ping" in dockerfile or "ping" in dockerfile,
        "Has Apache config": "apache" in dockerfile.lower(),
        "Has CMD": "CMD" in dockerfile or "ENTRYPOINT" in dockerfile
    }
    
    print("\n📊 Verification:")
    for check, passed in checks.items():
        print(f"  {'✓' if passed else '✗'} {check}")
    
    return all(checks.values())


def test_database_setup():
    """Test database setup generation"""
    print("\n" + "="*60)
    print("TEST 2: Database Setup")
    print("="*60)
    
    from ai_docker_generator import AIDockerGenerator
    
    gen = AIDockerGenerator()
    
    # Test SQL schema generation
    print("\n📝 Generating SQL schema...")
    schema, compose = gen.generate_database_setup(
        "SQL Injection",
        "login_system",
        "FLAG{test_flag}"
    )
    
    print("\n✓ Generated Schema:")
    print("-"*60)
    print(schema[:300] + "..." if len(schema) > 300 else schema)
    print("-"*60)
    
    print("\n✓ Generated Docker Compose Service:")
    print("-"*60)
    print(compose)
    print("-"*60)
    
    # Verify
    checks = {
        "Has CREATE TABLE": "CREATE TABLE" in schema,
        "Has flag": "FLAG{test_flag}" in schema,
        "Has INSERT": "INSERT" in schema,
        "Compose has MySQL": "mysql" in compose.lower(),
        "Compose has volumes": "volumes:" in compose or "volume" in compose
    }
    
    print("\n📊 Verification:")
    for check, passed in checks.items():
        print(f"  {'✓' if passed else '✗'} {check}")
    
    return all(checks.values())


def test_mongodb_setup():
    """Test MongoDB setup"""
    print("\n" + "="*60)
    print("TEST 3: MongoDB Setup")
    print("="*60)
    
    from ai_docker_generator import AIDockerGenerator
    
    gen = AIDockerGenerator()
    
    print("\n📝 Generating MongoDB setup...")
    init_js, compose = gen.generate_mongodb_setup("NoSQL Injection", "FLAG{nosql_test}")
    
    print("\n✓ Generated init.js:")
    print("-"*60)
    print(init_js)
    print("-"*60)
    
    print("\n✓ Generated Compose:")
    print("-"*60)
    print(compose)
    print("-"*60)
    
    checks = {
        "Has db creation": "db" in init_js,
        "Has flag": "FLAG{nosql_test}" in init_js,
        "Has collections": "createCollection" in init_js or "insertOne" in init_js,
        "Compose has mongo": "mongo" in compose.lower(),
        "Compose has volumes": "volumes:" in compose or "volume" in compose
    }
    
    print("\n📊 Verification:")
    for check, passed in checks.items():
        print(f"  {'✓' if passed else '✗'} {check}")
    
    return all(checks.values())


def test_file_structure_setup():
    """Test file structure setup"""
    print("\n" + "="*60)
    print("TEST 4: File Structure Setup")
    print("="*60)
    
    from ai_docker_generator import AIDockerGenerator
    
    gen = AIDockerGenerator()
    
    print("\n📝 Generating file structure setup...")
    setup_sh = gen.generate_file_structure_setup("Path Traversal", "FLAG{path_test}")
    
    print("\n✓ Generated setup.sh:")
    print("-"*60)
    print(setup_sh)
    print("-"*60)
    
    checks = {
        "Has shebang": "#!/bin/bash" in setup_sh,
        "Has flag": "FLAG{path_test}" in setup_sh,
        "Has mkdir": "mkdir" in setup_sh,
        "Has echo": "echo" in setup_sh,
        "Has chmod": "chmod" in setup_sh
    }
    
    print("\n📊 Verification:")
    for check, passed in checks.items():
        print(f"  {'✓' if passed else '✗'} {check}")
    
    return all(checks.values())


def test_docker_compose_generation():
    """Test master docker-compose generation"""
    print("\n" + "="*60)
    print("TEST 5: Master Docker Compose")
    print("="*60)
    
    from ai_docker_generator import AIDockerGenerator
    
    gen = AIDockerGenerator()
    
    # Mock machines
    machines = [
        {
            'machine_id': 'test_sqli_001',
            'port': 8080,
            'category': 'sql_injection'
        },
        {
            'machine_id': 'test_xss_002',
            'port': 8081,
            'category': 'cross_site_scripting'
        },
        {
            'machine_id': 'test_nosql_003',
            'port': 8082,
            'category': 'nosql_injection'
        }
    ]
    
    print("\n📝 Generating docker-compose.yml...")
    compose = gen.generate_docker_compose(machines)
    
    print("\n✓ Generated docker-compose.yml:")
    print("-"*60)
    print(compose)
    print("-"*60)
    
    checks = {
        "Has version": "version:" in compose,
        "Has services": "services:" in compose,
        "Has web services": "test_sqli_001:" in compose,
        "Has DB service": "db_test_sqli_001:" in compose,
        "Has MongoDB service": "mongodb_test_nosql_003:" in compose,
        "Has volumes": "volumes:" in compose
    }
    
    print("\n📊 Verification:")
    for check, passed in checks.items():
        print(f"  {'✓' if passed else '✗'} {check}")
    
    return all(checks.values())


def test_integration():
    """Test full integration"""
    print("\n" + "="*60)
    print("TEST 6: Full Integration")
    print("="*60)
    
    from ai_code_generator import AIEnhancedTemplate
    
    config = MockConfig()
    
    print("\n📝 Generating complete machine setup...")
    template = AIEnhancedTemplate(config, use_ai=True)
    
    # Generate all components
    print("\n1. Generating vulnerable code...")
    code = template.generate_code()
    print(f"   ✓ Code: {len(code)} chars")
    
    print("\n2. Generating Dockerfile...")
    dockerfile = template.generate_dockerfile()
    print(f"   ✓ Dockerfile: {len(dockerfile)} chars")
    
    print("\n3. Generating setup files...")
    setup_files = template.generate_setup_files()
    print(f"   ✓ Setup files: {len(setup_files)}")
    for filename in setup_files.keys():
        print(f"      - {filename}")
    
    success = len(code) > 0 and len(dockerfile) > 0
    print(f"\n{'✓ PASS' if success else '✗ FAIL'}")
    
    return success


def main():
    print("\n" + "="*60)
    print("AI DOCKER GENERATOR - TEST SUITE")
    print("="*60)
    
    results = {}
    
    try:
        results['Dockerfile'] = test_dockerfile_generation()
    except Exception as e:
        print(f"\n✗ Dockerfile test failed: {e}")
        results['Dockerfile'] = False
    
    try:
        results['Database'] = test_database_setup()
    except Exception as e:
        print(f"\n✗ Database test failed: {e}")
        results['Database'] = False
    
    try:
        results['MongoDB'] = test_mongodb_setup()
    except Exception as e:
        print(f"\n✗ MongoDB test failed: {e}")
        results['MongoDB'] = False
    
    try:
        results['FileStructure'] = test_file_structure_setup()
    except Exception as e:
        print(f"\n✗ File structure test failed: {e}")
        results['FileStructure'] = False
    
    try:
        results['DockerCompose'] = test_docker_compose_generation()
    except Exception as e:
        print(f"\n✗ Docker compose test failed: {e}")
        results['DockerCompose'] = False
    
    try:
        results['Integration'] = test_integration()
    except Exception as e:
        print(f"\n✗ Integration test failed: {e}")
        results['Integration'] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        print(f"  {'✓' if passed else '✗'} {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\n{'='*60}")
    print(f"RESULT: {passed}/{total} tests passed")
    print(f"{'='*60}\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
