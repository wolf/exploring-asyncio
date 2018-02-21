#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio


async def blink(message, interval):
    while True:
        print(message)
        await asyncio.sleep(interval)


async def cancel_future(future, delay):
    await asyncio.sleep(delay)
    status = future.cancel()
    print(f"Result of calling cancel is {str(status)}")


slow_blink = asyncio.ensure_future(blink("blink", 1.0))
quick_blink = asyncio.ensure_future(blink("quick-blink", 0.5))
asyncio.ensure_future(cancel_future(slow_blink, 5))
asyncio.get_event_loop().run_forever()
