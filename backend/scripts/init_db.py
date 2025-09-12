#!/usr/bin/env python3
"""
Initialize database with migrations and seed data
"""

import sys
import os
import subprocess
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def main():
    """Initialize the database"""
    print("🚀 Initializing Inno Supps PromptOps Database")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("alembic.ini"):
        print("❌ Please run this script from the backend directory")
        sys.exit(1)
    
    # Run migrations
    if not run_command("alembic upgrade head", "Running database migrations"):
        print("❌ Migration failed. Please check your database connection.")
        sys.exit(1)
    
    # Seed data
    if not run_command("python scripts/seed_data.py", "Loading seed data"):
        print("❌ Seed data loading failed.")
        sys.exit(1)
    
    print("\n🎉 Database initialization completed successfully!")
    print("You can now start the application with: make dev")

if __name__ == "__main__":
    main()
