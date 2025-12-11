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
| `score`             | number  | Relevance score (0-1)         |
| `rank`              | integer | Ranking position (default: 0) |

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
