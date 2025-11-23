import requests
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
import subprocess

class Experiment:
    def __init__(
        self,
        name: str,
        backend_url: str = "http://localhost:8000",
        description: Optional[str] = None,
        user: Optional[str] = None,
        auto_git: bool = True
    ):
        """
        Inicializa um experimento.
        
        Args:
            name: Nome do experimento
            backend_url: URL do servidor backend
            description: Descrição do experimento
            user: Usuário que executou o experimento
            auto_git: Se True, detecta automaticamente branch e commit do Git
        """
        self.name = name
        self.backend_url = backend_url.rstrip("/")
        self.description = description
        self.user = user or os.getenv("USER", "unknown")
        
        self._id: Optional[int] = None
        self._params: Dict[str, Any] = {}
        self._metrics: Dict[str, Any] = {}
        self._artifacts: Dict[str, str] = {}
        
        git_info = self._get_git_info() if auto_git else {}
        
        payload = {
            "name": name,
            "description": description,
            "user": self.user,
            "git_branch": git_info.get("branch"),
            "git_commit": git_info.get("commit"),
        }
        
        try:
            resp = requests.post(f"{self.backend_url}/api/experiments", json=payload)
            resp.raise_for_status()
            data = resp.json()
            self._id = data["id"]
            print(f"✓ Experimento criado: ID {self._id}")
        except Exception as e:
            raise RuntimeError(f"Erro ao criar experimento: {e}")
    
    def log_params(self, params: Dict[str, Any]) -> None:
        """Log de hiperparâmetros."""
        if not self._id:
            raise RuntimeError("Experimento não foi criado corretamente")
        
        self._params.update(params)
        self._sync_to_backend()
        print(f"✓ Parâmetros registrados: {params}")
    
    def log_metrics(self, metrics: Dict[str, Any]) -> None:
        """Log de métricas."""
        if not self._id:
            raise RuntimeError("Experimento não foi criado corretamente")
        
        self._metrics.update(metrics)
        self._sync_to_backend()
        print(f"✓ Métricas registradas: {metrics}")
    
    def log_metric(self, name: str, value: Any) -> None:
        """Log de uma métrica individual."""
        self.log_metrics({name: value})
    
    def save_artifact(self, name: str, obj: Any) -> None:
        """
        Salva um artefato (modelo, plot, etc).
        
        Args:
            name: Nome do artefato (ex: "model", "confusion_matrix")
            obj: Objeto a ser salvo (será pickled)
        """
        if not self._id:
            raise RuntimeError("Experimento não foi criado corretamente")
        
        import pickle
        
        artifacts_dir = Path("./artifacts") / f"exp_{self._id}"
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = artifacts_dir / f"{name}.pkl"
        
        try:
            with open(file_path, "wb") as f:
                pickle.dump(obj, f)
            
            self._artifacts[name] = str(file_path)
            self._sync_to_backend()
            print(f"✓ Artefato salvo: {file_path}")
        except Exception as e:
            print(f"✗ Erro ao salvar artefato: {e}")
    
    def log_file(self, name: str, file_path: str) -> None:
        """
        Registra um arquivo existente como artefato.
        
        Args:
            name: Nome do artefato
            file_path: Caminho do arquivo
        """
        if not self._id:
            raise RuntimeError("Experimento não foi criado corretamente")
        
        if not Path(file_path).exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
        
        artifacts_dir = Path("./artifacts") / f"exp_{self._id}"
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        
        dest_path = artifacts_dir / f"{name}_{Path(file_path).name}"
        
        import shutil
        shutil.copy(file_path, dest_path)
        
        self._artifacts[name] = str(dest_path)
        self._sync_to_backend()
        print(f"✓ Arquivo registrado: {dest_path}")
    
    def set_status(self, status: str) -> None:
        """Define o status do experimento (running, completed, failed)."""
        if not self._id:
            raise RuntimeError("Experimento não foi criado corretamente")
        
        if status not in ["running", "completed", "failed"]:
            raise ValueError(f"Status inválido: {status}")
        
        payload = {"status": status}
        
        try:
            resp = requests.patch(
                f"{self.backend_url}/api/experiments/{self._id}",
                json=payload
            )
            resp.raise_for_status()
            print(f"✓ Status atualizado: {status}")
        except Exception as e:
            print(f"✗ Erro ao atualizar status: {e}")
    
    def end(self, status: str = "completed") -> None:
        """Finaliza o experimento."""
        self.set_status(status)
        print(f"✓ Experimento finalizado!")
    
    def _sync_to_backend(self) -> None:
        """Sincroniza params, metrics e artifacts com o backend."""
        if not self._id:
            return
        
        payload = {
            "params": self._params,
            "metrics": self._metrics,
        }
        
        try:
            requests.patch(
                f"{self.backend_url}/api/experiments/{self._id}",
                json=payload
            )
        except Exception as e:
            print(f"⚠ Aviso: erro ao sincronizar com backend: {e}")
    
    @staticmethod
    def _get_git_info() -> Dict[str, Optional[str]]:
        """Detecta automaticamente branch e commit atual do Git."""
        try:
            branch = subprocess.check_output(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                stderr=subprocess.DEVNULL,
                text=True
            ).strip()
            
            commit = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                stderr=subprocess.DEVNULL,
                text=True
            ).strip()
            
            return {"branch": branch, "commit": commit}
        except (FileNotFoundError, subprocess.CalledProcessError):
            return {}
    
    @property
    def id(self) -> Optional[int]:
        """ID do experimento no servidor."""
        return self._id
    
    def __repr__(self) -> str:
        return f"<Experiment id={self._id} name='{self.name}' status='running'>"


