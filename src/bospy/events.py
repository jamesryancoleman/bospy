from bospy import common_pb2_grpc
from bospy import common_pb2
from bospy.config import get_events_addr

import grpc

def publish(topic:str, msg:str=None, kind:str=None, content_type='text/plain', partition:str=None, **kwargs):
    if not isinstance(msg, str):
        msg = str(msg)
    kwargs = {k: str(v) for k, v in kwargs.items()}
    response: common_pb2.PublishResponse
    with grpc.insecure_channel(get_events_addr()) as channel:
        stub = common_pb2_grpc.EventBusStub(channel)
        response = stub.Publish(common_pb2.PublishRequest(
            topic=topic,
            type=kind,
            payload=msg.encode("utf-8"),
            payload_content_type=content_type,
            metadata=kwargs,
            partition_key=partition,
        ))
    return response


async def subscribe(topics: list[str], consumer_id: str = None):
    async with grpc.aio.insecure_channel(get_events_addr()) as channel:
        stub = common_pb2_grpc.EventBusStub(channel)
        request = common_pb2.SubscribeRequest(
            topics=topics,
            consumer_id=consumer_id,
        )
        async for event in stub.Subscribe(request):
            yield event

