from servicefoundry import Build, Job, PythonBuild, Resources
import yaml

with open("train/train.yaml", "r") as stream:
    try:
        env_vars = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)


# servicefoundry uses this specification to automatically create a Dockerfile and build an image,
python_build = PythonBuild(
    python_version="3.9",
    command=env_vars['components'][0]['image']['build_spec']['command'],
)
env = {
    # These will automatically map the secret value to the environment variable.
    "MLF_HOST": env_vars['components'][0]['env']['MLF_HOST'],
    "MLF_API_KEY": env_vars['components'][0]['env']['MLF_API_KEY']
}

# Since this is a Job, Job() method will help us package and deploy the training job.
job = Job(
    name=env_vars['name'],
    image=Build(build_spec=python_build),
    env=env,
    resources=Resources(
        cpu_request=1, cpu_limit=2, memory_request=1000, memory_limit=1500
    ),
)


job.deploy(workspace_fqn=env_vars['components'][0]['env']['WORKSPACE_FQN'])

