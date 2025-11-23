from functools import wraps
from tracker.client import Experiment
from typing import Callable, Any, Dict, Optional

def track_experiment(
    name: Optional[str] = None,
    backend_url: str = "http://localhost:8000",
    auto_log_params: bool = True,
    auto_log_result: bool = True
) -> Callable:
    """
    Decorator para rastrear uma função como experimento.
    
    Args:
        name: Nome do experimento (default: nome da função)
        backend_url: URL do backend
        auto_log_params: Se True, loga automaticamente os argumentos da função
        auto_log_result: Se True, loga o resultado como métrica 'result'
    
    Exemplo:
        @track_experiment()
        def train_model(lr=0.001, epochs=10):
            # código de treinamento
            return {"accuracy": 0.95}
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            exp_name = name or func.__name__
            exp = Experiment(exp_name, backend_url=backend_url)
            
            if auto_log_params:
                # Log dos argumentos
                import inspect
                sig = inspect.signature(func)
                params = {}
                for param_name, param_value in list(zip(
                    sig.parameters.keys(), args
                )) + list(kwargs.items()):
                    params[param_name] = param_value
                
                if params:
                    exp.log_params(params)
            
            try:
                result = func(*args, **kwargs)
                
                if auto_log_result:
                    if isinstance(result, dict):
                        exp.log_metrics(result)
                    else:
                        exp.log_metric("result", result)
                
                exp.end("completed")
                return result
            
            except Exception as e:
                exp.end("failed")
                raise
        
        return wrapper
    return decorator