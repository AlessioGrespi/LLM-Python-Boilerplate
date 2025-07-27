4#!/usr/bin/env python3
"""
Flask REST API Demo Runner
Easy startup script for the Flask chat demo.
"""

import sys
import os
import subprocess
import time
import argparse
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import flask
        import flask_cors
        import requests
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("📦 Install dependencies with:")
        print("   pip install -r requirements_flask.txt")
        return False

def start_server(port=5001, debug=True):
    """Start the Flask server."""
    print("🚀 Starting Flask Chat Server...")
    print(f"📍 Server will run on http://localhost:{port}")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Start the server
        subprocess.run([
            sys.executable, "flask_chat_server.py"
        ], cwd=Path(__file__).parent)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def start_client(url="http://localhost:5001"):
    """Start the Flask client."""
    print("🎭 Starting Flask Chat Client...")
    print(f"🔗 Connecting to: {url}")
    print("=" * 50)
    
    try:
        # Start the client
        subprocess.run([
            sys.executable, "flask_chat_client.py", "--url", url
        ], cwd=Path(__file__).parent)
    except KeyboardInterrupt:
        print("\n👋 Client stopped by user")
    except Exception as e:
        print(f"❌ Failed to start client: {e}")

def run_tests(test_type="scenarios", url="http://localhost:5001"):
    """Run API tests."""
    print(f"🧪 Running {test_type} tests...")
    print(f"🔗 Testing against: {url}")
    print("=" * 50)
    
    try:
        if test_type == "scenarios":
            subprocess.run([
                sys.executable, "test_flask_api.py", "--scenarios", "--url", url
            ], cwd=Path(__file__).parent)
        elif test_type == "full":
            subprocess.run([
                sys.executable, "test_flask_api.py", "--full", "--url", url
            ], cwd=Path(__file__).parent)
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")

def check_server_health(url="http://localhost:5001"):
    """Check if the server is running and healthy."""
    try:
        import requests
        response = requests.get(f"{url}/api/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "healthy":
                print("✅ Server is healthy and running!")
                print(f"   Active sessions: {data.get('active_sessions', 0)}")
                return True
        print("❌ Server is not responding properly")
        return False
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        return False

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Flask REST API Demo Runner")
    parser.add_argument("mode", choices=["server", "client", "test", "health"], 
                       help="Mode to run")
    parser.add_argument("--port", type=int, default=5001,
                       help="Server port (default: 5001)")
    parser.add_argument("--url", default="http://localhost:5001",
                       help="Server URL (default: http://localhost:5001)")
    parser.add_argument("--test-type", choices=["scenarios", "full"], default="scenarios",
                       help="Type of test to run (default: scenarios)")
    parser.add_argument("--no-deps-check", action="store_true",
                       help="Skip dependency check")
    
    args = parser.parse_args()
    
    # Check dependencies unless skipped
    if not args.no_deps_check and not check_dependencies():
        return 1
    
    # Run the selected mode
    if args.mode == "server":
        start_server(args.port)
    elif args.mode == "client":
        start_client(args.url)
    elif args.mode == "test":
        run_tests(args.test_type, args.url)
    elif args.mode == "health":
        check_server_health(args.url)
    
    return 0

def interactive_menu():
    """Interactive menu for easy demo usage."""
    print("🎭 Flask REST API Demo")
    print("=" * 40)
    print("Choose an option:")
    print("1. Start Server")
    print("2. Start Client")
    print("3. Run Tests (Scenarios)")
    print("4. Run Tests (Full)")
    print("5. Check Server Health")
    print("6. Install Dependencies")
    print("0. Exit")
    print("=" * 40)
    
    while True:
        try:
            choice = input("Enter your choice (0-6): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                start_server()
            elif choice == "2":
                start_client()
            elif choice == "3":
                run_tests("scenarios")
            elif choice == "4":
                run_tests("full")
            elif choice == "5":
                check_server_health()
            elif choice == "6":
                print("📦 Installing dependencies...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", "requirements_flask.txt"
                ], cwd=Path(__file__).parent)
                print("✅ Dependencies installed!")
            else:
                print("❌ Invalid choice. Please enter 0-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    # If no arguments provided, show interactive menu
    if len(sys.argv) == 1:
        interactive_menu()
    else:
        sys.exit(main()) 