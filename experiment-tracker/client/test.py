
from tracker import Experiment

exp = Experiment(name="test_run")
exp.log_params({"lr": 0.001, "epochs": 100})
exp.log_metrics({"accuracy": 0.95, "f1": 0.92})
exp.end()
