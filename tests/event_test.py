import asyncio
import unittest
import uuid

import bospy.events as events


class TestPublish(unittest.TestCase):
    def test_01_publish(self):
        resp = events.publish("test", "hello from unittest", kind="test.publish")
        print(f"published event_id={resp.event_id} offset={resp.offset}")
        self.assertNotEqual(resp.event_id, "")


class TestSubscribe(unittest.IsolatedAsyncioTestCase):
    async def test_01_subscribe(self):
        """Subscribe to test and receive at least one event."""
        # publish something to ensure there's an event to receive
        events.publish("test", "subscribe test probe", kind="test.subscribe")

        async def first_event():
            async for event in events.subscribe(["test"]):
                return event

        event = await asyncio.wait_for(first_event(), timeout=10.0)
        print(f"received event id={event.id} topic={event.topic} type={event.type} payload={event.payload.decode('utf-8')}")
        self.assertIsNotNone(event)
        self.assertNotEqual(event.id, "")


class TestRoundTrip(unittest.IsolatedAsyncioTestCase):
    async def test_01_round_trip(self):
        """Subscribe, publish a uniquely marked message, verify receipt."""
        marker = str(uuid.uuid4())
        consumer_id = f"test-roundtrip-{marker}"

        async def receive():
            async for event in events.subscribe(["test"], consumer_id=consumer_id):
                if marker in event.payload.decode("utf-8"):
                    return event

        task = asyncio.create_task(receive())
        await asyncio.sleep(0.5)  # give subscriber time to connect

        events.publish("test", marker, kind="test.round_trip")

        event = await asyncio.wait_for(task, timeout=10.0)
        print(f"round-trip succeeded: event_id={event.id} payload={event.payload.decode()}")
        self.assertIsNotNone(event)
        self.assertIn(marker, event.payload.decode("utf-8"))


if __name__ == "__main__":
    unittest.main()