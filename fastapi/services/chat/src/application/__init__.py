from cqrs.commands import (
    Command,
    CommandHandler,
    CommandRegistry,
)
from cqrs.queries import (
    PaginatedQuery,
    Query,
    QueryHandler,
    QueryRegistry,
)

query_reg = QueryRegistry()
command_reg = CommandRegistry()

__all__ = [
    "Command",
    "Query",
    "PaginatedQuery",
    "CommandHandler",
    "QueryHandler",
    "query_reg",
    "command_reg",
]
