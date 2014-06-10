from flagon.status_api import StatusAPI

# Import and setup the backend to use ...
# from flagon.backends import localmemory
# backend = localmemory.LocalMemoryBackend({})

application = StatusAPI(backend)
