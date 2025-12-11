# Provider Finder AI - Client

A React-based web application that provides an intuitive interface for searching and ranking healthcare providers using natural language queries powered by AI.

## Features

- **Natural Language Search**: Describe what you need in plain English
- **Provider Results Table**: View detailed provider information in an organized table
- **AI-Powered Ranking**: Score and rank providers based on your specific needs
- **Real-time Updates**: Instant feedback with loading states and error handling

## Tech Stack

- **React** with TypeScript
- **TanStack Query** (React Query) for data fetching and caching
- **Material-UI** (MUI) for UI components and icons
- **CSS Modules** for styling

## Usage

### 1. Search for Providers

Enter a natural language query describing what you're looking for:

**Example Queries:**

- "I need a cardiologist who can do an ultrasound near downtown Chicago"
- "Find pediatricians accepting Medicare in California"
- "Orthopedic surgeons with high patient volume in New York"

The search will return:

- Provider specialty
- Location (city, state, zipcode)
- Related medical services (HCPCS descriptions)
- Number of matching providers

### 2. View Results

Search results are displayed in an interactive table showing:

- Provider name and credentials
- Full address
- Medical specialty
- Medicare acceptance status
- Patient statistics (total beneficiaries, average age)

### 3. Score and Rank Providers

After getting search results, you can refine by scoring providers:

1. Click "Find the best providers for you"
2. Enter information about yourself or your needs
3. Providers will be re-ranked with relevance scores

**Example Scoring Queries:**

- "23 year old white male"
- "Senior citizen with heart condition"
- "Pediatric patient needing surgery"

## Project Structure

```
client/
├── src/
│   ├── api/
│   │   └── providers.ts          # API service functions
│   ├── components/
│   │   ├── ProviderTable.tsx     # Results table component
│   │   ├── SearchInput.tsx       # Search input component
│   │   ├── SearchTips.tsx        # Tips and guidance
│   │   └── ScoreDialog.tsx       # Provider scoring dialog
│   ├── pages/
│   │   ├── Home.tsx              # Main home page
│   │   └── Home.module.css       # Page styles
│   └── types/
├── public/
├── index.html
├── package.json
└── vite.config.ts
```

## API Integration

The client connects to the Provider Finder AI API with two main endpoints:

### Search Providers

```typescript
POST /api/search_providers
{
  "query": "string"
}
```

### Rank Providers

```typescript
POST /api/rank_providers
{
  "query": "string",
  "provider_ids": [123, 456, 789]
}
```

For full API documentation, visit: https://ai-provider-finder.onrender.com/docs

## Components

### SearchInput

Reusable search input component with submit functionality.

**Props:**

- `userQuery`: Current query string
- `setUserQuery`: Query state setter
- `handleSubmit`: Form submit handler
- `placeholder`: Input placeholder text

### ProviderTable

Displays provider search or scoring results in a table format.

**Props:**

- `tableData`: Provider data (search or score response)
- `isLoading`: Loading state indicator

### ScoreDialog

Modal dialog for scoring and ranking providers.

**Props:**

- `userQuery`: Current scoring query
- `setUserQuery`: Query state setter
- `handleSubmit`: Form submit handler

### SearchTips

Static component providing helpful search query examples and tips.

## State Management

The application uses React Query for server state management:

- **Search Mutation**: Handles provider search requests
- **Score Mutation**: Handles provider ranking requests
- **Automatic Caching**: React Query caches responses for improved performance
- **Error Handling**: Built-in error states for failed requests

## Error Handling

The application handles various error states:

- Network errors
- API validation errors
- Empty search results
- Failed ranking requests
