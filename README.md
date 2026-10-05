# Luxury Watch MCP Integration

-   Additional **MCP layer** to the existing Luxury Watch API Integration project.
-   The MCP server connects to the existing authenticated Luxury Watch REST API.
-   The integration uses the existing FastAPI backend running on Cloudflare Workers.
-   Market data is retrieved from Supabase PostgreSQL through Cloudflare Hyperdrive.
-   API credentials are provided through environment variables and are not stored in the repository.
-   Main project: [https://github.com/dcanguven/luxury-watch-api-integration](https://github.com/dcanguven/luxury-watch-api-integration)


## Architecture

```mermaid
flowchart LR
    A["User"] --> B["Local Ollama Model"]
    B --> C["MCP Client"]
    C --> D["Luxury Watch MCP Server"]
    D --> E["Developer API /api/v1"]
    E --> F["FastAPI on Cloudflare Workers"]
    F --> G["Cloudflare Hyperdrive"]
    G --> H["Supabase PostgreSQL"]
```
## MCP Tools

- `list_brands`
- `list_models`
- `search_watches`
- `get_watch`

## Tech Stack

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/Model%20Context%20Protocol-MCP-111111)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-000000?logo=ollama&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3FCF8E?logo=supabase&logoColor=white)
![Cloudflare Workers](https://img.shields.io/badge/Cloudflare%20Workers-F38020?logo=cloudflareworkers&logoColor=white)
