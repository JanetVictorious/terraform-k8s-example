import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import pickle


app = FastAPI(title='Predicting Penguins')


class Penguin(BaseModel):
    island: str
    culmen_length_mm: float
    culmen_depth_mm: float
    flipper_length_mm: int
    body_mass_g: int
    sex: str


@app.on_event('startup')
def load_model():
    """Load model object from pickle file"""
    with open('./training_pipeline/output/serving/logistic_model.pkl', 'rb') as file:
        # f = file.read().replace(b'\r\n', b'\n')
        global model, feat_idx, targ_feat, targ_conv
        model, feat_idx, targ_feat, targ_conv = pickle.load(file)


@app.get('/')
def home():
    return 'Congratulations, your API is working as expected! Head over to http://localhost:80/docs'


@app.post('/predict')
def predict(penguin: Penguin):
    """Make online predictions"""
    data_point = np.array([[penguin.island,
                            penguin.culmen_length_mm,
                            penguin.culmen_depth_mm,
                            penguin.flipper_length_mm,
                            penguin.body_mass_g,
                            penguin.sex]])

    # Rearrange data point based on feature order
    # from training
    rearr_data_point = [[]]
    for j in feat_idx:
        if targ_feat[0] < j:
            rearr_data_point[0].append(data_point[0][j-1])
        else:
            rearr_data_point[0].append(data_point[0][j])

    # Predict
    pred = model.predict(rearr_data_point).tolist()
    pred = pred[0]

    # Extract penguin name
    pred_name = [k for k, v in targ_conv.items() if v == pred]
    pred_name = pred_name[0]
    print(pred_name)
    return {"Prediction": pred_name}


if __name__ == '__main__':
    """This is for debugging purposes only.

    Run debugger and set breakpoints above where needed.
    Go to http://0.0.0.0/docs and run a POST, the debugger
    will stop at first breakpoint.
    """
    uvicorn.run(app, host='0.0.0.0', port=80)
