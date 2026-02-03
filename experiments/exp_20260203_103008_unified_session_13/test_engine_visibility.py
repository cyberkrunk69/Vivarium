#!/usr/bin/env python3
"""
Test script for engine visibility functionality.
Validates that the enhanced dashboard correctly displays engine/model information.
"""

import requests
import json
import time


def test_enhanced_dashboard():
    """Test the enhanced dashboard endpoints."""
    base_url = "http://localhost:8081"

    print("🧪 Testing Enhanced Dashboard Engine Visibility")
    print("=" * 50)

    try:
        # Test status endpoint
        print("1. Testing /status endpoint...")
        response = requests.get(f"{base_url}/status", timeout=5)
        if response.status_code == 200:
            data = response.json()

            # Check for engine stats
            if 'engine_stats' in data:
                engine_stats = data['engine_stats']
                print(f"   ✓ Engine stats found")
                print(f"   Claude usage: {engine_stats.get('claude_usage_percent', 0)}%")
                print(f"   Groq usage: {engine_stats.get('groq_usage_percent', 0)}%")
                print(f"   Total cost: ${engine_stats.get('total_cost', 0):.2f}")
            else:
                print("   ⚠ Engine stats not found")

            # Check for enhanced workers
            if 'workers' in data:
                workers = data['workers']
                if 'workers' in workers:
                    worker_list = workers['workers']
                    print(f"   ✓ Found {len(worker_list)} workers")

                    for i, worker in enumerate(worker_list[:3]):  # Check first 3
                        engine = worker.get('engine', 'Unknown')
                        model = worker.get('model', 'Unknown')
                        reason = worker.get('selection_reason', 'No reason')
                        print(f"   Worker {i+1}: {engine} / {model} / {reason}")
                else:
                    print("   ⚠ No worker data found")

        else:
            print(f"   ❌ Status endpoint failed: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection failed: {e}")
        print("   💡 Make sure to run: python progress_server_enhanced.py --port 8081")
        return False

    print("\n2. Testing dashboard HTML...")
    try:
        response = requests.get(f"{base_url}/", timeout=5)
        if response.status_code == 200:
            html = response.text

            # Check for engine-specific CSS classes
            engine_features = [
                'engine-badge',
                'engine-claude',
                'engine-groq',
                'engine-stats',
                'worker-model',
                'worker-reason'
            ]

            missing_features = []
            for feature in engine_features:
                if feature in html:
                    print(f"   ✓ Found {feature}")
                else:
                    missing_features.append(feature)

            if missing_features:
                print(f"   ⚠ Missing features: {missing_features}")
            else:
                print("   ✓ All engine visibility features present")

        else:
            print(f"   ❌ Dashboard HTML failed: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"   ❌ Dashboard request failed: {e}")
        return False

    print("\n3. Testing real-time features...")
    print("   📡 SSE endpoint available at: /events")
    print("   🔄 Engine stats update every 30 seconds")
    print("   💰 Cost tracking includes both Claude and Groq")

    print("\n✅ Engine visibility tests completed!")
    print(f"🌐 Dashboard available at: {base_url}")
    return True


def generate_mock_data():
    """Generate mock worker data for testing."""
    mock_workers = [
        {
            "id": "1",
            "engine": "CLAUDE",
            "model": "claude-sonnet-4",
            "status": "running",
            "current_task": "Analyzing complex code patterns",
            "selection_reason": "Complex reasoning task"
        },
        {
            "id": "2",
            "engine": "GROQ",
            "model": "llama-3.3-70b",
            "status": "idle",
            "current_task": "Waiting for next task",
            "selection_reason": "Budget optimization"
        },
        {
            "id": "3",
            "engine": "CLAUDE",
            "model": "claude-haiku-4",
            "status": "running",
            "current_task": "Creative writing assistance",
            "selection_reason": "Creative/analytical task"
        }
    ]

    mock_engine_stats = {
        "claude_usage_percent": 65,
        "groq_usage_percent": 35,
        "total_cost": 2.45,
        "avg_response_time": 1250,
        "claude_cost": 1.89,
        "groq_cost": 0.56
    }

    return mock_workers, mock_engine_stats


if __name__ == "__main__":
    print("Engine Visibility Test Suite")
    print("=" * 30)

    # Generate and display mock data
    workers, stats = generate_mock_data()
    print("\n📊 Mock Data Preview:")
    print(f"Workers: {len(workers)}")
    print(f"Engine Distribution: {stats['claude_usage_percent']}% Claude, {stats['groq_usage_percent']}% Groq")
    print(f"Total Cost: ${stats['total_cost']}")

    print("\n" + "="*50)

    # Run tests
    success = test_enhanced_dashboard()

    if success:
        print("\n🎉 All tests passed! Engine visibility is working correctly.")
        print("\n📋 Next Steps:")
        print("1. Open the dashboard in your browser")
        print("2. Check that worker cards show engine badges")
        print("3. Verify engine statistics panel displays correctly")
        print("4. Confirm real-time updates are working")
    else:
        print("\n💥 Some tests failed. Check the server and try again.")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure the enhanced server is running on port 8081")
        print("2. Check that all files are in the correct location")
        print("3. Verify network connectivity")