# controllers/delete_controller.py

from controllers.base_controller import BaseController

class DeleteController(BaseController):
    @staticmethod
    def delete(manager, entity, delete_method, success_message):
        error = DeleteController.validate_entity(entity, "Entity not found")
        if error:
            return error
        result = delete_method(entity)
        return {"message": success_message, "data": result}
