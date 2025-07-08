import asyncio

from dotenv import load_dotenv

from matrixbot.main import main

load_dotenv()

if __name__ == "__main__":
    asyncio.run(main())
