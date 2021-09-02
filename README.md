# JPL

## Description

JPL is a command-line utility that can convert `.plist` files to/from the JSON encoding, which is a bit easier to work with in most settings.

## Usage

* Converting from Property List to JSON:

    ```shell
    python -m jpl path/to/input.plist -o path/to/output.json
    ```

* Converting from JSON to Property List:

    ```shell
    python -m jpl path/to/input.json -o path/to/output.plist
    ```
