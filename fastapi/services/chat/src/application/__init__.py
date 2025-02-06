from cqrs.commands import (
    Command,
    CommandHandler,
    CommandRegistry,
)
from cqrs.queries import (
    Query,
    QueryHandler,
    QueryRegistry,
)

query_reg = QueryRegistry()
command_reg = CommandRegistry()

__all__ = [
    "Command",
    "Query",
    "CommandHandler",
    "QueryHandler",
    "query_reg",
    "command_reg",
]
