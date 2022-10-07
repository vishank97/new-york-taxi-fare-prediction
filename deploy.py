import logging

from servicefoundry import Build, PythonBuild, Service, Resources

logging.basicConfig(level=logging.INFO)
service = Service(
    name="fastapi-taxi-fare",
    image=Build(
        build_spec=PythonBuild(
            command="uvicorn main:app --port 8000 --host 0.0.0.0",
        ),
    ),
    ports=[{"port": 8000}],
    resources=Resources(memory_limit=1500, memory_request=1000),
)
service.deploy(workspace_fqn="v1:tfy-dev-cluster:vishank-betatest-ws")
