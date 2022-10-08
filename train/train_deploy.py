from servicefoundry import Build, Job, PythonBuild, Resources


# servicefoundry uses this specification to automatically create a Dockerfile and build an image,
python_build = PythonBuild(
    python_version="3.9",
    command="python train/train.py",
)
env = {
    # These will automatically map the secret value to the environment variable.
    "MLF_HOST": "https://app.develop.truefoundry.tech",
    "MLF_API_KEY": "djE6dHJ1ZWZvdW5kcnk6dmlzaGFuay1iZXRhdGVzdDoyMzFhYzk="
}
job = Job(
    name="taxi-fare-train",
    image=Build(build_spec=python_build),
    env=env,
    resources=Resources(
        cpu_request=1, cpu_limit=1.5, memory_request=1000, memory_limit=1500
    ),
)
job.deploy(workspace_fqn='tfy-dev-cluster:vishank-unl')