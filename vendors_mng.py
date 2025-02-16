class VendorsMng:
    def __init__(self):
        self.vendors = {}

    def register_vendor(self, event, name, services):
        if event.id not in self.vendors:
            self.vendors[event.id] = []
        self.vendors[event.id].append({"name": name, "services": services})
        event.vendors.append({"name": name, "services": services})

    def list_vendors(self, event):
        return self.vendors.get(event.id, [])
    
    def edit_vendor(self, event, old_name, new_name, new_services):
        vendors_list = self.vendors.get(event.id, [])
        for vendor in vendors_list:
            if vendor["name"] == old_name:
                vendor["name"] = new_name
                vendor["services"] = new_services
                for v in event.vendors:
                    if v["name"] == old_name:
                        v["name"] = new_name
                        v["services"] = new_services
                        break
                return True
        return False

