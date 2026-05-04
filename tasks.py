import uuid
from abc import ABC, abstractmethod
from typing import Dict, Optional
import numpy as np

class Task(ABC):
    def __init__(self):
        self.id = str(uuid.uuid4())

    @abstractmethod
    def get_question():
        """Возвращает условие задачи для отображения пользователю."""
        pass

    @abstractmethod
    def get_answer(self):
        """Возвращает правильный ответ (число, вектор, матрицу и т.д.)."""
        pass

class DeterminantTask(Task):
    def __init__(self, matrix: np.ndarray):
        super().__init__()
        self.matrix = matrix
        # Здесь можно сразу вычислить ответ
        self._solution = self._compute_determinant()

    def _compute_determinant(self):
        matrix_np = self.matrix
        return np.linalg.det(matrix_np)

    def get_question(self):
        return self.matrix.tolist()

    def get_answer(self):
        return int(round(self._solution))

class SLAUTask(Task):
    def __init__(self, coef_matrix: np.ndarray, depvar_matrix: np.ndarray):
        super().__init__()
        self.coef_matrix = coef_matrix
        self.depvar_matrix = depvar_matrix
        self._system_solutions = self._solve_system()

    def _solve_system(self):
        return np.linalg.solve(self.coef_matrix, self.depvar_matrix)

    def get_question(self):
        return {"coefficients": self.coef_matrix.tolist(), "biases": self.depvar_matrix.tolist()}

    def get_answer(self):
        return self._system_solutions.flatten().tolist()

class TaskRepository:
    def __init__(self):
        self._storage: Dict[str, Task] = {}  # in-memory хранилище

    def save(self, task: Task):
        self._storage[task.id] = task

    def find_by_id(self, task_id: str) -> Optional[Task]:
        return self._storage.get(task_id)

    def remove(self, task_id: str):
        if task_id in self._storage:
            del self._storage[task_id]