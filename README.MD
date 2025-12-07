# LLM Project

## Project Setup

This project is divided into two main parts:
1. **Backend**: Contains the logic for the LLM (Large Language Model) operations.
2. **Frontend**: Provides the user interface for interacting with the backend.

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.8 or higher
- Node.js 16 or higher
- npm (Node Package Manager)
- Gemini API Key

### Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
   Also add Gemini API Key in backend/.env

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend application:
   ```bash
   python main.py
   ```

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install the required Node.js packages:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

### Project Structure

```
LLM-project/
├── backend/
│   ├── src/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── src/
│   ├── index.html
│   ├── vite.config.ts
│   └── ...
└── README.MD
```

### Additional Information

- Refer to the `backend/README.md` for backend-specific details.
- Refer to the `frontend/README.md` for frontend-specific details.

### License

This project is licensed under the MIT License. See the LICENSE file for details.
