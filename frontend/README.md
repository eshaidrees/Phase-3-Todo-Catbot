# Todo App Frontend Chatbot

This is the frontend for the Todo application built with Next.js 16+ using the App Router.

## Getting Started

First, install the dependencies:

```bash
npm install
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Environment Variables

Create a `.env.local` file in the root of the frontend directory with the following:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

Make sure your backend server is running on http://localhost:8000 before starting the frontend.

## Features

- Authentication (login/signup)
- Dashboard to manage tasks
- Create, update, delete, and mark tasks as complete
- Responsive design with Tailwind CSS
- Dark mode support

## Tech Stack

- Next.js 16+ (App Router)
- React 19+
- TypeScript
- Tailwind CSS
- React Icons

## API Integration

The frontend communicates with the backend API running on port 8000 by default. The API endpoints are defined in `src/lib/api.ts`.
