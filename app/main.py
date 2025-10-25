from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

# Initialize FastAPI app
app = FastAPI(
    title="Gemstone Price Prediction API",
    description="API for predicting gemstone prices based on their characteristics",
    version="1.0.0"
)

# CORS middleware - IMPORTANT for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (change in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic model for API validation
class GemstoneData(BaseModel):
    carat: float
    depth: float
    table: float
    x: float
    y: float
    z: float
    cut: str
    color: str
    clarity: str

    # Example values for API documentation
    class Config:
        schema_extra = {
            "example": {
                "carat": 1.5,
                "depth": 62.5,
                "table": 58.0,
                "x": 7.2,
                "y": 7.1,
                "z": 4.5,
                "cut": "Ideal",
                "color": "G",
                "clarity": "VS1"
            }
        }

# Main prediction endpoint
@app.post("/predict")
async def predict_price(gemstone_data: GemstoneData):
    """
    Predict gemstone price based on characteristics
    
    - **carat**: Weight of the gemstone (0.2 - 5.0)
    - **depth**: Depth percentage (40 - 80)
    - **table**: Table percentage (40 - 80)  
    - **x**: Length in mm (3 - 10)
    - **y**: Width in mm (3 - 10)
    - **z**: Height in mm (2 - 8)
    - **cut**: Quality (Fair, Good, Very Good, Premium, Ideal)
    - **color**: Color grade (D, E, F, G, H, I, J)
    - **clarity**: Clarity (I1, SI2, SI1, VS2, VS1, VVS2, VVS1, IF)
    """
    try:
        # Create CustomData object from Pydantic model
        data = CustomData(
            carat=gemstone_data.carat,
            depth=gemstone_data.depth,
            table=gemstone_data.table,
            x=gemstone_data.x,
            y=gemstone_data.y,
            z=gemstone_data.z,
            cut=gemstone_data.cut,
            color=gemstone_data.color,
            clarity=gemstone_data.clarity
        )

        # Get data as DataFrame
        pred_df = data.get_data_as_dataframe()
        
        # Make prediction
        predict_pipeline = PredictPipeline()
        pred = predict_pipeline.predict(pred_df)

        return {
            "status": "success",
            "predicted_price": round(pred[0], 2),
            "input_data": gemstone_data.dict()
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Prediction failed: {str(e)}"
        }

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "Gemstone Price Prediction API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is operational"}

# Get available options for categorical fields
@app.get("/options")
async def get_options():
    """Get available options for categorical fields"""
    return {
        "cut": ["Fair", "Good", "Very Good", "Premium", "Ideal"],
        "color": ["D", "E", "F", "G", "H", "I", "J"],
        "clarity": ["I1", "SI2", "SI1", "VS2", "VS1", "VVS2", "VVS1", "IF"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)