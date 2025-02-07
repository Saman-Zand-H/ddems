from uuid import UUID

MESSAGE_BUFFER_SIZE = 10
MESSAGE_BUFFER_KEY_TEMPLATE = "message_result_buffer:%(message_id)s"


def message_buffer_key(message_id: UUID):
    return MESSAGE_BUFFER_KEY_TEMPLATE % {"message_id": message_id}
