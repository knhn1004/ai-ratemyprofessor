# AI Rate My Professor

AI Rate My Professor is a web application that combines the functionality of Rate My Professor with AI-powered insights. It provides users with an interactive chat interface to inquire about professors and receive AI-generated responses based on Rate My Professor data.

## Project Structure

The project consists of two main parts:

1. Frontend: A Next.js application
2. Backend: A FastAPI-based API (ai-rmp-api)

## Frontend

The frontend is built using Next.js, React, and Tailwind CSS. It provides a user-friendly interface for interacting with the AI.

### Getting Started

To run the frontend development server:

```bash
cd frontend
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

### Technologies Used

- Next.js 14.2.6
- React 18
- Tailwind CSS
- TypeScript

## Backend (ai-rmp-api)

The backend is a Python-based API built using FastAPI. It handles the AI logic and interacts with the frontend to provide the AI-generated responses.

### Getting Started

To run the backend development server:

```bash
cd backend
poetry install
poetry run server
```

Open [http://localhost:8000](http://localhost:8000) with your browser to see the API documentation.

### Technologies Used

- FastAPI
- Langchain
- Groq

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.
