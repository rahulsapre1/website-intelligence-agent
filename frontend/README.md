# Website Intelligence Agent - Frontend

A modern, responsive web application built with Next.js and shadcn/ui for the Website Intelligence Agent.

## Features

- **🔐 Secure API Key Management**: Local storage with validation
- **🌐 Website Analysis**: Clean interface for URL input and analysis
- **📊 Business Insights Display**: Organized cards showing 7 core insights
- **💬 AI Chat Interface**: Conversational Q&A about analyzed websites
- **📱 Responsive Design**: Works on mobile, tablet, and desktop
- **🎨 Modern UI**: Beautiful components with shadcn/ui
- **⚡ Real-time Updates**: Live feedback and loading states

## Tech Stack

- **Next.js 15**: React framework with App Router
- **TypeScript**: Type safety and better DX
- **Tailwind CSS**: Utility-first styling
- **shadcn/ui**: Beautiful, accessible components
- **Lucide React**: Modern icons
- **Radix UI**: Headless UI primitives

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- Running Website Intelligence Agent API

### Installation

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm start
```

### Environment Variables

Create a `.env.local` file:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Usage

1. **Enter API Key**: Input your API secret key in the configuration section
2. **Analyze Website**: Enter a website URL and click "Analyze"
3. **View Insights**: Review the extracted business insights
4. **Chat**: Ask follow-up questions about the analyzed website

## Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # shadcn/ui components
│   ├── WebsiteAnalyzer.tsx
│   └── ChatInterface.tsx
├── lib/                   # Utilities
│   ├── api.ts            # API client
│   └── utils.ts          # Helper functions
└── types/                 # TypeScript types
    └── index.ts
```

## Components

### WebsiteAnalyzer
- URL input with validation
- Analysis results display
- Copy-to-clipboard functionality
- Error handling

### ChatInterface
- Message history display
- Real-time chat
- Example questions
- Loading states

## API Integration

The frontend communicates with the FastAPI backend through:
- **POST /api/analyze**: Website analysis
- **POST /api/chat**: Conversational Q&A
- **GET /health**: Health check

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

### Other Platforms

The app can be deployed to any platform that supports Next.js:
- Netlify
- Railway
- Heroku
- AWS Amplify

## Development

```bash
# Run with hot reload
npm run dev

# Type checking
npm run lint

# Build and test
npm run build
```

## License

MIT
