from servicefoundry import Build, PythonBuild, Resources, Service


# creating a service object and defining all the configurations
service = Service(
    name="taxi-fare-demo",
    image=Build(
        build_spec=PythonBuild(
            command="streamlit run demo/demo.py",
            python_version="3.9",
        ),
    ),
    env={
        # These will automatically map the secret value to the environment variable.
        "MLF_HOST": "https://app.develop.truefoundry.tech",
        # "INFERENCE_SERVER_URL": "https://fastapi-taxi-fare-vishank-betatest-ws.tfy-ctl-euwe1-develop.develop.truefoundry.tech",
        "MLF_API_KEY": "djE6dHJ1ZWZvdW5kcnk6dmlzaGFuay1iZXRhdGVzdDoyMzFhYzk="
    },
    ports=[{"port": 8501}], #In public cloud deployment TrueFoundry exposes port 8501
    resources=Resources(
        cpu_request=0.5, cpu_limit=.5, memory_limit=2500, memory_request=1500
    ),
)
service.deploy(workspace_fqn='tfy-dev-cluster:vishank-unl')