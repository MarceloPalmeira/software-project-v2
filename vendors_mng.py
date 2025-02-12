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
