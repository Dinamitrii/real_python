import asyncio
import ipaddress
import sys

import mtrpacket

async def trace(host):
    async with mtrpacket.MtrPacket() as mtr:
        for ttl in range(1, 256):
            result = await mtr.probe(host='abv.bg', ttl=ttl)
            print(result)

            if result.success:
                break

asyncio.get_event_loop().run_until_complete(trace(host='abv.bg'))
# asyncio.get_event_loop().run_forever()

