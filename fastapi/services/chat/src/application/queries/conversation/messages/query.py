from src.application import PaginatedQuery
from src.domain.choices import Role


class QueryMessagesByConversationId(PaginatedQuery):
    conversation_id: str
    role: Role | None = None
