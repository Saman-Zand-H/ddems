from src.application import Query


class QueryMessagesByConversationId(Query):
    conversation_id: str
