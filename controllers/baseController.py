# controllers/base_controller.py

class BaseController:
    @staticmethod
    def validate_entity(entity, error_message="Entity not found"):
        if entity is None:
            return {"error": error_message}, 404
        return None

    @staticmethod
    def get_data_field(data, field, default=None):
        # Validação comum para campos vazios ou ausentes
        value = data.get(field, default)
        return value if value not in [None, ""] else default
