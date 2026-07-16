from app.memory.memory_boost_manager import (
    MemoryBoostManager,
)


def main():

    print("=" * 50)
    print("Running Memory Boost...")
    print("=" * 50)

    MemoryBoostManager.run()

    print("=" * 50)
    print("Memory Boost Finished.")
    print("=" * 50)


if __name__ == "__main__":
    main()