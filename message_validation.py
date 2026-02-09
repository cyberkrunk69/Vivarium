from pydantic import ValidationError
import logging

def validate_and_publish(message_pool, role_instance, output_data):
    """
    Validate the role's output against its declared output_schema before publishing.
    """
    schema = getattr(role_instance, "output_schema", None)
    if schema is None:
        # No schema defined; publish as is
        message_pool.publish(output_data)
        return

    try:
        # This will raise ValidationError if data does not conform
        validated = schema.parse_obj(output_data)
        # Publish the validated dict
        message_pool.publish(validated.dict())
    except ValidationError as e:
        error_msg = f"Output validation failed for role {role_instance.__class__.__name__}: {e}"
        logging.error(error_msg)
        # Publish an error payload for downstream handling
        message_pool.publish({
            "error": error_msg,
            "original_output": output_data
        })