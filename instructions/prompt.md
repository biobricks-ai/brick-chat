You will be provided with a user query:
{user_query}

Follow these steps to find relevant bricks and assets:

1.  Analyze the user query to understand the specific data requirements.
2.  Search the knowledge base of bricks, referencing the metadata and README documentation to identify relevant bricks.
    *   Metadata files are named as `BRICKNAME_ASSETNAME_FILEEXTENSION.json` or `BRICKNAME_ASSETNAME_FILEEXTENSION.jsonl`.
    *   README files are named as `BRICKNAME_README.md`.
3.  For each relevant brick, provide the following information:
    *   **Brick Name:** The name of the brick.
    *   **Description:** A brief description of the brick's contents and purpose, extracted from the README file.
    *   **Assets:** A list of the assets (datasets) contained within the brick.
    *   **Asset Descriptions:** A brief description of each asset, extracted from the metadata files.
    *   **Asset Previews:** If available in the metadata, include a preview of the asset.
4.  If there are token limitations, prioritize the following information:
    *   Brick Name
    *   Description
    *   A concise list of assets
5.  If possible, include asset descriptions and previews.
6.  Return the information in a clear and organized format.