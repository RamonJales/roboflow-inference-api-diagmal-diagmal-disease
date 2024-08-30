import inference

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

model = inference.get_model("malaria_broadinstitute_diagmal/6")

app = FastAPI()

class InferenceResponseImage(BaseModel):
    width: int
    height: int

class ObjectDetectionPrediction(BaseModel):
    x: float
    y: float
    width: float
    height: float
    confidence: float
    class_name: str
    class_id: int
    detection_id: str

class ObjectDetectionInferenceResponse(BaseModel):
    visualization: Optional[str]
    inference_id: Optional[str]
    frame_id: Optional[str]
    time: Optional[float]
    image: InferenceResponseImage
    predictions: List[ObjectDetectionPrediction]


@app.post("/classify/")
async def classify(image_path: str):
    # Realiza a inferência usando o modelo
    result = model.infer(image=image_path)

    # Converte o resultado em um dicionário Python para a resposta JSON
    response = []
    for res in result:
        image_info = InferenceResponseImage(
            width=res.image.width,
            height=res.image.height
        )

        predictions = [
            ObjectDetectionPrediction(
                x=pred.x,
                y=pred.y,
                width=pred.width,
                height=pred.height,
                confidence=pred.confidence,
                class_name=pred.class_name,
                class_id=pred.class_id,
                detection_id=pred.detection_id
            )
            for pred in res.predictions
        ]

        response.append(
            ObjectDetectionInferenceResponse(
                visualization=None,
                inference_id=None,
                frame_id=None,
                time=None,
                image=image_info,
                predictions=predictions
            )
        )

    return response
