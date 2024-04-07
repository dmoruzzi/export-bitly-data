# Export Bitly Data


## About

This Python script is designed to process HTTP Archive (HAR) files exported from Bitly and extract short link data from them. It offers the flexibility to export the extracted data either to JSON format or to a SQLite database.

The script assumes that the input HAR file contains network traffic data captured from interactions with the Bitly API, specifically focusing on requests related to Bitlinks.

## Example Usage

1. Export to JSON

```bash
python main.py --input bitly_data.har --export-json --output-json link_export.json
```

2. Export Bitly data to SQLite:

```bash
python main.py --input bitly_data.har --export-sqlite --output-sqlite bitly_export.db
```

## Produce HAR File

Mozilla Firefox:

1. Navigate to Bitly.com and sign in

1. Click the "Links" navigation option 

1. Open Developer Tools: Right-click anywhere on the page and select "Inspect Element" from the context menu. Alternatively, press Ctrl + Shift + I (Windows/Linux) or Cmd + Option + I (Mac) to open Developer Tools.

1. Navigate to the "Network" Tab: In Developer Tools, click on the "Network" tab.

1. Start Recording: Toggle the network recording by clicking the round button with a dot inside (Start Recording) located at the top-left corner of the "Network" tab.

1. Record Network Activity: Scroll down to the very end beginning of your Bitly links history.


1. Export HAR File: After recording the network activity, right-click anywhere on the list of network requests in the "Network" tab. Then, select "Save All As HAR" to save the network activity as a HAR file.

## Disclaimer

Please be advised that this code is offered without any warranty, whether implied or express. The use of this code is at your own risk. The author shall not be held responsible for any damages or issues that may arise from its use.

It is essential to ensure that your use of this code complies with the Terms of Service (TOS) of the platforms or services involved. Any misuse or violation of TOS is solely the responsibility of the user.
