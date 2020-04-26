def pytest_collection_modifyitems(session, config, items):
    ignored_names = ['test_file']
    items[:] = [item for item in items if item.name not in ignored_names]
