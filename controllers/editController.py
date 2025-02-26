# controllers/edit_controller.py

from controllers.base_controller import BaseController

class EditController(BaseController):
    @staticmethod
    def edit(entity, data, edit_method, success_message):
        error = EditController.validate_entity(entity, "Entity not found")
        if error:
            return error
        
        # Atualiza os campos; espera que o método de edição saiba tratar campos vazios
        result = edit_method(entity, data)
        if result.get("error"):
            return result
        return {"message": success_message, "data": result}
