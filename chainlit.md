# Biomedical Data Chat Application

This application provides an AI-powered chat interface to explore biomedical data repositories.  
Repositories are called **bricks**, and each brick contains multiple **assets** (datasets).  
The AI helps users find and use the most relevant bricks and assets for their biomedical research needs.

---

## Features

- **Natural language search**: Ask questions in plain English and receive relevant biomedical bricks.  
  Example: *"Find data on the human genome."*  
  → The AI returns bricks containing genome-related datasets.
- **Context-aware recommendations**: The AI identifies not only relevant bricks but also specific assets within them.  
- **Biomedical focus**: All bricks and assets are curated biomedical datasets.  
- **Flexible applications**: Assets can be used for downstream tasks such as:
  - Creating graphs  
  - Drawing results  
  - Building analytical workflows  

---

## How It Works

1. **Query the AI Chat**: Type your question or request.  
   Example: *"Show me bricks with gene expression data related to cancer."*
2. **Receive Relevant Bricks**: The AI matches your query with the most appropriate biomedical bricks.  
3. **Explore Assets**: Inspect the assets inside each brick to see which datasets fit your needs.  
4. **Use Assets in Applications**: Apply the assets for visualization, analysis, or integration into pipelines.  

---

## Example Usage

```text
User: I need bricks about protein structures.
AI: Found 3 relevant bricks:
  - ProteinAtlas (contains datasets on tissue-specific protein expression)
  - PDB Bricks (structural datasets from the Protein Data Bank)
  - UniProt Brick (annotated protein sequences and functional information)
```

---

## Capabilities

- Retrieves and ranks relevant bricks based on user intent.
- Surfaces both brick-level and asset-level insights.
- Focused exclusively on biomedical datasets to ensure domain relevance.

The system is designed for research support and data discovery, not for clinical decision-making.
