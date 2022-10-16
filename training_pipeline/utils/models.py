from enum import Enum

from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier


class SklearnModelMixin:
    """Sci-Kit Learn mixin class.

    Implements `.fit()` and `.predict()` from sklearn models.
    """
    def fit(self, X, y):
        self._model.fit(X, y)
        return self

    def predict(self, X):
        return self._model.predict(X)


class LogisticModel(SklearnModelMixin):
    def __init__(self, **kwargs):
        super().__init__()
        self._model = LogisticRegression(multi_class='multinomial',
                                         max_iter=1000,
                                         penalty='l2',
                                         random_state=42,
                                         **kwargs)


class SvcModel(SklearnModelMixin):
    def __init__(self, **kwargs):
        self._model = LinearSVC(penalty='l1',
                                dual=False,
                                random_state=42,
                                **kwargs)


class RandomForestModel(SklearnModelMixin):
    def __init__(self, **kwargs):
        self._model = RandomForestClassifier(criterion='entropy',
                                             n_jobs=-1,
                                             random_state=42,
                                             **kwargs)


class ModelBuilder:
    def __init__(self, model):
        self._model = None
        self.model = model

    def __call__(self, **params):
        if not self._model:
            self._model = self.model(**params)
        return self._model


class ModelFactory:
    def __init__(self):
        self._models = {}

    def register_model(self, key, model):
        self._models[key] = model

    def create(self, key, **kwargs):
        model = self._models.get(key)
        if not model:
            err_msg = f'Model "{key}" is not implemented'
            raise ValueError(err_msg)
        return model(**kwargs)


class ModelService(ModelFactory):
    def get(self, model_id, **kwargs):
        return self.create(model_id, **kwargs)


# Instantiate ModelService
_services = ModelService()

# Register models in ModelService
_services.register_model('logistic', ModelBuilder(LogisticModel))
_services.register_model('svc', ModelBuilder(SvcModel))
_services.register_model('random_forest', ModelBuilder(RandomForestModel))


class ModelName(str, Enum):
    """Register model name."""
    logistic = 'logistic'
    svc = 'svc'
    random_forest = 'random_forest'
