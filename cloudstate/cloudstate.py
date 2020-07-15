"""
Copyright 2020 Lightbend Inc.
Licensed under the Apache License, Version 2.0.
"""
from typing import Optional

from dataclasses import (dataclass, field)
from typing import List
import os

from concurrent import futures
import grpc

from cloudstate.evensourced_servicer import CloudStateEventSourcedServicer
from cloudstate.event_sourced_entity import EventSourcedEntity
from cloudstate.discovery_servicer import CloudStateEntityDiscoveryServicer
from cloudstate.entity_pb2_grpc import add_EntityDiscoveryServicer_to_server

import logging

from cloudstate.event_sourced_pb2_grpc import add_EventSourcedServicer_to_server

@dataclass
class CloudState:
    logging.basicConfig(format='%(asctime)s - %(filename)s - %(levelname)s: %(message)s', level=logging.INFO)
    logging.root.setLevel(logging.NOTSET)

    host = '127.0.0.1'
    port = '8080'
    workers = 10
    use_domain_sockets: bool = False
    address = '{}:{}'.format(os.environ.get('HOST', host), os.environ.get('PORT', port))
    event_sourced_entities: List[EventSourcedEntity] = field(default_factory=list)

    def use_uds(self):
        self.use_domain_sockets = True
        return self

    def host(self, address: str):
        self.host = address
        return self

    def port(self, port: str):
        self.port = port
        return self

    def max_workers(self, workers: Optional[int] = 10):
        self.workers = workers
        return self

    def register_event_sourced_entity(self, entity: EventSourcedEntity):
        self.event_sourced_entities.append(entity)
        return self

    def start(self):
        if self.use_domain_sockets:
            self.address = 'unix://var/run/cloudstate.sock'

        server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.workers))
        add_EntityDiscoveryServicer_to_server(CloudStateEntityDiscoveryServicer(self.event_sourced_entities), server)
        add_EventSourcedServicer_to_server(CloudStateEventSourcedServicer(self.event_sourced_entities), server)

        logging.info('Starting Cloudstate on address %s', self.address)
        try:
            server.add_insecure_port(self.address)
            server.start()
        except IOError as e:
            logging.error('Error on start Cloudstate %s', e.__cause__)

        server.wait_for_termination()
