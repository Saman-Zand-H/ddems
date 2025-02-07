import asyncio
from typing import AsyncGenerator


async def receive_response(prompt: str, *args, **kwargs) -> AsyncGenerator[str, None]:
    # Simulate streaming response from an external resource
    for i in range(5):
        await asyncio.sleep(1)  # Simulate network delay
        yield f"Response part {i+1} for prompt: {prompt}"
