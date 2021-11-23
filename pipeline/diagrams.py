"""Generates Bindings Diagram."""

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.container import Docker
from diagrams.onprem.queue import RabbitMQ


def _generate_exchange_cluster(
    service_node: Docker,
    node_mapping: dict[str, str],
    direction: str
):
    """Generate a cluster node.

    Args:
        service_node: Node representing the main service.
        node_mapping: Mapping of exchange to routing key.
        direction: Incoming, or outcoming.

    """
    with Cluster(direction):
        for node_name, routing_key in node_mapping.items():
            edge: Edge = Edge(color='black', label=routing_key)
            if direction == 'Incoming':
                exchange_node: RabbitMQ = RabbitMQ(node_name)
                exchange_node >> edge >> service_node
            elif direction == 'Outgoing':
                exchange_node: Docker = Docker(node_name)
                service_node >> edge >> exchange_node


def generate_bindings_diagram(
    settings: dict, *, filename: str = 'docs/images/bindings'
) -> None:
    """Generate bindings diagram for specified in settings dict.

    Args:
        settings: Dictionary of settings.
        filename: Location of where to write file.

    """
    service_name: str = settings.DIAGRAMS_SERVICE_NAME
    with Diagram(
            f'{service_name.upper()} BINDINGS',
            direction='LR',
            filename=filename):
        service_node: Docker = Docker(service_name)

        # Draw incoming exchanges and routing keys
        _generate_exchange_cluster(
            service_node, settings.DIAGRAMS_INCOMING_EXCHANGES, 'Incoming')

        # Really only need to show this if it's a topic exchange.
        # Used when connecting to multiple outgoing queues
        outgoing_exchange_node: RabbitMQ = None
        if settings.DIAGRAMS_OUTGOING_EXCHANGE:
            outgoing_exchange_node = RabbitMQ(
                settings.DIAGRAMS_OUTGOING_EXCHANGE)
            service_node >> Edge(
                color='black', label='#') >> outgoing_exchange_node
            next_node = outgoing_exchange_node
        else:
            next_node = service_node

        # Draw outgoing queues with routing keys
        _generate_exchange_cluster(
            next_node,
            settings.DIAGRAMS_OUTGOING_QUEUES,
            'Outgoing')
