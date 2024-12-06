# Magic Dance Web Application

This is a web application that allows users to upload source and pose images to generate dance animations.

## Project Structure

```
web/
├── backend/         # FastAPI backend
│   ├── main.py     # Main FastAPI application
│   └── requirements.txt
└── frontend/        # React frontend
    ├── src/
    │   └── App.tsx # Main React component
    └── package.json
```

## Setup Instructions

### Backend Setup

1. Create a Python virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Run the backend server:
   ```bash
   uvicorn main:app --reload
   ```

The backend will be available at http://localhost:8000

### Frontend Setup

1. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the frontend development server:
   ```bash
   npm run dev
   ```

The frontend will be available at http://localhost:5173

## Usage

1. Open your web browser and navigate to http://localhost:5173
2. Upload a source image (the person/subject)
3. Upload a pose image (the target pose)
4. Click "Generate" to process the images
5. Wait for the results to appear below the form

## API Endpoints

- `POST /upload/`: Upload source and pose images for processing
- `GET /results/{session_id}/{image_name}`: Retrieve generated images 