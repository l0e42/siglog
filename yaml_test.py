import yaml

with open("global_parameters.yaml", "r") as yaml_file:
	 global_parameters = yaml.safe_load(yaml_file)

print(global_parameters)
