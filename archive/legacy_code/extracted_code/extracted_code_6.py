if lesson.get('load_on_demand'):
    import importlib
    importlib.import_module(f"api.{lesson['domains'][0].split(':')[1]}")