# AI Provider Finder - Client

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

1. Click "Rank Providers"
2. Enter information about yourself
3. Providers will be re-ranked with relevance scores

**Example Scoring Queries:**

- "23 year old white male"
- "Asian woman aged 68"

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
│       └── provider.ts           # Types
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

# AI Provider Finder API

A FastAPI-based healthcare provider search and ranking system that uses natural language processing to find and rank medical providers based on various criteria.

## Base URL

```
https://ai-provider-finder.onrender.com
```

## API Documentation

Interactive API documentation is available at:

- **Swagger UI**: https://ai-provider-finder.onrender.com/docs

## Endpoints

### 1. Search Providers

Search for healthcare providers using natural language queries.

**Endpoint:** `POST /api/search_providers`

**Request Body:**

```json
{
  "query": "string"
}
```

**Response:**

```json
{
  "success": true,
  "parsed_params": {},
  "results": [
    {
      "id": 0,
      "last_name": "string",
      "first_name": "string",
      "credentials": "string",
      "street_1": "string",
      "street_2": "string",
      "city": "string",
      "state": "string",
      "zipcode": "string",
      "specialty": "string",
      "accepts_medicare": "string",
      "total_benes": 0,
      "avg_age": 0
    }
  ],
  "hcpcs_desc": "string",
  "count": 0,
  "error": null
}
```

**Example Request:**

```bash
curl -X POST "https://ai-provider-finder.onrender.com/api/search_providers" \
  -H "Content-Type: application/json" \
  -d '{"query": "I need a cardiologist who can do an ultrasound near downtown Chicago"}'
```

### 2. Rank Providers

Rank a specific set of providers based on relevance to a query.

**Endpoint:** `POST /api/rank_providers`

**Request Body:**

```json
{
  "query": "string",
  "provider_ids": [0, 1, 2]
}
```

**Response:**

```json
{
  "success": true,
  "parsed_params": {},
  "results": [
    {
      "id": 0,
      "last_name": "string",
      "first_name": "string",
      "credentials": "string",
      "street_1": "string",
      "street_2": "string",
      "city": "string",
      "state": "string",
      "zipcode": "string",
      "specialty": "string",
      "accepts_medicare": "string",
      "total_benes": 0,
      "avg_age": 0,
      "score": 0.95,
      "rank": 1
    }
  ],
  "error": null
}
```

**Example Request:**

```bash
curl -X POST "https://ai-provider-finder.onrender.com/api/rank_providers" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "23 year old white male",
    "provider_ids": [123, 456, 789]
  }'
```

## Data Models

### Provider

Represents a healthcare provider with the following fields:

| Field              | Type    | Description                         |
| ------------------ | ------- | ----------------------------------- |
| `id`               | integer | Unique provider identifier          |
| `last_name`        | string  | Provider's last name                |
| `first_name`       | string  | Provider's first name (nullable)    |
| `credentials`      | string  | Professional credentials (nullable) |
| `street_1`         | string  | Primary street address              |
| `street_2`         | string  | Secondary address line (nullable)   |
| `city`             | string  | City                                |
| `state`            | string  | State                               |
| `zipcode`          | string  | ZIP code                            |
| `specialty`        | string  | Medical specialty                   |
| `accepts_medicare` | string  | Medicare acceptance status          |
| `total_benes`      | integer | Total number of beneficiaries       |
| `avg_age`          | number  | Average patient age                 |

### ScoredProvider

Extends Provider with ranking information:

| Field               | Type    | Description                   |
| ------------------- | ------- | ----------------------------- |
| All Provider fields | -       | Inherits all Provider fields  |
| `score`             | number  | Relevance score (0-100)         |
| `rank`              | integer | Ranking position |

## Response Formats

### NLSResponse (Search)

| Field           | Type       | Description                        |
| --------------- | ---------- | ---------------------------------- |
| `success`       | boolean    | Request success status             |
| `parsed_params` | object     | Parsed query parameters            |
| `results`       | Provider[] | Array of matching providers        |
| `hcpcs_desc`    | string     | HCPCS code description (nullable)  |
| `count`         | integer    | Total result count (nullable)      |
| `error`         | string     | Error message if failed (nullable) |

### RankedProvidersResponse

| Field           | Type             | Description                        |
| --------------- | ---------------- | ---------------------------------- |
| `success`       | boolean          | Request success status             |
| `parsed_params` | object           | Parsed query parameters            |
| `results`       | ScoredProvider[] | Ranked providers with scores       |
| `error`         | string           | Error message if failed (nullable) |

## Error Handling

The API uses standard HTTP status codes:

- `200` - Success
- `422` - Validation Error

Validation errors return:

```json
{
  "detail": [
    {
      "loc": ["string"],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

## Use Cases

### Natural Language Search

Search for providers using conversational queries:

- "Find cardiologists near 10001"
- "Pediatricians accepting Medicare in California"
- "Orthopedic surgeons with high patient volume"

### Provider Ranking

Rank and compare specific providers:

- Score providers based on user information
