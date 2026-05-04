import math

def values_are_equal(solution, user_answer, rel_tol=1e-9, abs_tol=1e-6):
    """ Сравнивает одиночное значение или списки с учётом погрешности. """
    if isinstance(solution, list):
        if not isinstance(user_answer, list) or len(solution) != len(user_answer):
            return False
        return all(
            math.isclose(s, u, rel_tol=rel_tol, abs_tol=abs_tol)
            for s, u in zip(solution, user_answer)
        )
    else:
        return math.isclose(solution, user_answer, rel_tol=rel_tol, abs_tol=abs_tol)