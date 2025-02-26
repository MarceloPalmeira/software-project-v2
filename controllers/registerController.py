# controllers/register_controller.py

from controllers.base_controller import BaseController

class RegisterController(BaseController):
    @staticmethod
    def register(manager, event, data, register_method, success_message):
        # Verifica se o evento (ou entidade principal) existe
        error = RegisterController.validate_entity(event, "Event not found")
        if error:
            return error
        
        # Pode adicionar validações genéricas aqui
        result = register_method(event, **data)
        return {"message": success_message, "data": result}
