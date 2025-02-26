# controllers/list_controller.py

class ListController:
    @staticmethod
    def list_items(manager, event, list_method):
        if event is None:
            return {"error": "Event not found"}, 404
        items = list_method(event)
        return {"data": items}
