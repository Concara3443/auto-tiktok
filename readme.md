# Auto TikTok

This project automates the editing and uploading of videos to TikTok.

## Installation

### Python Dependencies

1. Make sure you have Python installed. You can download it from [python.org](https://www.python.org/).
2. Install the Python dependencies using `pip`:

    ```sh
    pip install -r requirements.txt
    ```

### Node.js Dependencies

1. Make sure you have Node.js installed. You can download it from [nodejs.org](https://nodejs.org/).
2. Navigate to the directory `functions/tiktok_uploader/tiktok-signature` and install the Node.js dependencies:

    ```sh
    cd functions/tiktok_uploader/tiktok-signature
    npm install
    ```

## Usage

1. Run the main script:

    ```sh
    python main.py
    ```

## Project Structure

- `functions/`: Contains the main functions of the project.
  - `choices.py`
  - `config_funcs.py`
  - `editing.py`
  - `misc_functions.py`
  - `tiktok_uploader/`
    - `__init__.py`
    - `basics.py`
    - `bot_utils.py`
    - `Browser.py`
    - `Config.py`
    - `tiktok.py`
  - `youtube.py`
- `text_files/`: Contains necessary text files.
  - `bottom_video_links.txt`
  - `config.toml`
  - `top_video_links.txt`
- `videos_final/`: Folder where the final videos are saved.
- `videos_temp/`: Folder where temporary videos are saved.
  - `bottom/`
  - `top/`

## Contributions

Contributions are welcome. Please open an issue or a pull request to discuss any changes you would like to make.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.