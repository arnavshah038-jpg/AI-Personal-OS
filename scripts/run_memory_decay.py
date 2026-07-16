from app.memory.memory_decay_manager import (
    MemoryDecayManager,
)


def main():

    print("=" * 50)
    print("Running Memory Decay...")
    print("=" * 50)

    MemoryDecayManager.run()

    print("=" * 50)
    print("Memory Decay Finished.")
    print("=" * 50)


if __name__ == "__main__":
    main()