## Submitting Models

The root folder contains the necessary meta-files and references to submit a model to the challenge.

### The Model
[`run.sh`](./run.sh) first runs the [`setup.py`](./nips-defense/setup.py) script, which installs the 
[`SubmittableResNet`](./nips-defense/nips_defense/model/submittable_resnet.py). This is a simple wrapper around 
a `BaseModel` and provides a function that returns a foolbox model, representing the model itself.

### Submitting a New Model
If one wants to submit a newly implemented model (call it `MyModel`), the steps are as follows:

1. Train `MyModel` and create a checkpoint with the flag `save_directory`.
Note the `CHECKPOINT_PATH` where the checkpoint can be found. The checkpoint needs to be added to the repository.
2. Change [`SubmittableResNet`](./nips-defense/nips_defense/model/submittable_resnet.py) to use `MyModel` as
its base class. 
3. If necessary, adjust [`submit.py`](./nips-defense/nips_defense/mains/submit.py) (e.g. change the placeholder
tensor if needed). In most cases however, this step should not be necessary.
4. Move the requirements of all dependencies into a new file called `requirements.txt` placed in the root folder.
5. Update [`run.sh`](./run.sh) and set the `CHECKPOINT_PATH` as the `global_checkpoint` argument
6. Optional: make sure everything works using a VM (with `nvidia-docker` installed) using `avc-test-model .`. This will
test the accuracy of your model.
7. Head over to [crowdai's GitLab](https://gitlab.crowdai.org) and create a new repository. 
Add the new repository as a new remote of this repository, commit and push everything.
8. Run `avc-submit .` to run the evaluation and submit the model.  
