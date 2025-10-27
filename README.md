# Create-Your-Own-Story-With-AI

A full-stack "Choose Your Own Adventure" web application that leverages Google's Gemini AI to generate interactive, branching stories based on user-provided themes.

[![Python](https://img.shields.io/badge/Python-3.10-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg?style=flat&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2-61DAFB.svg?style=flat&logo=react&logoColor=black)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Render](https://img.shields.io/badge/Render-Deploy-46E3B7.svg?style=flat&logo=render&logoColor=white)](https://render.com/)

**Live Demo:** [**https://create-your-own-story-with-ai.onrender.com**](https://create-your-own-story-with-ai.onrender.com)

---

## 📜 Table of Contents

* [Features](#-features)
* [Project Flow & Architecture](#-project-flow--architecture)
* [Tech Stack](#️-tech-stack)
* [Getting Started (Local Setup)](#-getting-started-local-setup)
    * [Prerequisites](#prerequisites)
    * [Installation & Setup](#installation--setup)
    * [Running the Application](#running-the-application)
* [Deployment on Render](#️-deployment-on-render)
* [Configuration](#-configuration)

## ✨ Features

* **AI-Powered Story Generation**: Utilizes Google Gemini (via LangChain) to generate unique, branching storylines from any user-provided theme.
* **Interactive Gameplay**: A clean React UI allows users to select choices that lead them down different narrative paths.
* **Asynchronous Job Processing**: Story generation is handled as a background task, keeping the frontend responsive. The UI polls for completion status.
* **Full-Stack Architecture**: Built with a modern, decoupled stack (FastAPI + React) for scalability and performance.
* **Persistent Storage**: Saves all generated stories, nodes, and job statuses in a **PostgreSQL** database.
* **Fast Package Management**: Employs `uv` instead of `pip` for rapid Python dependency installation and management.

## 📈 Project Flow & Architecture

1.  **Theme Input (React)**: The user enters a theme (e.g., "Pirate Adventure") into the React frontend.
2.  **API Request (FastAPI)**: The frontend sends a POST request to the FastAPI backend's `/stories/create` endpoint.
3.  **Job Creation (PostgreSQL)**: The backend creates a `StoryJob` record in the PostgreSQL database with a `pending` status and returns a `job_id` to the frontend.
4.  **Background Task (FastAPI + Google AI)**:
    * The backend spawns a background task and updates the job status to `processing`.
    * This task calls the Google AI (Gemini) API via LangChain, using the theme and a structured prompt.
    * The AI generates the story, title, content, and options.
    * The generated story and its nodes are saved to the database.
    * The job status is updated to `completed` (or `failed`) and linked to the new `story_id`.
5.  **Polling (React)**: Meanwhile, the frontend periodically polls the `/jobs/{job_id}` endpoint to check the job status.
6.  **Redirect & Play (React)**: Once the frontend detects the `completed` status, it navigates the user to the `/story/{story_id}` page, where they can read and play the story.

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Backend** | Python 3.10.13, FastAPI, SQLAlchemy, LangChain (Google Gemini), Gunicorn |
| **Frontend** | React, Vite, JavaScript, Axios, React Router DOM |
| **Database** | PostgreSQL |
| **Python Tooling** | `uv` (Package Manager) |
| **Deployment** | Render |

## 🚀 Getting Started (Local Setup)

Follow these steps to set up and run the project on your local machine.

### Prerequisites

* **Python `3.10.13`**
* **`uv`** (Python package manager): Install from [astral.sh/uv](https://astral.sh/uv).
* **Node.js** (v18 or newer)
* **PostgreSQL**: A running local instance or access to a cloud database.
* **Google AI API Key**: Obtain from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Installation & Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/aditya-rai0/create-your-own-story-with-ai.git](https://github.com/aditya-rai0/create-your-own-story-with-ai.git)
    cd create-your-own-story-with-ai
    ```

2.  **Backend Setup (`/backend` folder):**
    ```bash
    cd backend

    # 1. Create and activate the virtual environment
    uv venv
    source .venv/bin/activate  # (Linux/macOS)
    # .\.venv\Scripts\Activate.ps1  # (Windows PowerShell)

    # 2. Install dependencies
    uv pip install -r requirements.txt

    # 3. Set up environment variables
    # Create a .env file and add your credentials.
    # See the Configuration section for the template.
    cp .env.example .env 
    # Now, edit the .env file with your keys and DB URL
    ```

3.  **Frontend Setup (`/frontend` folder):**
    ```bash
    cd ../frontend

    # 1. Install Node modules
    npm install

    # 2. Set up environment variables
    # This enables the local development proxy
    echo "VITE_DEBUG=true" > .env
    ```

4.  **Database Setup:**
    * Create a new database in your local PostgreSQL server (e.g., `story_ai_db`).
    * Update the `DATABASE_URL` in `backend/.env` to point to this new database.
    * **First time only**: To create the tables, temporarily uncomment the `create_tables()` call in `backend/main.py` (inside the `if __name__ == "__main__":` block). Run `uvicorn` once, then comment it back out.

### Running the Application

You will need two separate terminals.

1.  **Terminal 1: Backend (FastAPI)**
    * From the `/backend` directory (with virtual env activated):
    ```bash
    uvicorn main:app --reload --host 127.0.0.1 --port 8000
    ```
    * The backend will run at `http://127.0.0.1:8000`.

2.  **Terminal 2: Frontend (React)**
    * From the `/frontend` directory:
    ```bash
    npm run dev
    ```
    * The frontend will run at `http://localhost:5173`.

## ☁️ Deployment on Render

This project is configured for a monorepo deployment on Render using three services.

1.  **Service 1: PostgreSQL Database**
    * On the Render dashboard, create a new **PostgreSQL** instance.
    * Copy the **"Internal Connection URL"** provided.

2.  **Service 2: Backend (Web Service)**
    * Create a new **Web Service** and connect your GitHub repository.
    * **Root Directory**: `backend`
    * **Runtime**: `Python 3`
    * **Build Command**: `uv pip install -r requirements.txt`
    * **Start Command**: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:$PORT`
    * **Environment Variables**:
        * `PYTHON_VERSION`: `3.10.13`
        * `GOOGLE_API_KEY`: (Your Google AI API key)
        * `DATABASE_URL`: (Paste the "Internal Connection URL" from your Render DB)
        * `DEBUG`: `False` (This is crucial for production)
        * `ALLOWED_ORIGINS`: Your deployed frontend URL (e.g., `https://your-frontend-name.onrender.com`)

3.  **Service 3: Frontend (Static Site)**
    * Create a new **Static Site** using the same repository.
    * **Root Directory**: `frontend`
    * **Build Command**: `npm install && npm run build`
    * **Publish Directory**: `frontend/dist`
    * **Rewrite/Redirect Rules**:
        * **Source**: `/*`
        * **Destination**: `/index.html`
        * **Action**: `Rewrite`
    * **Final Step**: Update the `API_BASE_URL` in `frontend/src/util.js` to point to your new backend service URL:
        ```javascript
        // frontend/src/util.js
        export const API_BASE_URL = '[https://your-backend-name.onrender.com/api](https://your-backend-name.onrender.com/api)'; 
        ```
    * Commit and push this change to trigger a new deploy.

## ⚙️ Configuration

Use these templates to create your environment files.

### Backend (`backend/.env`)

Create this file in the `/backend` directory.

```env
# .env.example
# --- Google AI API Key ---
GOOGLE_API_KEY='YOUR_GOOGLE_AI_API_KEY_HERE'

# --- Local Development Database (when DEBUG=True) ---
DATABASE_URL='postgresql://postgres:my_password@localhost:5432/story_ai_db'

# --- Production Database (when DEBUG=False) ---
# These are used by the config if DEBUG is False
DB_USER='render_db_user'
DB_PASSWORD='render_db_password'
DB_HOST='render_db_host'
DB_PORT=5432
DB_NAME='render_db_name'

# --- App Settings ---
DEBUG=True # Set to False in production
ALLOWED_ORIGINS=http://localhost:5173,[http://127.0.0.1:5173](http://127.0.0.1:5173)
